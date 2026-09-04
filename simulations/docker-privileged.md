# Privileged Docker command test

On an isolated disposable host, use an approved local image and a command equivalent in safety to a privileged container with no network, no mounts, automatic removal, and `true` as the only workload. The exact command remains subject to operator review.

Expected telemetry is audited sudo/Docker command activity and rule 100056 level 12. A non-privileged equivalent is the negative case. Stop if any mount, network attachment, long-running process, unexpected image pull, or host modification occurs.

Confirm the container is absent, no networks/volumes were created, no process persists, and required workloads remain healthy. This detects a command pattern and does not demonstrate container escape.
