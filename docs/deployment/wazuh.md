# Wazuh deployment

## Supported baseline

The only confirmed version is Wazuh 4.8.2 with Manager, Indexer, Dashboard, and Filebeat on the detection-core host. Broader compatibility is `target`, not implied.

Follow the official Wazuh installation documentation for the chosen platform. This repository does not mirror upstream packages or installation scripts.

## Required flows

| Source | Destination | Port | Purpose |
|---|---|---:|---|
| Wazuh agents | Manager | TCP/1514 | Agent events |
| Enrollment clients | Manager | TCP/1515 when enabled | Agent registration |
| Filebeat/Manager | Indexer | TCP/9200 with TLS | Alert indexing |
| Dashboard | Manager API | TCP/55000 with TLS | Management API |
| Browser | Dashboard | TCP/443 or chosen HTTPS port | Analyst interface |

Restrict all management paths to the lab network. Validate certificates rather than disabling verification.

## Health checks

```sh
sudo /var/ossec/bin/wazuh-control status
sudo /var/ossec/bin/agent_control -lc
sudo /var/ossec/bin/wazuh-analysisd -t
sudo systemctl --no-pager --full status wazuh-manager filebeat
curl --fail --silent --show-error --cacert /PATH/TO/ca.pem https://indexer.example:9200/
```

An unauthenticated Indexer `401` can prove TLS reachability, but not application health or authorization. Confirm fresh event timestamps in archives/alerts and recent searchable documents.

## Backup and rollback

Back up configuration, custom rules/decoders, certificates, keystore material, and Indexer snapshots separately. Never commit backups. Before changing a rule, keep a private timestamped copy, run `wazuh-analysisd -t`, then restart only the required service. Restore the known-good file if validation fails.

## Removal

Use the official package removal procedure for the installed version. Revoke agent keys, remove stored secrets, and delete test indexes/volumes only after confirming the exact lab target and retaining required private evidence.
