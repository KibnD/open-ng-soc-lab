# Detection Coverage Matrix

Evidence state definitions:

- `tested-private`: validated in the private lab; public fixture/export pending.
- `pending-export`: source or dependency has not entered sanitized staging.
- `reproduced-public`: sanitized fixture passes the public test harness.

| Rule | Detection | Data source | MITRE ATT&CK | Private evidence | Public reproduction | v0.1.0 |
|---:|---|---|---|---|---|---|
| 100051 | High/medium-priority Suricata alert | Suricata EVE via pfSense Syslog | Signature-dependent; no universal mapping | Positive priority 1 and negative priority 3 | Pending decoder/fixture export | Optional |
| 100052 | Windows event-log clearing | Windows Security events | T1070.001 | Positive validated; XML mapping verified | Pending sanitized positive/negative fixtures | Candidate |
| 100053 | IAM access-key creation | Synthetic CloudTrail | T1098.001 | Positive synthetic event validated | Pending source and negative fixture export | Candidate |
| 100054 | Domain Admins membership addition | Windows event 4728 | T1098 | Positive, negative, rollback, fresh indexing | Pending sanitized fixtures | Candidate |
| 100055 | Successful RC4 service-ticket request heuristic | Windows event 4769 | T1558.003 | RC4 positive, AES negative, cleanup, fresh indexing | Pending sanitized fixtures | Candidate |
| 100056 | Privileged Docker launch through audited sudo | Linux audit/sudo command | T1611 | Privileged positive, standard negative, cleanup, fresh indexing | Pending sanitized fixtures | Candidate |
| 100100 | MISP match on suspicious SSH source | Wazuh alert plus MISP CTI | CTI context; no standalone behavioral mapping | End-to-end validated | Deferred to v0.2.0 | No |
