# Runbook — Kerberos RC4 ticket

Triage event 4769 status, encryption type, service account/SPN, requester, source, volume, and surrounding authentication. Approved legacy use is a major false positive.

Escalate unusual RC4 involving valuable accounts, high volume, enumeration, or endpoint compromise. Do not disable compatibility blindly. Coordinate isolation, credential rotation, and AES migration. Verify service authentication, AES issuance, no continued suspicious requests, and cleanup.
