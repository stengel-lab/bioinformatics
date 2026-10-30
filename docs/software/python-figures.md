# Python figure libraries and custom helpers

Selected custom helpers arrange motif-table images and plot interval-set Venn summaries. These are visualization utilities, not independent evidence of reproducibility. Set membership must be defined before a Venn diagram is meaningful.

| Library | Observed role | Primary reference |
|---|---|---|
| Pillow (`PIL`) | Image loading, text/drawing, layout and composition | [Overview](https://pillow.readthedocs.io/en/stable/handbook/overview.html) |
| matplotlib | Figure generation and rendering | [Installation](https://matplotlib.org/stable/users/installing/index.html) |
| matplotlib-venn | Optional two/three-set diagrams in a helper | [Maintainer repository](https://github.com/konstantint/matplotlib-venn) |
| Python standard library | CSV, paths, subprocess and utility logic | Supplied with Python; not extra PyPI packages |

## Install

Inside an isolated Python environment:

```bash
python -m pip install matplotlib Pillow matplotlib-venn
```

Installation examples are candidates, **not verified installations**. Check your platform and solve first with `--dry-run` when using Conda. Linux and macOS package builds vary; run Linux command examples in WSL2 on Windows. See [installation help](../installation/index.md) for platform setup and [shared workflow environments](../assays/cut-and-run/installation.md#candidate-environments) to avoid installing a separate environment for every tool.

## Verify installation

```bash
python -c "import matplotlib, PIL, matplotlib_venn; from importlib.metadata import version; print({p: version(p) for p in ['matplotlib', 'Pillow', 'matplotlib-venn']})"
```

Confirm that the command/package resolves in the intended environment. A version or startup check does not validate an analysis.

## Basic syntax

```text
fig, ax = plt.subplots(); ...; fig.savefig("figure.png")
```

## Common options

| Option / setting | Meaning |
|---|---|
| `matplotlib.use("Agg")` | Select a noninteractive renderer for headless systems. |
| `venn2(subsets=...)` | Supply A-only, B-only and shared counts in that order. |
| `savefig(..., dpi=150)` | Write a raster figure at the requested resolution. |

## Workflow example

Examples use fictional sample names and require the indicated inputs. Analysis commands have not been executed as a complete teaching workflow.

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

## Expected inputs and outputs

reviewed tables/images/set counts → figures. Counts here are fictional and the code was syntax-checked only. Sets shared across contrasts are not biological-replicate consensus. Retain underlying counts, set definitions, coordinate rules and source-table provenance. Inspect cropping, readable fonts and labels before publication; image assembly must not obscure the statistical question.

## Documentation and lab notes

Installation notes: optional figure environment in the setup guide; check Python/platform compatibility and fonts. These selected helpers do not establish a dependency on pandas or CairoSVG. Do not copy the private helpers or their hardcoded sample rules into a public runner without a separate review.

**Function:** Figure composition and interval-set visualization. **Evidence:** [CR-S23 / CR-S24](../assays/cut-and-run/sources.md).

**Observed version evidence:** Pillow, matplotlib and optional matplotlib-venn versions not established.

Continue to [relevant CUT&RUN lesson](../assays/cut-and-run/04-differential-and-interpretation.md#stage-16-figures-that-preserve-the-measurement) or [software catalog](index.md).
