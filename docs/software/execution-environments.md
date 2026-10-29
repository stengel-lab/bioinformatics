# Bash, Conda, Slurm and command-line utilities

**Function:** Execution environment. **Evidence:** [CR-S01–CR-S04 / CR-S07–CR-S09 / CR-S22](../assays/cut-and-run/sources.md).

**Observed version evidence:** No complete shell/scheduler/Conda/module lock; environment names are not package specifications.

The original workers assume a Linux shell, Conda activation, shared storage and a Slurm scheduler. Core methods can be taught manually without reproducing the original supervisor. Native Windows PowerShell cannot interpret Bash syntax; use WSL2 or remote Linux for these command examples.

| Component | Actual role and portability concern |
|---|---|
| Bash | Pipelines, arrays, arithmetic and error handling; `set -e` has context-dependent behavior |
| Conda | Activates `cutrun` and `genomics` environments; names do not determine installed versions |
| Slurm | `sbatch` arrays/dependencies, resource and log settings; not installed by WSL2 |
| awk, sed, grep, sort, cut, find, gzip, coreutils | Sample selection, text tables, sorting, compression and file checks; GNU-specific options need review on macOS |
| flock / temporary locks | Some workers use job-scoped lock paths; distinct jobs may still race on shared outputs |
| Environment modules | Site-dependent initialization in historical/external wrappers; no portable module specification established |
| Python/R/Perl | Statistical code, helpers and HOMER runtime; dependencies belong to reviewed environments |

**Installation:** Linux/WSL2 or a compatible macOS environment, with a reviewed package manager. Use site-provided Slurm only on an authorized cluster. Consult [Conda create](https://docs.conda.io/projects/conda/en/stable/commands/create.html), [Slurm sbatch](https://slurm.schedmd.com/sbatch.html) and [Bash manual](https://www.gnu.org/software/bash/manual/). The tutorial's candidate Conda commands use `--dry-run`; they have not been solved here.

**Configured inspection example:** inspect tool identity and basic resource context; no job submission.

```bash
command -v bash conda bowtie2 samtools Rscript
uname -s
df -h .
```

**Input → output:** shell commands plus environment/reference identity → logs and analysis artifacts. The source's core read array is one-based while its averaging array is zero-based. `afterany` allows downstream jobs after upstream failures; output existence is weaker than successful completion. The coverage post-increment under `set -e` can return failure even when a track exists. See the [operational decision](../assays/cut-and-run/decisions.md#d18-scheduler-restarts-and-exit-status). No original scheduler wrapper was executed or published in this milestone.

## Setup and workflow links

Follow the shared [CUT&RUN installation and reference guide](../assays/cut-and-run/installation.md) for candidate environments, platform limitations and version recording. Installation commands and analysis examples are **not execution-verified** in this milestone.

Return to the [relevant CUT&RUN lesson](../assays/cut-and-run/installation.md) or [software catalog](index.md). Tool invocation is source evidence, not proof that a workflow was scientifically validated.
