# Contributing

Contributions are welcome for review, but cannot be accepted for release until project ownership and licensing are resolved. By submitting material, you confirm you have the right to contribute it and understand that final licensing is pending.

## Development setup

1. Fork and clone the repository.
2. Create a focused branch from `main`.
3. Use Python 3.11+ and PowerShell 7 where available.
4. Keep credentials in an ignored local environment file; never edit `.env.example` with real values.
5. Run:

```text
python scripts/validate_repository.py
python -m unittest discover -s tests -v
pwsh -File scripts/validate_repository.ps1
```

## Detection changes

Every detection must include purpose, source and prerequisites; accurate ATT&CK justification or explicit no-mapping rationale; tested Wazuh version; positive and meaningful negative fixtures; expected decoder/rule/level/fields; false positives and tuning; investigation and reversible response; cleanup; evidence status; and provenance.

Do not mark `reproduced-public` until the public fixtures pass the documented Wazuh integration test. Static XML validation is not Wazuh execution. Rule IDs require maintainer coordination. Rules `99901`–`99920` are reserved from publication while their dependencies are unresolved.

## Pull requests

Keep changes small and explain behavior, risk, evidence, and limitations. Complete the pull-request template. CI must pass and review discussions must be resolved. Maintainers may request a safer fixture or narrower claim.

Never submit credentials, authentication objects, personal data, company material, raw operational evidence, live indicators, malware, weaponized exploits, unsafe PCAPs, VM disks, snapshots, ISOs, database/index dumps, or third-party feeds without clear rights.

## Commit and release conventions

Use concise imperative commit messages, optionally with Conventional Commit types such as `docs:`, `test:`, `feat:`, or `fix:`. Maintainers manage versions and releases according to [the version policy](docs/project/versioning.md). Contributor pull requests must not add release tags or silently change evidence states.

## Reporting problems

Use issue templates for nonsensitive defects and detection proposals. Follow [SECURITY.md](SECURITY.md) for vulnerabilities or accidental secret exposure.
