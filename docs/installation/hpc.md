# High-performance computing

An HPC tutorial needs both a software environment and a site-specific resource configuration. Use placeholders for account names, partitions, hosts, and storage locations in public examples.

Document the scheduler, CPU and memory requests, wall time, array indexing, job dependencies, log locations, scratch cleanup, and restart behavior. Explain where software modules or container runtimes come from and which operations are permitted on login versus compute nodes.

Keep site configuration outside reusable teaching commands. Record reference data and external container image versions or digests. A path to an environment or image does not prove that it exists or has the required contents.

This milestone does not submit jobs or validate any site's analysis environment.

The [CUT&RUN source reconstruction](../assays/cut-and-run/sources.md#computational-requests-in-the-sources) records observed resource requests and scheduler assumptions. Read its restart/dependency cautions before adapting any private worker. The public lesson contains manual commands, not a cluster submission pipeline.
