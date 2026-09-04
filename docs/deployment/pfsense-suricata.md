# pfSense and Suricata deployment

Deploy pfSense as the isolated lab gateway, restrict its management interface, and enable Suricata only on intended interfaces. Select signatures based on the test objective; uncontrolled broad rulesets create noise and resource pressure.

The private lab forwards telemetry to Wazuh using UDP/514. This is unencrypted and acceptable only inside the isolated laboratory. Prefer authenticated TLS Syslog or a protected collector for any broader environment.

## Validation

1. Confirm the Wazuh Manager is fully healthy and listening before testing forwarding.
2. Send one uniquely tagged benign Syslog marker.
3. Verify its arrival in Wazuh archives; an undecoded marker proves transport only.
4. Replay a sanitized Suricata EVE fixture to validate the decoder separately.
5. Confirm a priority-1/2 positive and priority-3 negative for rule 100051.

After powered-off restarts, forwarding may require reloading pfSense `syslogd` after Wazuh becomes healthy. Do not treat a marker as proof of a detection match.

Export configuration backups only to private encrypted storage. Public examples must exclude interface identifiers, hashes, certificates, accounts, and private topology.
