# File formats and coordinates

At each processing boundary, identify what one record represents: a sequencing read, an alignment, a paired fragment, a genomic interval, a feature count, or an aggregated signal bin. A file extension is a clue; inspect its schema and metadata before using it.

A reference record should include organism, genome assembly, annotation source and release, contig naming, and index-generation procedure. Files with the same organism label can still use incompatible coordinates or annotations.

Document the coordinate convention for every interval conversion and show a small synthetic example. Explain whether an interval includes its end position, how strand is represented, and whether the program expects sorted input. For paired data, state whether a measurement counts reads, alignments, fragments, or contacts.

Before publishing a format conversion, cite the format specification and check a known locus or synthetic interval. Do not use visual similarity in a genome browser as the only evidence of a correct conversion.
