$ErrorActionPreference = 'Stop'
Set-Location "c:/GitHubProjects/autonomous-bas-auditor"

$keyPath = "c:/GitHubProjects/autonomous-bas-auditor/.private/lightSail05May.pem"
$token = ssh -o BatchMode=yes -o IdentitiesOnly=yes -i $keyPath ubuntu@50.19.79.71 "sudo cat /etc/autonomous-bas-auditor/api.env | cut -d= -f2"
$token = $token.Trim()

if (-not $token) {
    throw "Failed to retrieve BAS_AUDITOR_API_TOKEN from Lightsail."
}

# Prevent parallel runs that would corrupt reliability metrics.
Get-CimInstance Win32_Process |
    Where-Object { $_.Name -eq 'python.exe' -and $_.CommandLine -match 'edge-collector/run_collector.py --max-cycles 2880' } |
    ForEach-Object { Stop-Process -Id $_.ProcessId -Force }

$env:EDGE_COLLECTOR_CONFIG = "edge-collector/testing/reliability_config.json"
$env:EDGE_COLLECTOR_BEARER_TOKEN = $token

$outLog = "c:/GitHubProjects/autonomous-bas-auditor/edge-collector/testing/reliability_stdout.log"
$errLog = "c:/GitHubProjects/autonomous-bas-auditor/edge-collector/testing/reliability_stderr.log"
$metaLog = "c:/GitHubProjects/autonomous-bas-auditor/edge-collector/testing/reliability_run.log"
$pidFile = "c:/GitHubProjects/autonomous-bas-auditor/edge-collector/testing/reliability_run.pid"

foreach ($f in @($outLog, $errLog, $metaLog, $pidFile)) {
    if (Test-Path $f) {
        Remove-Item $f -Force
    }
}

$process = Start-Process -FilePath "c:/GitHubProjects/autonomous-bas-auditor/.venv-1/Scripts/python.exe" `
    -ArgumentList "edge-collector/run_collector.py --max-cycles 2880" `
    -WorkingDirectory "c:/GitHubProjects/autonomous-bas-auditor" `
    -RedirectStandardOutput $outLog `
    -RedirectStandardError $errLog `
    -PassThru

$process.Id | Out-File -FilePath $pidFile -Encoding ascii

"Starting reliability test at $(Get-Date -Format o)" | Tee-Object -FilePath $metaLog
"Config: $env:EDGE_COLLECTOR_CONFIG" | Tee-Object -FilePath $metaLog -Append
"Cycles: 2880" | Tee-Object -FilePath $metaLog -Append
"PID: $($process.Id)" | Tee-Object -FilePath $metaLog -Append
"STDOUT: $outLog" | Tee-Object -FilePath $metaLog -Append
"STDERR: $errLog" | Tee-Object -FilePath $metaLog -Append
