# Runbook — Suspicious PowerShell

Triage the full event 4104 script block, user, host, parent/child processes, command line, downloads, encoded content, and signing context. Collect relevant PowerShell, Security, process, network, and file evidence. Legitimate automation may use `IEX`; scope exceptions to reviewed contexts.

Escalate for obfuscation, download/execute behavior, unexpected identity, persistence, or correlated alerts. Reversible response includes isolating the host, stopping the process, and disabling a compromised account with authorization. Verify process termination, persistence removal, telemetry continuity, and restored function.
