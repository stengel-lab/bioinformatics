# Software reference

This page defines the public catalog structure. Detailed entries will be added after source evidence and publication suitability have been reviewed.

| Function | Questions an entry must answer |
|---|---|
| Quality control | What measurement is checked, and what constitutes a concern? |
| Preprocessing | What is removed or transformed, and how can that change the signal? |
| Alignment | What reference and mapping assumptions are used? |
| Filtering and intervals | Which reads or regions are retained, and why? |
| Quantification | What unit is counted, and what is the denominator? |
| Peak and motif analysis | What null model, background, and threshold are used? |
| Statistical analysis | What design, normalization, effect, and uncertainty are estimated? |
| Visualization | What transformation, aggregation, or normalization is displayed? |
| Contact analysis | How are valid pairs, bins, normalization, and interactions defined? |
| Runtime and installation | What platform, dependency versions, and resources are required? |

Use one directory per tool when there is enough content for multiple pages. Start a single entry with the [tool template](../contributing/templates/tool.md). Record aliases and alternate implementations explicitly.

Each catalog entry must distinguish an observed invocation, a documented dependency, a historical alternative, and a prose-only mention. Explicit version strings describe the source evidence; they do not establish what is installed on another system.
