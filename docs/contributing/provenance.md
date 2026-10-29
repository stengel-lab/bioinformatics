# Provenance conventions

Use a stable opaque source ID for private evidence. Do not encode a person, sample, experiment, filesystem path, institutional host, or unpublished finding into that ID.

Maintain the full map locally outside Git tracking. Each entry should record original absolute and relative paths, a SHA256 content hash, observation date, line references, relevant command or configuration, and interpretation notes. A modified file needs a new recorded hash; a stable path alone does not identify its contents.

In public documentation, cite only the approved source ID, a safe description, and public primary references. The private map should let an authorized reviewer trace each public claim to exact source lines. Public URLs must lead to approved material; never link a private map or local filesystem path from the website.

Record the publication decision and reviewer per claim or excerpt. Redacting a path is not sufficient when surrounding text contains sensitive metadata or source material with unclear rights. Source comments, installed-version reports, invocation code, and successful run evidence are different evidence types and should remain distinguishable.
