# Threat Model

## Assets

- Detection rules, decoders, and test integrity.
- Telemetry confidentiality and authenticity.
- Wazuh manager/indexer availability.
- Integration credentials and workflow authenticity.
- Analyst access and evidence integrity.

## Threats considered

- Credential disclosure through configuration, logs, screenshots, fixtures, or Git history.
- Telemetry tampering, spoofing, loss, or indexing gaps.
- Excessive false positives hiding meaningful alerts.
- Unsafe simulations escaping the isolated lab.
- Dependency or CI compromise.
- Misleading mappings or unsupported capability claims.

## Assumptions

- Tests run only in an isolated, authorized environment.
- Synthetic identities and documentation networks replace private values.
- Secrets remain outside Git and are rotated after suspected exposure.
- A detection is not accepted without positive and negative evidence.

## Out of scope for v0.1.0

- Production hardening or availability guarantees.
- Real organization AWS ingestion.
- Automated containment actions.
- Completed Purple Team validation.
