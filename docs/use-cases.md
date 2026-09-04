# Use cases

| Use case | Detection path | Current evidence |
|---|---|---|
| Prioritize network IDS alerts | Suricata → pfSense Syslog → Wazuh 100051 | `tested-private` |
| Detect anti-forensics | Windows logs → Wazuh 100052 | `tested-private`; PT-05 not run |
| Monitor synthetic cloud credential creation | Local CloudTrail JSON → Wazuh 100053 | `simulated` |
| Detect privileged identity change | Event 4728 → Wazuh 100054 | `tested-private` |
| Identify RC4 ticket heuristic | Event 4769 → Wazuh 100055 | `tested-private` |
| Detect risky container launch | sudo/audit → Wazuh 100056 | `tested-private` |
| Correlate failed logons | Event 4625 sequence → Wazuh 100057 | `tested-private` |
| Review suspicious PowerShell | Event 4104 → Wazuh 100058 | `tested-private` |
| Identify shell-based services | Event 7045 → Wazuh 100059 | `tested-private` |
| Add CTI context to SSH alerts | Wazuh → Shuffle → MISP → Slack / 100100 | `tested-private` |

The repository is useful for architecture study, detection specification, publication safety, and future controlled reproduction. It is not a managed SOC service or production deployment guide.
