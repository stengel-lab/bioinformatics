# Installation overview

Choose an environment per workflow and record its operating system, architecture, runtime versions, package sources, and reference data. Package names alone do not define a reproducible environment.

| Platform | Starting point | Review still needed |
|---|---|---|
| [Windows](windows.md) | Native documentation and supported desktop tools; consider WSL for Linux command-line software | Per-tool support, path handling, filesystem performance |
| [macOS](macos.md) | Isolated environments; distinguish Apple Silicon and Intel | Platform builds, binary compatibility, memory limits |
| [Linux](linux.md) | Shell and isolated tool environments | Distribution libraries, reference indexes, resource use |
| [HPC](hpc.md) | Site-supported modules, environments, or approved containers | Scheduler policy, storage, compute resources, local configuration |

No cross-platform analysis installation recipe is validated in this milestone. The [documentation preview](../getting-started/preview.md) has its own environment.
