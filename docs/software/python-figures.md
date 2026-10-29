# Python figure libraries and custom helpers

**Function:** Figure composition and interval-set visualization. **Evidence:** [CR-S23 / CR-S24](../assays/cut-and-run/sources.md).

**Observed version evidence:** Pillow, matplotlib and optional matplotlib-venn versions not established.

Selected custom helpers arrange motif-table images and plot interval-set Venn summaries. These are visualization utilities, not independent evidence of reproducibility. Set membership must be defined before a Venn diagram is meaningful.

| Library | Observed role | Primary reference |
|---|---|---|
| Pillow (`PIL`) | Image loading, text/drawing, layout and composition | [Overview](https://pillow.readthedocs.io/en/stable/handbook/overview.html) |
| matplotlib | Figure generation and rendering | [Installation](https://matplotlib.org/stable/users/installing/index.html) |
| matplotlib-venn | Optional two/three-set diagrams in a helper | [Maintainer repository](https://github.com/konstantint/matplotlib-venn) |
| Python standard library | CSV, paths, subprocess and utility logic | Supplied with Python; not extra PyPI packages |

**Installation:** optional figure environment in the setup guide; check Python/platform compatibility and fonts. These selected helpers do not establish a dependency on pandas or CairoSVG. Do not copy the private helpers or their hardcoded sample rules into a public runner without a separate review.

**Configured basic usage with synthetic values only:**

```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib_venn import venn2
fig, ax = plt.subplots()
venn2(subsets=(3, 2, 1), set_labels=("set_A", "set_B"), ax=ax)
fig.savefig("synthetic_set_example.png", dpi=150)
plt.close(fig)
```

**Input → output:** reviewed tables/images/set counts → figures. Counts here are fictional and the code was syntax-checked only. Sets shared across contrasts are not biological-replicate consensus. Retain underlying counts, set definitions, coordinate rules and source-table provenance. Inspect cropping, readable fonts and labels before publication; image assembly must not obscure the statistical question.

## Setup and workflow links

Follow the shared [CUT&RUN installation and reference guide](../assays/cut-and-run/installation.md) for candidate environments, platform limitations and version recording. Installation commands and analysis examples are **not execution-verified** in this milestone.

Return to the [relevant CUT&RUN lesson](../assays/cut-and-run/04-differential-and-interpretation.md#stage-16-figures-that-preserve-the-measurement) or [software catalog](index.md). Tool invocation is source evidence, not proof that a workflow was scientifically validated.
