# Deployment prerequisites

## Confirmed laboratory baseline

- VMware Workstation Pro 17
- Wazuh 4.8.2
- Windows Server 2025 with AD DS/DNS
- Windows 10 and Ubuntu guests
- pfSense and Suricata
- Docker and MongoDB
- MISP, Shuffle, and Slack

## Capacity planning

Size the Wazuh all-in-one host and MISP/Shuffle host conservatively, preserve free disk space for OpenSearch indexes and container volumes, and start infrastructure in dependency order: network, detection core, endpoints, then CTI/SOAR. Exact clean-environment sizing has not yet been reproduced publicly.

## Publication test prerequisites

- PowerShell 7 for the cross-platform repository validator, or Windows PowerShell 5.1 locally.
- Python 3.11+ for the Python validator and unit tests.
- A compatible Wazuh installation or future pinned container for optional `wazuh-logtest` integration tests.

There is currently no one-command installer. Follow component-specific guides only after their status is marked reproducible.
