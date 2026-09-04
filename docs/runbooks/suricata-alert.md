# Runbook — Suricata alert

## Triage and investigation

Confirm signature, priority, timestamp, interfaces, source/destination, action, and asset criticality. Correlate firewall, endpoint, DNS, and Wazuh evidence. Ask whether traffic was allowed and whether exploit evidence exists. Scanners, malformed benign traffic, and noisy signatures are common false positives.

## Escalation, response, and recovery

Escalate when the target is exposed, behavior is corroborated, or impact indicators exist. Prefer reversible source isolation or narrow blocking; do not block solely on a signature name. Remove temporary controls after review, verify expected traffic and sensor health, document tuning, and preserve minimized evidence.
