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
    'CITATION.cff',
    'LICENSE-PENDING.md',
    '.gitattributes',
    '.gitignore',
    'detections\tests\manifest.yml',
    'docs\detections\coverage-matrix.md'
)

foreach ($relative in $required) {
    if (-not (Test-Path -LiteralPath (Join-Path $root $relative) -PathType Leaf)) {
        $failures.Add("missing required file: $relative")
    }
}

$manifestPath = Join-Path $root 'detections\tests\manifest.yml'
if (Test-Path -LiteralPath $manifestPath -PathType Leaf) {
    try {
        $manifest = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
        $ids = @($manifest.detections.rule_id)
        if (@($ids | Sort-Object -Unique).Count -ne $ids.Count) {
            $failures.Add('manifest contains duplicate rule IDs')
        }
        $fields = @('rule_id','title','release','evidence_status','fixture_status','expected_level','mitre')
        foreach ($detection in $manifest.detections) {
            foreach ($field in $fields) {
                if ($detection.PSObject.Properties.Name -notcontains $field) {
                    $failures.Add("rule $($detection.rule_id) missing field: $field")
                }
            }
        }
    }
    catch {
        $failures.Add("manifest is not valid JSON-compatible YAML: $($_.Exception.Message)")
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
    if ($file.FullName -match '\\.git\\') { continue }
    if ($forbidden -contains $file.Extension.ToLowerInvariant()) {
        $failures.Add("forbidden artifact type: $($file.FullName.Substring($root.Length + 1))")
        continue
    }
    $content = [System.IO.File]::ReadAllText($file.FullName)
    foreach ($entry in $patterns.GetEnumerator()) {
        if ([regex]::IsMatch($content, $entry.Value)) {
            $failures.Add("possible $($entry.Key) in $($file.FullName.Substring($root.Length + 1))")
        }
    }
}

if ($failures.Count -gt 0) {
    Write-Host 'Repository validation failed:'
    foreach ($failure in $failures) { Write-Host "- $failure" }
    exit 1
}

Write-Host 'Repository validation passed.'
Write-Host 'Note: this check does not replace credential rotation or a dedicated secret scanner.'
