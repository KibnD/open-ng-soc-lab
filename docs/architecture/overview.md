# Architecture overview

Open NG-SOC Lab is an isolated VMware Workstation Pro 17 environment. pfSense segments the laboratory and Suricata generates network telemetry. Three Wazuh agents cover Windows and Ubuntu systems. Wazuh Manager and Filebeat process events; Wazuh Indexer stores them; Wazuh Dashboard supports analysis. MISP, Shuffle, and Slack form the tested-private enrichment and notification path.

The confirmed detection baseline is Wazuh 4.8.2. Example deployments should use documentation addresses and `.example` names rather than copying the private lab topology.

## Trust boundaries

1. **External/WAN to lab:** controlled by pfSense; no public service exposure is required.
2. **Endpoint to detection core:** authenticated Wazuh agent channel.
3. **Network sensor to manager:** UDP/514 in the lab; unencrypted and explicitly non-production.
4. **Detection storage:** Filebeat to Wazuh Indexer over TLS/9200.
5. **Detection to SOAR:** lab HTTP endpoint; must use TLS for any non-isolated deployment.
6. **SOAR to CTI and notification:** credentials are secrets and must never enter Git.

See [data flows](data-flows.md) and [trust boundaries](trust-boundaries.md).
