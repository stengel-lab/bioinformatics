# Bash, Conda, Slurm and command-line utilities

The original workers assume a Linux shell, Conda activation, shared storage and a Slurm scheduler. Core methods can be taught manually without reproducing the original supervisor. Native Windows PowerShell cannot interpret Bash syntax; use WSL2 or remote Linux for these command examples.

| Component | Actual role and portability concern |
|---|---|
| Bash | Pipelines, arrays, arithmetic and error handling; `set -e` has context-dependent behavior |
| Conda | Activates `cutrun` and `genomics` environments; names do not determine installed versions |
| Slurm | `sbatch` arrays/dependencies, resource and log settings; not installed by WSL2 |
| awk, sed, grep, sort, cut, find, gzip, coreutils | Sample selection, text tables, sorting, compression and file checks; GNU-specific options need review on macOS |
| flock / temporary locks | Some workers use job-scoped lock paths; distinct jobs may still race on shared outputs |
| bc / xargs | Coverage worker tests the median with `bc -l` and launches concurrent Bash children with `xargs`; these are explicit runtime dependencies |
| Environment modules | Site-dependent initialization in historical/external wrappers; no portable module specification established |
| Python/R/Perl | Statistical code, helpers and HOMER runtime; dependencies belong to reviewed environments |

## Install

Install [Conda using its official instructions](https://docs.conda.io/projects/conda/en/stable/user-guide/install/index.html). Use Bash on Linux/macOS or [WSL2 on Windows](../installation/windows.md). Slurm is provided by a cluster administrator; local use of these examples does not require a scheduler.

Installation examples are candidates, **not verified installations**. Check your platform and solve first with `--dry-run` when using Conda. Linux and macOS package builds vary; run Linux command examples in WSL2 on Windows. See [installation help](../installation/index.md) for platform setup and [shared workflow environments](../assays/cut-and-run/installation.md#candidate-environments) to avoid installing a separate environment for every tool.

## Verify installation

```bash
bash --version
conda --version
command -v bash conda
```

Confirm that the command/package resolves in the intended environment. A version or startup check does not validate an analysis.

## Basic syntax

```text
conda activate ENVIRONMENT
command -v TOOL
TOOL [options]
```

## Common options

| Option / setting | Meaning |
|---|---|
| `conda create --name` | Create an isolated named environment. |
| `--dry-run` | Inspect a proposed environment without installing it. |
| `--strict-channel-priority` | Prefer higher-priority channels consistently. |
| `command -v` | Show which executable the active shell will use. |

## Workflow example

Examples use fictional sample names and require the indicated inputs. Analysis commands have not been executed as a complete teaching workflow.

```bash
command -v bash conda bowtie2 samtools Rscript
command -v bc flock xargs
uname -s
df -h .
```

## Expected inputs and outputs

shell commands plus environment/reference identity → logs and analysis artifacts. The source's core read array is one-based while its averaging array is zero-based. `afterany` allows downstream jobs after upstream failures; output existence is weaker than successful completion. The coverage post-increment under `set -e` can return failure even when a track exists. See the [operational decision](../assays/cut-and-run/decisions.md#d18-scheduler-restarts-and-exit-status). No original scheduler wrapper was executed or published in this milestone.

Parent `set -euo pipefail` is not an explicit error contract for a newly launched `bash -c` worker. Configure/check child options and producer exit statuses in a future reviewed implementation; a successful downstream log formatter can otherwise hide a failed producer. Assignment through `local name=$(...)` can also obscure failure. These source-level concerns were examined with synthetic shell examples, not original jobs.

## Documentation and lab notes

Installation notes: linux/WSL2 or a compatible macOS environment, with a reviewed package manager. Use site-provided Slurm only on an authorized cluster. Consult [Conda create](https://docs.conda.io/projects/conda/en/stable/commands/create.html), [Slurm sbatch](https://slurm.schedmd.com/sbatch.html) and [Bash manual](https://www.gnu.org/software/bash/manual/). The tutorial's candidate Conda commands use `--dry-run`; they have not been solved here.

**Function:** Execution environment. **Evidence:** [CR-S01–CR-S04 / CR-S07–CR-S09 / CR-S22](../assays/cut-and-run/sources.md).

**Observed version evidence:** No complete shell/scheduler/Conda/module lock; environment names are not package specifications.

Continue to [relevant CUT&RUN lesson](../assays/cut-and-run/installation.md) or [software catalog](index.md).
