# Slack notification template

The Block Kit-compatible JSON contains no token, webhook, workspace, or channel identifier. Configure the destination and OAuth authentication inside Shuffle's secret/authentication mechanism.

Treat template values as untrusted text. Before implementation, ensure the Shuffle Slack app safely escapes interpolated values and restrict lengths using the Wazuh payload schema. A notification is an analyst prompt, not authorization for automated containment.
