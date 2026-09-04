# Active Directory identity tests

Use a disposable disabled account in a dedicated lab domain. Confirm auditing and rollback commands before beginning.

- Rule 100054: add the disabled account briefly to Domain Admins, confirm event 4728, remove it immediately, and confirm event 4729.
- Rule 100055: use a controlled service account/SPN to request an RC4 ticket; compare with AES; remove temporary state afterward.
- Rule 100057: generate only the minimum five failed network logons within 120 seconds against a disposable account; stop before lockout unless lockout is explicitly planned.

Stop for an unexpected account, group, host, successful authentication, replication scope, or failure to remove test state. Verify membership, SPNs, credentials, sessions, account state, and normal authentication during cleanup.
