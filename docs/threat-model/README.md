# Threat model

## Scope and assets

The model covers an isolated educational NG-SOC laboratory and its public repository. Assets include rule/fixture integrity, telemetry confidentiality and authenticity, detection availability, integration credentials, workflow authenticity, analyst access, evidence integrity, and truthful project claims.

## Trust assumptions

- Simulations run only inside an owned or explicitly authorized isolated lab.
- Synthetic identities, `.example` names, and documentation networks replace private values.
- Secrets stay outside Git and rotate after suspected exposure.
- Positive and negative evidence is required before public reproduction claims.
- Administrators can access hypervisor and guest consoles; compromise of that plane can invalidate evidence.

## Threats and controls

| Threat | Consequence | Current control | Residual limitation |
|---|---|---|---|
| Secret leakage in code/history/screenshots | Account or workflow compromise | Environment variables, ignore rules, validators, Gitleaks, manual review | INC-006 rotation remains open |
| Forged or lost telemetry | False conclusions or missed detection | Tagged fresh events, source correlation, health checks | UDP Syslog lacks integrity/confidentiality |
| Detection evasion/noise | Missed activity or analyst overload | Negative fixtures, documented tuning, signature context | Public Wazuh tests pending |
| Unsafe simulation | Damage or scope escape | Isolated lab, stop conditions, rollback, non-destructive substitutes | Human execution error remains possible |
| CI/supply-chain compromise | Malicious repository changes | Read-only permissions, SHA-pinned actions, checksum-pinned tool | Hosted runner and upstream trust remain |
| CTI false positive/outage | Incorrect automated decision | Explicit no-match/error paths; analyst review | Feed quality varies; no automated blocking |
| Unsupported claims | Misleading users | Controlled evidence states and manifest | Private evidence is not independently public |

## Out of scope

Production hardening, high availability, real organizational AWS ingestion, automated destructive response, and adversarial hypervisor defense are excluded. Purple Team scenarios PT-01/02/03/04/06 passed privately; public reproduction remains incomplete. PT-05 was not run because live log clearing is destructive.
