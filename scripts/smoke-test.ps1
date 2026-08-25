param(
    [int]$Port = 8000,
    [string]$BaseUrl = "127.0.0.1"
)

$ErrorActionPreference = "Continue"
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

. .\scripts\dev-env.ps1

$runLog = Join-Path $PSScriptRoot "runserver.log"
if (Test-Path $runLog) { Remove-Item $runLog }

$listener = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
if ($listener) {
    Write-Output "SKIP: port $Port is already in use by PID $($listener.OwningProcess) - refusing to touch it."
    exit 1
}

$server = Start-Process -FilePath "powershell" `
    -ArgumentList "-NoProfile", "-Command", ". .\scripts\dev-env.ps1; & .\.venv\Scripts\python manage.py runserver $BaseUrl`:$Port --noreload *> `"$runLog`"" `
    -WorkingDirectory $root -PassThru -WindowStyle Hidden

Start-Sleep -Seconds 8

function Get-Status([string]$Path) {
    try {
        $resp = Invoke-WebRequest ("http://{0}:{1}{2}" -f $BaseUrl, $Port, $Path) -UseBasicParsing -TimeoutSec 20
        return "$($resp.StatusCode)"
    } catch {
        if ($_.Exception.Response) {
            return "$([int]$_.Exception.Response.StatusCode)"
        }
        return "ERR: $($_.Exception.Message)"
    }
}

$results = [ordered]@{
    "/"       = Get-Status "/"
    "/admin/" = Get-Status "/admin/"
    "/news/"  = Get-Status "/news/"
}

$results.GetEnumerator() | ForEach-Object { Write-Output ("{0} -> {1}" -f $_.Key, $_.Value) }

$children = Get-CimInstance Win32_Process -Filter "ParentProcessId = $($server.Id)" -ErrorAction SilentlyContinue
foreach ($child in $children) { Stop-Process -Id $child.ProcessId -Force -ErrorAction SilentlyContinue }
Stop-Process -Id $server.Id -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2

if (Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue) {
    Write-Output "WARN: port $Port still listening after stop."
} else {
    Write-Output "port $Port released."
}