$ErrorActionPreference = 'Stop'

$taskName = "AutonomousBASReliabilityHourlyCheck"
$scriptPath = "c:\GitHubProjects\autonomous-bas-auditor\edge-collector\testing\hourly_reliability_checkpoint.ps1"
$runCmd = 'powershell -NoProfile -ExecutionPolicy Bypass -File "' + $scriptPath + '"'

schtasks /Create /TN $taskName /TR $runCmd /SC HOURLY /MO 1 /F | Out-Null
schtasks /Run /TN $taskName | Out-Null
Write-Output "registered_task=$taskName"
Write-Output "script=$scriptPath"
