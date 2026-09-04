# Release checklist

## Ownership and security

- [ ] Internship/company ownership and name/logo permissions confirmed in writing.
- [ ] Final license texts and SPDX identifiers reviewed.
- [ ] Third-party provenance complete.
- [ ] INC-006 credentials rotated/revoked and integrations retested.
- [ ] Current tree and complete Git history pass a dedicated secret scan.
- [ ] Screenshots pass visual, metadata, privacy, and rights review.

## Reproducibility

- [ ] Exact rules, decoders, and dependencies audited.
- [ ] Every released rule has positive/negative fixtures and expected results.
- [ ] Static validators and their unit tests pass.
- [ ] Wazuh integration tests pass on every claimed version.
- [ ] MISP and Shuffle artifacts pass authorized interoperability/import tests.
- [ ] Deployment steps are reproduced from a clean environment.

## Repository and GitHub

- [ ] CI is green on the release commit.
- [ ] Branch rules and security features are enabled and verified.
- [ ] README claims, evidence states, limitations, changelog, citation, and support table agree.
- [ ] Release notes and checksums are prepared.
- [ ] Tag is signed or otherwise verifiable according to maintainer policy.

Stop the release when any applicable item is incomplete. Do not interpret public visibility as release authorization.
