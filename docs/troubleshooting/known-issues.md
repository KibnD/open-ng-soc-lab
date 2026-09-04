# Known issues

## Indexer and dashboard cold start

**Symptoms:** API/UI unavailable or stale search results immediately after a powered-off start. **Cause:** resource-constrained OpenSearch/Wazuh dependencies are not ready simultaneously. **Correction:** start in dependency order and wait for service health rather than repeatedly restarting the stack. **Validation:** authenticated API health plus a newly generated searchable event. **Prevention:** reserve disk/RAM and document boot checks.

## pfSense Syslog unavailable after restart

**Symptoms:** a local pfSense marker exists but UDP/514 traffic does not reach Wazuh; pfSense reports `sendto: Connection refused`. **Supported cause:** forwarding initialization/timing while Wazuh was still starting. **Correction:** after Wazuh is healthy and listening, restart only pfSense `syslogd`, then send a fresh marker. **Validation:** marker appears in Wazuh archives. An undecoded marker proves transport, not detection. **Prevention:** perform this check after every cold start.

## Historical data does not prove current health

Old dashboard documents can remain visible when ingestion is stopped. Validate a uniquely tagged fresh event, its archive timestamp, alert processing where expected, and Indexer searchability. Use UTC consistently when comparing host and dashboard times.

## Suricata noise and signature semantics

Priority alone does not identify a technique. Review the originating signature and tune narrowly. A contained request that does not create a Suricata event is not a failed downstream decoder test; use a controlled sanitized replay to isolate the pipeline stage.

## Shuffle/MISP resource pressure

Low disk space and container startup dependencies can leave frontends reachable while workers are not ready. Check persistent containers, health checks, Swarm replica counts, MISP/API response, OpenSearch response, and free disk space. Treat idempotency warnings for already-existing services/policies separately from genuine health failures.

## Docker network overlap

Container networks can overlap VMware or lab subnets and cause ambiguous routing. Inventory host, VMware, pfSense, Docker bridge, and overlay ranges before deployment. Choose non-overlapping ranges, then recreate only the specifically affected disposable network after verifying attached workloads.

## Legacy rules 99901–99920

These rules depend on unresolved CDB lists. They are excluded from publication and must not be enabled until dependencies are repaired or removed and positive/negative tests pass.
