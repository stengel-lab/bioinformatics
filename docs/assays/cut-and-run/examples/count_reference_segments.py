"""Teaching example: audit idxstats against a complete, reviewed contig manifest.

Reads text only. No BAM access, alignment, normalization, or workflow execution.
The manifest assigns every contig exactly one role: target, spike, or exclude.
Species identity must come from reference provenance, never inferred here.
"""

import argparse
import csv
import hashlib
import io
import json
from pathlib import Path


def nonnegative_integer(value, label):
    if not value or not value.isascii() or not value.isdecimal():
        raise ValueError(f"{label}: expected a nonnegative integer")
    return int(value)


def count_segments(manifest_text, idxstats_text):
    """Validate full contig/length agreement and sum mapped read-segments by role."""
    reader = csv.DictReader(io.StringIO(manifest_text), delimiter="\t")
    if reader.fieldnames != ["contig", "length", "role"]:
        raise ValueError("manifest header must be: contig<TAB>length<TAB>role")
    manifest = {}
    for row in reader:
        if None in row or any(value is None for value in row.values()):
            raise ValueError("manifest row must have exactly three fields")
        name, size, role = row["contig"], row["length"], row["role"]
        if not name or name == "*" or name != name.strip() or any(c.isspace() for c in name):
            raise ValueError("invalid manifest contig name")
        if name in manifest:
            raise ValueError(f"duplicate manifest contig: {name}")
        length = nonnegative_integer(size, "contig length")
        if length == 0 or role not in {"target", "spike", "exclude"}:
            raise ValueError("manifest needs positive lengths and target/spike/exclude roles")
        manifest[name] = (length, role)
    if not {"target", "spike"}.issubset({role for _, role in manifest.values()}):
        raise ValueError("manifest must contain both target and spike contigs")

    counts = {"target": 0, "spike": 0, "exclude": 0}
    unmapped = 0
    seen = set()
    for line in idxstats_text.splitlines():
        if not line.strip():
            raise ValueError("blank idxstats row")
        fields = line.split("\t")
        if len(fields) != 4:
            raise ValueError("idxstats rows must have four TAB-separated fields")
        name, size, mapped, missing = fields
        if name in seen:
            raise ValueError(f"duplicate idxstats contig: {name}")
        seen.add(name)
        length = nonnegative_integer(size, "idxstats length")
        mapped = nonnegative_integer(mapped, "mapped segments")
        missing = nonnegative_integer(missing, "unmapped segments")
        unmapped += missing
        if name == "*":
            if length != 0 or mapped != 0:
                raise ValueError("invalid idxstats '*' row")
            continue
        if name not in manifest:
            raise ValueError(f"unclassified contig: {name}")
        expected_length, role = manifest[name]
        if length != expected_length:
            raise ValueError(f"reference length mismatch: {name}")
        counts[role] += mapped
    if set(manifest) != seen - {"*"} or "*" not in seen:
        raise ValueError("idxstats needs the complete manifest contig set and '*' row")
    return {
        "schema_version": 1,
        "unit": "mapped_read_segments",
        "contigs_checked": len(manifest),
        "mapped_segments_by_role": counts,
        "unmapped_segments": unmapped,
        "spike_count_positive": counts["spike"] > 0,
        "manifest_sha256": hashlib.sha256(manifest_text.encode("utf-8")).hexdigest(),
        "idxstats_sha256": hashlib.sha256(idxstats_text.encode("utf-8")).hexdigest(),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--idxstats", type=Path, required=True)
    args = parser.parse_args()
    try:
        # Preserve line endings so the hashes identify the actual UTF-8 input bytes.
        manifest = args.manifest.read_bytes().decode("utf-8")
        idxstats = args.idxstats.read_bytes().decode("utf-8")
        result = count_segments(manifest, idxstats)
    except (OSError, UnicodeError, ValueError) as exc:
        parser.exit(2, f"reference-counting error: {exc}\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
