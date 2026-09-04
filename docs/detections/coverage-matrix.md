# Detection coverage matrix

The [manifest](../../detections/tests/manifest.json) is authoritative. None is `reproduced-public` because exact XML and fixtures have not passed public Wazuh execution.

| Rule | Data source | Level | ATT&CK | Evidence | Fixtures | Target |
|---:|---|---:|---|---|---|---|
| 100051 | Suricata EVE via pfSense | 8 | Signature-dependent | `tested-private` | Pending | v0.1.0 |
| 100052 | Windows Security log | 12 | T1070.001 | `tested-private`; PT-05 NOT RUN | Pending synthetic fixtures | v0.1.0 |
| 100053 | Synthetic CloudTrail | 12 | T1098.001 | `simulated` | Pending | v0.1.0 |
| 100054 | Windows event 4728 | 14 | T1098 | `tested-private` | Pending | v0.1.0 |
| 100055 | Windows event 4769 | 12 | T1558.003 | `tested-private` | Pending | v0.1.0 |
| 100056 | Linux sudo/audit | 12 | T1611 | `tested-private` | Pending | v0.1.0 |
| 100057 | Windows event 4625 correlation | 10 | T1110.001 | `tested-private` | Pending stateful fixtures | v0.1.0 |
| 100058 | PowerShell event 4104 | 10 | T1059.001 | `tested-private` | Pending | v0.1.0 |
| 100059 | Windows System event 7045 | 12 | T1543.003 | `tested-private` | Pending | v0.1.0 |
| 100100 | SSH alert plus MISP result | 12 | Context only | `tested-private` | Pending integration audit | v0.2.0 |

Every published detection must document prerequisites, expected decoder/rule/level, positive and negative cases, important fields, false positives, tuning, investigation, response, cleanup, supported Wazuh version, and evidence state.
