# Runbook — Privileged Docker launch

Triage actor, sudo session, command, image digest, mounts, capabilities, network, container state, host processes, and file changes. Approved maintenance may be legitimate.

Escalate unapproved privileged launches, sensitive mounts, unknown images, external connections, or host changes. After evidence collection and authorization, stop/remove the container and revoke exposed secrets. Confirm containers, mounts, networks, processes, files, and persistence are absent; verify required workloads and telemetry.
