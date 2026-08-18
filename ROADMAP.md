# Roadmap

## v0.1.0 — Architecture and tested Wazuh detection pack

- Export and sanitize candidate rules and parent dependencies.
- Build positive and negative fixtures with expected decoder, rule, and level.
- Reproduce tests on Wazuh 4.8.2 in a clean environment.
- Complete ownership, licensing, provenance, and security gates.

## v0.2.0 — MISP enrichment

- Publish a sanitized, configurable integration only after credential rotation and security review.
- Add synthetic MISP responses and deterministic error-path tests.

## v0.3.0 — Shuffle and Slack response

- Rebuild a workflow template without authentication objects or identifiers.
- Add a synthetic Wazuh webhook payload and generic Slack message template.

## v0.4.0 — Expanded coverage and dashboards

- Add additional network, identity, cloud, and container detections.
- Add sanitized dashboards validated against synthetic data.

## v1.0.0 — Purple Team validated

- Release only after an authorized controlled campaign is executed, evidenced, reviewed, and documented honestly.
