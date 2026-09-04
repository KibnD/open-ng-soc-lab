# Infrastructure reference

This is a capacity-conscious multi-VM design, not infrastructure-as-code yet. Public automation will be added only after clean-environment testing.

## Documentation addressing plan

| Example host | Address | Role |
|---|---:|---|
| `gateway.lab.example` | `192.0.2.1` | pfSense and Suricata |
| `dc.lab.example` | `192.0.2.10` | AD DS and DNS |
| `client.lab.example` | `192.0.2.20` | Windows client |
| `wazuh.lab.example` | `192.0.2.30` | Wazuh all-in-one core |
| `app.lab.example` | `192.0.2.40` | Ubuntu, Docker, MongoDB |
| `soar.lab.example` | `192.0.2.50` | MISP and Shuffle |

These RFC 5737 addresses are documentation examples and must be replaced for deployment.

## Startup order

1. Start pfSense and confirm routing/DNS/time.
2. Start Wazuh Indexer, Manager/Filebeat, then Dashboard; wait for health.
3. Start endpoints and confirm all three Wazuh agents reconnect.
4. Start the CTI/SOAR host; verify persistent MISP services first, then Shuffle services/workers.
5. Test pfSense Syslog with a tagged marker after Wazuh is ready.
6. Check disk space, index freshness, container health, and clock synchronization before simulations.

## Backup, rollback, and capacity

Keep encrypted private backups of configuration, certificates, databases, Indexer snapshots, and workflow source. Do not use Git for secrets, VM snapshots, database volumes, or firewall backups. Take application-consistent backups and test restoration.

Constrained memory and disk can delay OpenSearch/MISP/Shuffle startup. Do not start a scenario until dependencies are healthy. Stop application workloads before infrastructure, and preserve required evidence before deleting test data. Exact minimum hardware remains unverified in a clean public deployment.
