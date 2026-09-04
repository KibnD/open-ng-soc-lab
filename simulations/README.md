# Controlled simulations

These procedures are plans for an isolated lab and remain `documented-only` until their public fixtures and expected results are available. Read [safety controls](safety-and-cleanup.md) first.

| Procedure | Related rules | Method | State |
|---|---|---|---|
| [Synthetic CloudTrail](synthetic-cloudtrail.md) | 100053 | Local JSON event only | `simulated` privately |
| [AD identity tests](ad-identity.md) | 100054, 100055, 100057 | Disposable disabled/test identities | `tested-private` |
| [Container test](docker-privileged.md) | 100056 | No network, no mounts, `true` workload | `tested-private` |
| [Network replay](network-replay.md) | 100051, 100100 | Sanitized log replay | `tested-private` |

No malware, exploit delivery, credential theft, operational log clearing, unsafe PCAP, or real third-party targeting is required.
