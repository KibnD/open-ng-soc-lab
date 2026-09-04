# Network and SSH telemetry replay

Use minimized synthetic log lines, not packets or live exploitation. Confirm Wazuh and pfSense transport separately with a tagged benign marker.

- Rule 100051: replay priority-1/2 Suricata-format telemetry; use priority 3 as a negative case.
- Rule 100100: replay one synthetic `sshd` event using TEST-NET address `198.51.100.42`, query only a synthetic MISP IOC, and exercise Shuffle match/no-match/error paths.

Stop if traffic leaves the lab, a real IOC/feed is queried unintentionally, or a notification reaches a non-test destination. Remove the synthetic IOC and disposable webhook, verify forwarding and worker health, and do not interpret a transport marker as a detection match.
