param(
  [Parameter(ValueFromRemainingArguments = $true)]
  [string[]] $Args
)

$ErrorActionPreference = "Stop"

$DefaultModel = "google/gemini-3-pro-image-preview"
$DefaultEndpoint = "https://openrouter.ai/api/v1/chat/completions"
$DefaultEnvFile = Join-Path $HOME ".config\banana-pro\openrouter.env"

function Show-Usage {
  @"
banana-pro [options] "prompt"

Options:
  --prompt-file <path>       Read UTF-8 prompt text from a file.
  --image <path-or-url>      Reference image path, HTTPS URL, or data URL. Repeatable.
  --aspect-ratio <ratio>     Default: 16:9.
  --image-size <size>        Default: 2K.
  --model <model>            Default: google/gemini-3-pro-image-preview.
  --endpoint <url>           Default: OpenRouter chat completions endpoint.
  --output, -o <dir>         Output directory.
  --timeout <seconds>        Request timeout. Default: 180.
  --env-file <path>          Env file containing OPENROUTER_API_KEY.
  --dry-run                  Print payload without calling OpenRouter.
  --save-json / --no-save-json
  --download-remote / --no-download-remote
"@
}

function Read-EnvFile([string] $Path) {
  if (-not (Test-Path -LiteralPath $Path)) { return }
  foreach ($raw in Get-Content -LiteralPath $Path -Encoding UTF8) {
    $line = $raw.Trim()
    if (-not $line -or $line.StartsWith("#") -or -not $line.Contains("=")) { continue }
    $key, $value = $line.Split("=", 2)
    $key = $key.Trim()
    $value = $value.Trim().Trim('"').Trim("'")
    if ($key -and -not [Environment]::GetEnvironmentVariable($key, "Process")) {
      [Environment]::SetEnvironmentVariable($key, $value, "Process")
    }
  }
}

function Get-MimeType([string] $Path) {
  $ext = [System.IO.Path]::GetExtension($Path).ToLowerInvariant()
  switch ($ext) {
    ".png" { "image/png"; break }
    ".webp" { "image/webp"; break }
    ".gif" { "image/gif"; break }
    ".bmp" { "image/bmp"; break }
    ".jpg" { "image/jpeg"; break }
    ".jpeg" { "image/jpeg"; break }
    default { "image/jpeg" }
  }
}

function Convert-ImageToDataUrl([string] $Value) {
  if ($Value.StartsWith("http://") -or $Value.StartsWith("https://") -or $Value.StartsWith("data:")) {
    return $Value
  }
  $path = (Resolve-Path -LiteralPath $Value).Path
  if (-not (Test-Path -LiteralPath $path)) { throw "Reference image not found: $Value" }
  $mime = Get-MimeType $path
  $encoded = [Convert]::ToBase64String([System.IO.File]::ReadAllBytes($path))
  return "data:$mime;base64,$encoded"
}

function Save-DataUrl([string] $Url, [string] $OutDir, [int] $Index) {
  if (-not $Url.StartsWith("data:")) { return $null }
  $parts = $Url.Split(",", 2)
  $header = $parts[0]
  $encoded = $parts[1]
  $mediaType = $header.Substring(5).Split(";", 2)[0]
  $ext = switch ($mediaType) {
    "image/jpeg" { ".jpg" }
    "image/png" { ".png" }
    "image/webp" { ".webp" }
    "image/gif" { ".gif" }
    default { ".png" }
  }
  $path = Join-Path $OutDir ("banana-pro-{0:D2}{1}" -f $Index, $ext)
  [System.IO.File]::WriteAllBytes($path, [Convert]::FromBase64String($encoded))
  return $path
}

function Get-ImageUrls($Response) {
  $urls = New-Object System.Collections.Generic.List[string]
  foreach ($choice in @($Response.choices)) {
    $message = $choice.message
    foreach ($image in @($message.images)) {
      if ($image.image_url.url) { [void] $urls.Add([string] $image.image_url.url) }
    }
    $content = $message.content
    if ($content -is [array]) {
      foreach ($part in $content) {
        if ($part.type -eq "image_url" -and $part.image_url.url) {
          [void] $urls.Add([string] $part.image_url.url)
        }
      }
    }
  }
  return $urls
}

function Get-TextContent($Response) {
  $texts = New-Object System.Collections.Generic.List[string]
  foreach ($choice in @($Response.choices)) {
    $content = $choice.message.content
    if ($content -is [string] -and $content.Trim()) {
      [void] $texts.Add($content.Trim())
    } elseif ($content -is [array]) {
      foreach ($part in $content) {
        if ($part.type -eq "text" -and $part.text) { [void] $texts.Add([string] $part.text) }
      }
    }
  }
  return ($texts -join "`n`n")
}

$options = @{
  Images = New-Object System.Collections.Generic.List[string]
  AspectRatio = "16:9"
  ImageSize = "2K"
  Model = if ($env:BANANA_PRO_MODEL) { $env:BANANA_PRO_MODEL } else { $DefaultModel }
  Endpoint = if ($env:OPENROUTER_ENDPOINT) { $env:OPENROUTER_ENDPOINT } else { $DefaultEndpoint }
  Output = "banana-pro-output-$([int][double]::Parse((Get-Date -UFormat %s)))"
  Timeout = 180
  SaveJson = $true
  DownloadRemote = $true
  DryRun = $false
  EnvFile = if ($env:BANANA_PRO_ENV) { $env:BANANA_PRO_ENV } else { $DefaultEnvFile }
  PromptParts = New-Object System.Collections.Generic.List[string]
}

for ($i = 0; $i -lt $Args.Count; $i++) {
  $arg = $Args[$i]
  switch ($arg) {
    "--help" { Show-Usage; exit 0 }
    "-h" { Show-Usage; exit 0 }
    "--prompt-file" { $i++; $options.PromptFile = $Args[$i] }
    "--image" { $i++; [void] $options.Images.Add($Args[$i]) }
    "--aspect-ratio" { $i++; $options.AspectRatio = $Args[$i] }
    "--image-size" { $i++; $options.ImageSize = $Args[$i] }
    "--model" { $i++; $options.Model = $Args[$i] }
    "--endpoint" { $i++; $options.Endpoint = $Args[$i] }
    "--output" { $i++; $options.Output = $Args[$i] }
    "-o" { $i++; $options.Output = $Args[$i] }
    "--timeout" { $i++; $options.Timeout = [int] $Args[$i] }
    "--env-file" { $i++; $options.EnvFile = $Args[$i] }
    "--dry-run" { $options.DryRun = $true }
    "--save-json" { $options.SaveJson = $true }
    "--no-save-json" { $options.SaveJson = $false }
    "--download-remote" { $options.DownloadRemote = $true }
    "--no-download-remote" { $options.DownloadRemote = $false }
    default {
      if ($arg.StartsWith("-")) { throw "Unknown argument: $arg" }
      [void] $options.PromptParts.Add($arg)
    }
  }
}

Read-EnvFile $options.EnvFile

if ($options.PromptFile) {
  [void] $options.PromptParts.Add((Get-Content -LiteralPath $options.PromptFile -Raw -Encoding UTF8).Trim())
}
if ($options.PromptParts.Count -eq 0) { throw "Provide a prompt argument or --prompt-file." }
$prompt = (($options.PromptParts | Where-Object { $_ -and $_.Trim() }) -join "`n`n").Trim()

if ($options.Images.Count -gt 0) {
  $content = New-Object System.Collections.Generic.List[object]
  [void] $content.Add([ordered]@{ type = "text"; text = $prompt })
  foreach ($image in $options.Images) {
    [void] $content.Add([ordered]@{
      type = "image_url"
      image_url = [ordered]@{ url = (Convert-ImageToDataUrl $image) }
    })
  }
} else {
  $content = $prompt
}

$payload = [ordered]@{
  model = $options.Model
  messages = @([ordered]@{ role = "user"; content = $content })
  modalities = @("image", "text")
  stream = $false
  image_config = [ordered]@{ aspect_ratio = $options.AspectRatio; image_size = $options.ImageSize }
}

if ($options.DryRun) {
  $payload | ConvertTo-Json -Depth 20
  exit 0
}

$apiKey = [Environment]::GetEnvironmentVariable("OPENROUTER_API_KEY", "Process")
if (-not $apiKey) { throw "Missing OPENROUTER_API_KEY. Set it in the environment or $DefaultEnvFile." }

$headers = @{
  Authorization = "Bearer $apiKey"
  "Content-Type" = "application/json"
  "X-Title" = if ($env:OPENROUTER_X_TITLE) { $env:OPENROUTER_X_TITLE } else { "Banana Pro CLI" }
}
if ($env:OPENROUTER_HTTP_REFERER) { $headers["HTTP-Referer"] = $env:OPENROUTER_HTTP_REFERER }

$body = $payload | ConvertTo-Json -Depth 20 -Compress
$response = Invoke-RestMethod -Uri $options.Endpoint -Method Post -Headers $headers -Body $body -TimeoutSec $options.Timeout

$outDir = [System.IO.Path]::GetFullPath($options.Output)
New-Item -ItemType Directory -Path $outDir -Force | Out-Null
if ($options.SaveJson) {
  $response | ConvertTo-Json -Depth 50 | Set-Content -LiteralPath (Join-Path $outDir "response.json") -Encoding UTF8
}

$saved = New-Object System.Collections.Generic.List[string]
$remote = New-Object System.Collections.Generic.List[string]
$urls = Get-ImageUrls $response
$idx = 1
foreach ($url in $urls) {
  $path = Save-DataUrl $url $outDir $idx
  if ($path) {
    [void] $saved.Add($path)
  } else {
    [void] $remote.Add($url)
    if ($options.DownloadRemote) {
      $downloadPath = Join-Path $outDir ("banana-pro-{0:D2}.png" -f $idx)
      Invoke-WebRequest -Uri $url -OutFile $downloadPath -TimeoutSec $options.Timeout | Out-Null
      [void] $saved.Add($downloadPath)
    }
  }
  $idx++
}

$text = Get-TextContent $response
if ($text) { Set-Content -LiteralPath (Join-Path $outDir "message.txt") -Value ($text + "`n") -Encoding UTF8 }

foreach ($path in $saved) { Write-Output $path }
foreach ($url in $remote) { Write-Output $url }
if ($saved.Count -eq 0 -and $remote.Count -eq 0) {
  Write-Output "No image URL found. Full response saved in $(Join-Path $outDir 'response.json')"
}
