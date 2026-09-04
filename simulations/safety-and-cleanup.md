# Simulation safety and cleanup

Before execution, record owner authorization, exact hosts, time window, operator, expected telemetry, stop conditions, and rollback. Take configuration backups to private encrypted storage; snapshots are not public artifacts.

Stop immediately for unexpected routing, production connectivity, unavailable monitoring, resource exhaustion, unintended privilege, persistent process, data loss, or an unplanned target. Do not improvise offensive actions.

After execution, remove disposable accounts/groups/SPNs/services/containers/webhooks/IOCs/files, restore configuration, confirm Wazuh/endpoint/CTI/SOAR health, generate a fresh benign marker, verify expected business function, and record only minimized sanitized evidence. PT-05 uses synthetic telemetry instead of clearing logs.
