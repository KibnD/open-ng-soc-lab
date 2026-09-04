# Versioning policy

The project intends to use Semantic Versioning after the first authorized release. Before then, files may use `0.1.0-dev`; this is not a release.

- Patch: documentation corrections, safe test improvements, and compatible detection tuning without changing intended semantics.
- Minor: new compatible detections, integrations, simulations, or documented capabilities.
- Major: incompatible configuration, fixture, manifest, integration-contract, or rule-behavior changes.

Detection rule IDs are stable identifiers, not package versions. A materially different detection should normally receive a new ID rather than silently redefining an existing one. Every release updates the changelog, citation metadata, manifest version, compatibility table, release notes, and artifact checksums where applicable.

No version may be tagged while ownership/licensing, credential rotation, secret/history audit, required tests, or provenance review is incomplete.
