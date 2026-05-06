$ErrorActionPreference = 'Stop'

$taskName = "AutonomousBASReliabilityHourlyCheck"
schtasks /Delete /TN $taskName /F | Out-Null
Write-Output "deleted_task=$taskName"
