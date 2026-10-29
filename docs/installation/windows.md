# Windows

Documentation can be read in a browser or previewed with native Python. Follow the [PowerShell preview instructions](../getting-started/preview.md).

For analysis, check whether each tool supports Windows directly. WSL provides a Linux userspace for tools that require it; document the selected distribution and tool versions rather than assuming every Linux workflow will transfer unchanged.

Record Windows versus Linux paths, quoting, line endings, executable permissions, data storage location, and available memory. Confirm that all reference files are accessible from the environment running the command. A native desktop launcher may control a remote Linux job without executing its analysis locally.

The [CUT&RUN setup guide](../assays/cut-and-run/installation.md) describes a WSL2 route and candidate Linux environments. Those analysis installations have not been performed in this milestone. Native PowerShell is used for WSL setup, then Bash inside Linux for assay commands.
