param(
  [switch]$DryRun,
  [switch]$PruneTempProfiles
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Write-Step([string]$text) {
  Write-Host "[playwright-mcp] $text"
}

function Stop-StaleMcpProcesses {
  $regex = "@playwright\\mcp\\cli\\.js|ms-playwright\\mcp-chrome|playwright_chromiumdev_profile"
  $candidates = Get-CimInstance Win32_Process | Where-Object {
    $_.CommandLine -and $_.CommandLine -match $regex
  }
  if (-not $candidates) {
    Write-Step "No stale Playwright MCP processes found."
    return 0
  }

  $killed = 0
  foreach ($proc in $candidates) {
    $label = "pid=$($proc.ProcessId) name=$($proc.Name)"
    if ($DryRun) {
      Write-Step "DryRun: would stop $label"
      continue
    }
    try {
      Stop-Process -Id $proc.ProcessId -Force -ErrorAction Stop
      Write-Step "Stopped $label"
      $killed += 1
    } catch {
      Write-Step "Skip stop failed ($label): $($_.Exception.Message)"
    }
  }
  return $killed
}

function Remove-StaleLockFiles {
  $profileDir = Join-Path $env:LOCALAPPDATA "ms-playwright\mcp-chrome"
  if (-not (Test-Path $profileDir)) {
    Write-Step "Profile dir missing: $profileDir"
    return 0
  }

  $lockFiles = @(
    "SingletonLock",
    "SingletonCookie",
    "SingletonSocket",
    "DevToolsActivePort"
  )

  $removed = 0
  foreach ($name in $lockFiles) {
    $target = Join-Path $profileDir $name
    if (-not (Test-Path $target)) {
      continue
    }
    if ($DryRun) {
      Write-Step "DryRun: would remove $target"
      continue
    }
    try {
      Remove-Item -LiteralPath $target -Force -ErrorAction Stop
      Write-Step "Removed lock file: $target"
      $removed += 1
    } catch {
      Write-Step "Skip remove failed ($target): $($_.Exception.Message)"
    }
  }
  return $removed
}

function CleanupTempProfiles {
  if (-not $PruneTempProfiles) {
    return 0
  }
  $tempDir = $env:TEMP
  if (-not (Test-Path $tempDir)) {
    return 0
  }
  $targets = Get-ChildItem -Path $tempDir -Directory -ErrorAction SilentlyContinue | Where-Object {
    $_.Name -like "playwright_chromiumdev_profile-*"
  }
  if (-not $targets) {
    Write-Step "No temp Chromium profiles to prune."
    return 0
  }
  $removed = 0
  foreach ($item in $targets) {
    if ($DryRun) {
      Write-Step "DryRun: would prune $($item.FullName)"
      continue
    }
    try {
      Remove-Item -LiteralPath $item.FullName -Recurse -Force -ErrorAction Stop
      Write-Step "Pruned temp profile: $($item.FullName)"
      $removed += 1
    } catch {
      Write-Step "Skip prune failed ($($item.FullName)): $($_.Exception.Message)"
    }
  }
  return $removed
}

Write-Step "Recovery start"
$killedCount = Stop-StaleMcpProcesses
$removedLockCount = Remove-StaleLockFiles
$prunedCount = CleanupTempProfiles
Write-Step "Recovery done (killed=$killedCount, locks_removed=$removedLockCount, temp_profiles_pruned=$prunedCount)"
Write-Step "Recommended MCP args: --headless --isolated"
