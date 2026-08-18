# Open NG-SOC Lab

Open NG-SOC Lab is an educational, evidence-driven blueprint for building and validating an open detection-and-response laboratory with Wazuh and complementary open-source components.

## Current status

**Local development staging — not released and not production-ready.**

The initial target is a reproducible Wazuh detection pack backed by sanitized positive and negative fixtures. Integrations with MISP, Shuffle, Slack, dashboards, and Purple Team validation are later milestones and must not be represented as complete in this staging repository.

## Design principles

- Reproducible tests over screenshots.
- Honest evidence states: `planned`, `pending-export`, `tested-private`, or `reproduced-public`.
- Synthetic identities and documentation networks only.
- Safe, isolated, authorized simulations with cleanup and rollback.
- No credentials, private topology, company material, raw operational evidence, or third-party feed data.
- No production-readiness claim.

## Planned v0.1.0 scope

- Generic architecture and threat model.
- Wazuh rules `100052`–`100056` if each passes sanitized positive and negative tests.
- Optional Suricata rule `100051` if decoder provenance and deterministic fixtures pass review.
- Synthetic CloudTrail telemetry only; no claim of real AWS ingestion.
- Detection coverage matrix and machine-readable test manifest.
- Local repository validation and later pinned CI.

## Repository map

- `detections/wazuh/`: original rules and decoders after export and review.
- `detections/tests/`: sanitized fixtures, expected results, and manifest.
- `docs/`: architecture, threat model, deployment, detections, runbooks, and case studies.
- `integrations/`: later sanitized MISP, Shuffle, and Slack material.
- `simulations/`: safe synthetic validation procedures.
- `scripts/`: local validation tooling.

## Safety boundary

Use this project only in systems you own or are explicitly authorized to test. Do not use examples against production environments. Review every simulation, prerequisite, stop condition, and cleanup step before execution.

## Licensing

Licensing and ownership review is still pending. See `LICENSE-PENDING.md`. Until a final license is added, this staging content is not offered for redistribution.

## Evidence policy

Private internship reports, screenshots, raw logs, VM exports, and operational histories are not part of this repository. Public evidence will consist of minimized sanitized fixtures, deterministic assertions, and clean-environment reproduction records.
