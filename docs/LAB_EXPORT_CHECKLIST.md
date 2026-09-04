# Lab export checklist

Run this checklist only after the lab is powered on and healthy. Store raw exports in the private archive first; do not copy them directly into the public repository.

## Wazuh manager

```sh
sudo /var/ossec/bin/wazuh-control info
sudo /var/ossec/bin/wazuh-analysisd -t
sudo sha256sum /var/ossec/etc/rules/local_rules.xml
sudo sha256sum /var/ossec/etc/decoders/local_decoder.xml
sudo install -m 0600 /var/ossec/etc/rules/local_rules.xml /PRIVATE_EXPORT/ng_soc_local_rules.xml
sudo install -m 0600 /var/ossec/etc/decoders/local_decoder.xml /PRIVATE_EXPORT/ng_soc_local_decoder.xml
```

Confirm rules `100051`–`100059` and `100100` from the exported copy. Do not print the full files into a shared terminal transcript. Record every referenced parent rule, group, list, and decoder. Run one sanitized positive and negative event per rule through `/var/ossec/bin/wazuh-logtest`; rule `100057` needs five correlated events inside 120 seconds.

## MISP integration

```sh
sudo sha256sum /var/ossec/integrations/custom-misp*
sudo stat /var/ossec/integrations/custom-misp*
```

Copy the script only to the private export area. Before public adaptation, inspect for API keys, URLs, `verify=False`, missing timeouts, unsafe queue writes, and secret-bearing logs. Rotate/revoke the historic MISP and Shuffle credentials under INC-006 before any release.

## Shuffle

Export a duplicate workflow created for publication—not the operational workflow. Remove authentication objects, webhook and channel IDs, tokens, execution history, private hostnames, and personal names. Confirm generic match, no-match, and error branches. Record the Shuffle version and import steps.

## Evidence and screenshots

Select only evidence that proves a documented behavior. Redact tokens, identifiers, names, timestamps when unnecessary, and private topology; remove image metadata; verify provenance; retain originals privately. Never export raw indexes, VM disks, snapshots, Windows ISOs, malware, third-party feeds, or unsafe PCAPs.

## Return package

- Exact Wazuh version output.
- Audited XML candidates and SHA-256 values.
- Dependency inventory.
- Sanitized positive/negative fixtures and expected `wazuh-logtest` output.
- Audited MISP script candidate and testable contract.
- Sanitized Shuffle template.
- Credential-rotation confirmation without secret values.
