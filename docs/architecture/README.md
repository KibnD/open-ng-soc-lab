# Architecture

The public architecture will describe generic trust zones and data flows without reproducing the private laboratory topology.

```text
Telemetry sources
  -> collection and normalization
  -> Wazuh detection and indexing
  -> analyst investigation
  -> optional CTI enrichment
  -> optional SOAR notification/response
```

## Trust boundaries

- Monitored endpoints and workloads.
- Network security sensors and gateway.
- Detection/indexing platform.
- CTI and automation platform.
- Analyst and administration interfaces.
- External notification/API boundary.

Exact deployment guidance remains pending clean-room reconstruction and validation.
