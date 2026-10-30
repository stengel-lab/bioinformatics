"""Synthetic-only checks for the educational reference-counting example."""

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "docs/assays/cut-and-run/examples/count_reference_segments.py"
spec = importlib.util.spec_from_file_location("reference_counting", SCRIPT)
module = importlib.util.module_from_spec(spec)
previous_bytecode_setting = sys.dont_write_bytecode
try:
    sys.dont_write_bytecode = True
    spec.loader.exec_module(module)
finally:
    sys.dont_write_bytecode = previous_bytecode_setting
MANIFEST = "contig\tlength\trole\nchrX\t1000\ttarget\nchrM\t1000\ttarget\nyeast_chrI\t1000\tspike\n"
STATS = "chrX\t1000\t100\t0\nchrM\t1000\t25\t0\nyeast_chrI\t1000\t50\t0\n*\t0\t0\t3\n"


class ReferenceCountingTests(unittest.TestCase):
    def test_host_x_and_m_not_spike(self):
        result = module.count_segments(MANIFEST, STATS)
        self.assertEqual(result["mapped_segments_by_role"], {"target": 125, "spike": 50, "exclude": 0})
        self.assertEqual(result["unmapped_segments"], 3)
        self.assertEqual(result["unit"], "mapped_read_segments")

    def test_same_names_different_roles_are_manifest_defined(self):
        manifest = MANIFEST.replace("chrM\t1000\ttarget", "chrM\t1000\texclude")
        self.assertEqual(module.count_segments(manifest, STATS)["mapped_segments_by_role"]["exclude"], 25)

    def test_zero_spike_is_reported_without_claiming_calibration(self):
        result = module.count_segments(MANIFEST, STATS.replace("1000\t50", "1000\t0"))
        self.assertFalse(result["spike_count_positive"])

    def test_reject_invalid_manifests(self):
        bad = ["", MANIFEST + "chrX\t1000\tspike\n", MANIFEST.replace("\tspike", "\ttarget"),
               MANIFEST.replace("\ttarget", "\tunknown"), MANIFEST.replace("1000", "0", 1),
               MANIFEST.replace("1000", "-1", 1), MANIFEST + "*\t0\texclude\n",
               MANIFEST.replace("chrX\t", " chrX\t", 1), MANIFEST + "new\t1000\tspike\textra\n"]
        for value in bad:
            with self.subTest(manifest=value), self.assertRaises(ValueError):
                module.count_segments(value, STATS)

    def test_reject_incomplete_mismatched_or_malformed_idxstats(self):
        bad = ["", STATS.replace("chrX\t1000", "chrX\t999"), STATS.replace("chrX\t", "other\t", 1),
               STATS + "chrX\t1000\t1\t0\n", STATS.replace("\t100\t", "\t-1\t"),
               STATS.replace("\t100\t", "\t1.5\t"), STATS.replace("*\t0\t0", "*\t0\t1"),
               STATS.replace("yeast_chrI\t1000\t50\t0\n", ""), STATS.replace("*\t0\t0\t3\n", ""),
               STATS + "\n", STATS.replace("\t", ",")]
        for value in bad:
            with self.subTest(idxstats=value), self.assertRaises(ValueError):
                module.count_segments(MANIFEST, value)

    def test_byte_hashes_and_line_endings(self):
        import hashlib
        text = MANIFEST.replace("\n", "\r\n")
        result = module.count_segments(text, STATS)
        self.assertEqual(result["manifest_sha256"], hashlib.sha256(text.encode()).hexdigest())

    def test_cli_outputs_json_and_preserves_inputs(self):
        with tempfile.TemporaryDirectory() as directory:
            manifest, stats = Path(directory) / "manifest.tsv", Path(directory) / "idxstats.tsv"
            manifest.write_bytes(MANIFEST.encode())
            stats.write_bytes(STATS.encode())
            result = subprocess.run([sys.executable, str(SCRIPT), "--manifest", str(manifest),
                                     "--idxstats", str(stats)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["mapped_segments_by_role"]["spike"], 50)
            self.assertEqual(manifest.read_bytes(), MANIFEST.encode())
            self.assertEqual(stats.read_bytes(), STATS.encode())
            stats.write_text("bad\n")
            failed = subprocess.run([sys.executable, str(SCRIPT), "--manifest", str(manifest),
                                     "--idxstats", str(stats)], capture_output=True, text=True)
            self.assertEqual(failed.returncode, 2)
            self.assertEqual(failed.stdout, "")


if __name__ == "__main__":
    unittest.main()
