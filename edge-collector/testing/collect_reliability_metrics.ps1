$ErrorActionPreference = 'Stop'
Set-Location "c:/GitHubProjects/autonomous-bas-auditor"

$keyPath = "c:/GitHubProjects/autonomous-bas-auditor/.private/lightSail05May.pem"
$remoteCount = ssh -o BatchMode=yes -o IdentitiesOnly=yes -i $keyPath ubuntu@50.19.79.71 "ls -1 ~/autonomous-bas-auditor/data/raw_payloads | wc -l"
$remoteCount = $remoteCount.Trim()

$metaLogPath = "edge-collector/testing/reliability_run.log"
$stdoutLogPath = "edge-collector/testing/reliability_stdout.log"
$stderrLogPath = "edge-collector/testing/reliability_stderr.log"
$pidPath = "edge-collector/testing/reliability_run.pid"

$collectorPid = ""
$isRunning = $false
if (Test-Path $pidPath) {
    $collectorPid = (Get-Content $pidPath -Raw).Trim()
    if ($collectorPid) {
        $proc = Get-Process -Id $collectorPid -ErrorAction SilentlyContinue
        if ($proc) {
            $isRunning = $true
        }
    }
}

$successCount = 0
$failureCount = 0
if (Test-Path $stdoutLogPath) {
    $successCount = (Select-String -Path $stdoutLogPath -Pattern "POST succeeded" | Measure-Object).Count
    $failureCount += (Select-String -Path $stdoutLogPath -Pattern "POST failed|POST exception|Queued payload" | Measure-Object).Count
}
if (Test-Path $stderrLogPath) {
    $failureCount += (Select-String -Path $stderrLogPath -Pattern ".+" | Measure-Object).Count
}

$spoolCount = 0
if (Test-Path "edge-collector/spool/reliability") {
    $spoolCount = (Get-ChildItem "edge-collector/spool/reliability" -Filter *.json -ErrorAction SilentlyContinue | Measure-Object).Count
}

Write-Output "remote_payload_count=$remoteCount"
Write-Output "collector_pid=$collectorPid"
Write-Output "collector_running=$isRunning"
Write-Output "collector_success_count=$successCount"
Write-Output "collector_failure_signals=$failureCount"
Write-Output "local_spool_count=$spoolCount"
