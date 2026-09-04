# Deployment

The deployment guides describe the confirmed private-lab design and safe reconstruction requirements. They are not a one-command installer and have not yet been reproduced from a clean public environment.

1. Review [prerequisites](prerequisites.md) and allocate resources.
2. Build the isolated network and firewall boundaries.
3. Deploy and validate [Wazuh](wazuh.md).
4. Configure [pfSense and Suricata](pfsense-suricata.md).
5. Add endpoint agents and telemetry sources.
6. Deploy [MISP](misp.md), then [Shuffle](shuffle.md), only after the detection core is healthy.
7. Execute health checks before controlled simulations.

Use unique credentials and trusted certificates. Never copy credentials, host identities, or backups from the private laboratory.
