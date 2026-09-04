# Data flows

| Flow | Source | Destination | Lab transport | Security note |
|---|---|---|---|---|
| Endpoint telemetry | Wazuh agents | Wazuh Manager | TCP/1514 | Wazuh agent encryption |
| Network telemetry | pfSense/Suricata | Wazuh Manager | UDP/514 | Unencrypted; isolated-lab limitation |
| Alert indexing | Filebeat | Wazuh Indexer | TLS/9200 | Validate CA trust and certificate names |
| Analyst access | Browser | Wazuh Dashboard | HTTPS | Keep management access restricted |
| Alert orchestration | Wazuh | Shuffle frontend/webhook | HTTP/3001 in lab | Use HTTPS when leaving an isolated lab |
| CTI query | Shuffle | MISP | HTTPS/443 | Verify TLS; API key from secret storage |
| Notification | Shuffle | Slack API | HTTPS/443 | OAuth token and channel identifiers are secrets |
| Cloud simulation | Synthetic file | Wazuh localfile | Local file | No real AWS ingestion claim |

Shuffle backend port `5001` is internal. Port `3443` applies only when HTTPS is explicitly configured; neither `3001` nor `3443` is presented as a universal backend port.
