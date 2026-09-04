# Synthetic CloudTrail CreateAccessKey

**Prerequisites:** isolated Wazuh 4.8.2 test manager, JSON `localfile` input, audited rule 100053, and synthetic fixtures. No AWS credentials or network access are needed.

Feed a minimized synthetic `CreateAccessKey` record into the designated test file. The positive must decode as JSON and reach rule 100053 level 12; a comparable read-only event must not. Stop if the input path could consume real organizational logs.

Delete the synthetic file/entry, restore the previous `localfile` configuration if changed, validate Wazuh health, and retain expected output without account identifiers. This does not test AWS, GuardDuty, or `wazuh-aws`.
