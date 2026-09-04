# Detection engineering

The manifest tracks all ten laboratory capabilities. The XML directories remain intentionally empty until exact source files and dependencies are exported from the lab and audited. Prose descriptions are not sufficient to reconstruct a rule safely.

## Publication gate per rule

1. Export exact XML and record its SHA-256 digest.
2. Check provenance and remove secrets or private identifiers.
3. Validate XML and referenced parent rules/groups/decoders.
4. Add minimized positive and negative fixtures.
5. Add expected decoder, rule ID, level, and important fields.
6. Run `wazuh-logtest` on Wazuh 4.8.2 and record the command/result.
7. Run static repository validation.
8. Change to `reproduced-public` only after the public test succeeds.

Legacy rules `99901`–`99920` are excluded because their CDB dependencies are unresolved.
