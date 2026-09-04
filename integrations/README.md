# Integrations

The repository contains a new clean-room MISP lookup adapter with synthetic tests. It is not an export of the private integration and remains pre-release until the test suite and authorized interoperability test pass.

- MISP private-script export: deferred pending credential rotation and source review.
- Shuffle/Slack: a sanitized manual-build blueprint, payload schema, synthetic alert, and generic Slack message are present. A directly importable export remains deferred until disposable-instance testing proves portability.

No live `.env`, API response, workflow export, authentication object, or secret belongs in this repository.

See [`misp/README.md`](misp/README.md) for the safe public adapter. The original alert must remain available when enrichment times out or fails; an error must never be converted into an IOC match.
