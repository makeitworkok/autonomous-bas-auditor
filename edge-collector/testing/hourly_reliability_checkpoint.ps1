$ErrorActionPreference = 'Stop'
Set-Location "c:/GitHubProjects/autonomous-bas-auditor"

$metricsOutput = powershell -ExecutionPolicy Bypass -File "c:/GitHubProjects/autonomous-bas-auditor/edge-collector/testing/collect_reliability_metrics.ps1"
$timestamp = Get-Date -Format o

$pairs = @{}
foreach ($line in $metricsOutput) {
    if ($line -match "=") {
        $parts = $line -split "=", 2
        if ($parts.Count -eq 2) {
            $pairs[$parts[0]] = $parts[1]
        }
    }
}

$logPath = "c:/GitHubProjects/autonomous-bas-auditor/edge-collector/testing/reliability_hourly.log"
$record = [PSCustomObject]@{
    timestamp = $timestamp
    remote_payload_count = $pairs['remote_payload_count']
    collector_pid = $pairs['collector_pid']
    collector_running = $pairs['collector_running']
    collector_success_count = $pairs['collector_success_count']
    collector_failure_signals = $pairs['collector_failure_signals']
    local_spool_count = $pairs['local_spool_count']
}

$line = ($record | ConvertTo-Json -Compress)
Add-Content -Path $logPath -Value $line
Write-Output $line
