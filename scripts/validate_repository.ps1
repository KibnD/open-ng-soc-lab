[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$root = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
$failures = [System.Collections.Generic.List[string]]::new()

$required = @(
    'README.md',
    'CHANGELOG.md',
    'ROADMAP.md',
    'SECURITY.md',
    'CONTRIBUTING.md',
    'CODE_OF_CONDUCT.md',
    'SUPPORT.md',
    '.github\CODEOWNERS',
    '.github\REPOSITORY_SETTINGS.md',
    'CITATION.cff',
    'LICENSE-PENDING.md',
    '.gitattributes',
    '.gitignore',
    'README.fr.md',
    'REPOSITORY_STATUS.md',
    'detections\tests\manifest.json',
    'detections\tests\schema\manifest.schema.json',
    '.github\workflows\ci.yml',
    '.github\dependabot.yml',
    'docs\evidence\evidence-policy.md',
    'docs\LAB_EXPORT_CHECKLIST.md',
    'docs\deployment\wazuh.md',
    'docs\deployment\pfsense-suricata.md',
    'docs\deployment\misp.md',
    'docs\deployment\shuffle.md',
    'docs\troubleshooting\known-issues.md',
    'infrastructure\README.md',
    'integrations\misp\client.py',
    'integrations\misp\enrich.py',
    'integrations\misp\README.md',
    'tests\test_misp_client.py',
    'integrations\shuffle\workflow-blueprint.json',
    'integrations\shuffle\wazuh-alert.schema.json',
    'integrations\shuffle\README.md',
    'integrations\slack\message-template.json',
    'examples\payloads\wazuh-ssh-alert.json',
    'tests\test_shuffle_blueprint.py',
    'detections\wazuh\VERSION_SUPPORT.md',
    'docs\project\versioning.md',
    'docs\project\release-checklist.md',
    'docs\use-cases.md',
    'docs\assets\README.md',
    'dashboards\README.md',
    'simulations\safety-and-cleanup.md',
    'simulations\synthetic-cloudtrail.md',
    'simulations\ad-identity.md',
    'simulations\docker-privileged.md',
    'simulations\network-replay.md',
    'docs\case-studies\pt-01.md',
    'docs\case-studies\pt-02.md',
    'docs\case-studies\pt-03.md',
    'docs\case-studies\pt-04.md',
    'docs\case-studies\pt-05.md',
    'docs\case-studies\pt-06.md',
    'docs\detections\coverage-matrix.md'
)

foreach ($relative in $required) {
    if (-not (Test-Path -LiteralPath (Join-Path $root $relative) -PathType Leaf)) {
        $failures.Add("missing required file: $relative")
    }
}

$manifestPath = Join-Path $root 'detections\tests\manifest.json'
if (Test-Path -LiteralPath $manifestPath -PathType Leaf) {
    try {
        $manifest = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
        $ids = @($manifest.detections.rule_id)
        $requiredIds = @((100051..100059) + 100100)
        if (Compare-Object -ReferenceObject $requiredIds -DifferenceObject @($ids | Sort-Object)) {
            $failures.Add('manifest rule IDs must be exactly 100051-100059 and 100100')
        }
        if (@($ids | Sort-Object -Unique).Count -ne $ids.Count) {
            $failures.Add('manifest contains duplicate rule IDs')
        }
        $fields = @('rule_id','title','data_source','prerequisites','expected_decoder','expected_level','mitre','mitre_justification','evidence_status','positive_fixture','negative_fixture','expected_result','release_target','cleanup','limitations')
        $evidenceStates = @('implemented-private','tested-private','reproduced-public','documented-only','simulated','target')
        foreach ($detection in $manifest.detections) {
            $documentation = Join-Path $root "docs\detections\rule-$($detection.rule_id).md"
            if (-not (Test-Path -LiteralPath $documentation -PathType Leaf)) {
                $failures.Add("rule $($detection.rule_id) missing detection documentation")
            }
            foreach ($field in $fields) {
                if ($detection.PSObject.Properties.Name -notcontains $field) {
                    $failures.Add("rule $($detection.rule_id) missing field: $field")
                }
            }
            if ($evidenceStates -notcontains $detection.evidence_status) {
                $failures.Add("rule $($detection.rule_id) has invalid evidence status")
            }
            if ($detection.expected_level -lt 0 -or $detection.expected_level -gt 16) {
                $failures.Add("rule $($detection.rule_id) has invalid expected level")
            }
            foreach ($pathField in @('positive_fixture','negative_fixture','expected_result')) {
                $relative = $detection.$pathField
                if ($relative -and -not (Test-Path -LiteralPath (Join-Path $root $relative) -PathType Leaf)) {
                    $failures.Add("rule $($detection.rule_id) references missing ${pathField}: $relative")
                }
            }
        }
    }
    catch {
        $failures.Add("manifest is not valid JSON: $($_.Exception.Message)")
    }
}

$forbidden = @('.evtx','.pcap','.pcapng','.vmdk','.ova','.ovf','.iso','.p12','.pfx','.key','.pem','.dump')
$patterns = [ordered]@{
    'AWS access key' = 'AKIA[0-9A-Z]{16}'
    'Slack token' = 'xox[baprs]-[A-Za-z0-9-]+'
    'GitHub token' = 'gh[pousr]_[A-Za-z0-9]{20,}'
    'private key' = '-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'
}

foreach ($file in Get-ChildItem -LiteralPath $root -Recurse -File -Force) {
    if ($file.FullName -match '[\\/](?:\.git|__pycache__|\.pytest_cache)[\\/]') { continue }
    if ($forbidden -contains $file.Extension.ToLowerInvariant()) {
        $failures.Add("forbidden artifact type: $($file.FullName.Substring($root.Length + 1))")
        continue
    }
    if ($file.Extension -eq '.json') {
        try { Get-Content -LiteralPath $file.FullName -Raw | ConvertFrom-Json | Out-Null }
        catch { $failures.Add("invalid JSON in $($file.FullName.Substring($root.Length + 1)): $($_.Exception.Message)") }
    }
    $content = [System.IO.File]::ReadAllText($file.FullName)
    $bytes = [System.IO.File]::ReadAllBytes($file.FullName)
    if ($bytes.Length -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF) {
        $failures.Add("UTF-8 BOM is not allowed: $($file.FullName.Substring($root.Length + 1))")
    }
    for ($index = 0; $index -lt $bytes.Length - 1; $index++) {
        if ($bytes[$index] -eq 0x0D -and $bytes[$index + 1] -eq 0x0A) {
            $failures.Add("CRLF line endings are not allowed: $($file.FullName.Substring($root.Length + 1))")
            break
        }
    }
    foreach ($entry in $patterns.GetEnumerator()) {
        if ([regex]::IsMatch($content, $entry.Value)) {
            $failures.Add("possible $($entry.Key) in $($file.FullName.Substring($root.Length + 1))")
        }
    }
    if ($file.Extension -eq '.md') {
        foreach ($match in [regex]::Matches($content, '(?<!!)\[[^\]]+\]\(([^)]+)\)')) {
            $target = $match.Groups[1].Value.Trim()
            if ($target -match '^(#|https?://|mailto:)') { continue }
            $target = ($target -split '#', 2)[0].Trim('<>')
            if (-not $target) { continue }
            $decoded = [System.Uri]::UnescapeDataString($target)
            $resolved = Join-Path $file.DirectoryName $decoded
            if (-not (Test-Path -LiteralPath $resolved)) {
                $failures.Add("broken internal link in $($file.FullName.Substring($root.Length + 1)): $target")
            }
        }
    }
}

if ($failures.Count -gt 0) {
    Write-Host 'Repository validation failed:'
    foreach ($failure in $failures) { Write-Host "- $failure" }
    exit 1
}

Write-Host 'Repository validation passed.'
Write-Host 'Scope: static publication checks only; Wazuh was not executed.'
