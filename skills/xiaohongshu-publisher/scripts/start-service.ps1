param([Parameter(Mandatory=$true)][string]$RuntimeRoot)
$ErrorActionPreference = 'Stop'
$taskRuntime = (Resolve-Path -LiteralPath $RuntimeRoot).Path
$taskBinary = Join-Path $taskRuntime 'xiaohongshu-mcp-windows-amd64.exe'
$taskState = Join-Path $taskRuntime 'state'
if (-not (Test-Path -LiteralPath $taskBinary)) { throw 'Download and verify the pinned upstream executable first.' }
if ((Get-FileHash -LiteralPath $taskBinary -Algorithm SHA256).Hash.ToLower() -ne 'cb55674f90c1649c875be9c4cde3af193b02fc34ffc860c40c8d711e6ca53e27') {
    throw 'Executable differs from the inspected v2.5.5 Windows release; review the upgrade first.'
}
New-Item -ItemType Directory -Path $taskState -Force | Out-Null
$taskListener = Get-NetTCPConnection -LocalPort 18060 -State Listen -ErrorAction SilentlyContinue
if ($taskListener) {
    foreach ($taskConnection in $taskListener) {
        $taskProcess = Get-Process -Id $taskConnection.OwningProcess
        if ($taskConnection.LocalAddress -ne '127.0.0.1' -or $taskProcess.Path -ne $taskBinary) {
            throw 'Port 18060 belongs to another service or is not loopback-only; inspect before continuing.'
        }
    }
    Write-Output 'Existing local publisher process found; run the health/login check.'
    exit 0
}
$taskPidPath = Join-Path $taskState 'server.pid'
if (Test-Path -LiteralPath $taskPidPath) {
    $taskPreviousId = 0
    if ([int]::TryParse(([IO.File]::ReadAllText($taskPidPath).Trim()), [ref]$taskPreviousId)) {
        $taskPrevious = Get-Process -Id $taskPreviousId -ErrorAction SilentlyContinue
        if ($taskPrevious -and $taskPrevious.Path -eq $taskBinary) {
            Write-Output 'Publisher process is still starting; inspect its runtime log before relaunching.'
            exit 0
        }
    }
}
$taskTokenPath = Join-Path $taskState 'auth-token.txt'
if (-not (Test-Path -LiteralPath $taskTokenPath)) {
    $taskRandom = New-Object byte[] 32
    $taskRng = [System.Security.Cryptography.RandomNumberGenerator]::Create()
    try { $taskRng.GetBytes($taskRandom) } finally { $taskRng.Dispose() }
    [IO.File]::WriteAllText($taskTokenPath, [Convert]::ToBase64String($taskRandom))
}
# The entire runtime state also contains the upstream browser login cookies.
$taskAcl = New-Object System.Security.AccessControl.DirectorySecurity
$taskAcl.SetAccessRuleProtection($true, $false)
$taskIdentity = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
$taskRule = New-Object System.Security.AccessControl.FileSystemAccessRule($taskIdentity, 'FullControl', 'ContainerInherit,ObjectInherit', 'None', 'Allow')
$taskAcl.AddAccessRule($taskRule)
Set-Acl -LiteralPath $taskState -AclObject $taskAcl
$taskOldAuth = $env:AUTH_TOKEN
$taskOldCookies = $env:COOKIES_PATH
try {
    $env:AUTH_TOKEN = [IO.File]::ReadAllText($taskTokenPath).Trim()
    if (-not $env:AUTH_TOKEN) { throw 'Local token file is empty.' }
    $env:COOKIES_PATH = Join-Path $taskState 'cookies.json'
    $taskStarted = Start-Process -FilePath $taskBinary -ArgumentList '-port=127.0.0.1:18060','-headless=true' -WorkingDirectory $taskState -WindowStyle Hidden -RedirectStandardOutput (Join-Path $taskState 'server.stdout.log') -RedirectStandardError (Join-Path $taskState 'server.stderr.log') -PassThru
    $taskStarted.Id | Set-Content -LiteralPath (Join-Path $taskState 'server.pid')
    Write-Output "Publisher started (PID $($taskStarted.Id)); first startup may install its browser. Verify health separately."
} finally {
    $env:AUTH_TOKEN = $taskOldAuth
    $env:COOKIES_PATH = $taskOldCookies
}
