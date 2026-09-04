## Summary

Describe the change and why it is needed.

## Evidence

- [ ] Positive fixture and expected result added or updated.
- [ ] Meaningful negative fixture and expected result added or updated.
- [ ] Clean-environment or supported-version result recorded.

## Safety and privacy

- [ ] No secrets, private identifiers, company material, or raw operational evidence.
- [ ] Simulation scope, cleanup, and rollback are documented.
- [ ] Third-party provenance and licensing were reviewed.

## Validation

- [ ] `python scripts/validate_repository.py` passes.
- [ ] `python -m unittest discover -s tests -v` passes.
- [ ] `pwsh -File scripts/validate_repository.ps1` passes.
- [ ] Claims and MITRE mappings match the evidence.

## Release impact

- Evidence-state changes:
- Compatibility or breaking changes:
- Human decisions or lab verification still required:
