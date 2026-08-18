# Contributing

Contributions are not yet open while ownership, licensing, and the first reproducible detection pack are under review.

When contribution opens, every detection change must include:

- a clear rule purpose and data-source prerequisite;
- an accurate MITRE ATT&CK mapping or an explicit rationale for no mapping;
- sanitized positive and meaningful negative fixtures;
- expected decoder, rule ID, level, and supported Wazuh version;
- false-positive, tuning, investigation, response, and cleanup notes;
- provenance and license information;
- no secrets, private identifiers, raw operational evidence, or unsafe payloads.

Run `pwsh scripts/validate_repository.ps1` before requesting review. A dependency-free Python equivalent is also provided for environments with Python 3.
