param(
    [Parameter(Mandatory=$true)]
    [string]$InputPath,

    [Parameter(Mandatory=$true)]
    [int]$Rows,

    [Parameter(Mandatory=$true)]
    [int]$Cols,

    [string]$ScreenSize,
    [string]$OutputDir,
    [string]$Prefix,
    [string]$Codec = "libx264",
    [int]$Crf = 18,
    [string]$Preset = "medium",
    [string]$PixFmt = "yuv420p",
    [double]$Fps = 0,
    [ValidateSet("none", "first", "all")]
    [string]$Audio = "none",
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

function Require-Tool($Name) {
    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        throw "Required tool not found in PATH: $Name"
    }
}

function Parse-Size($Value) {
    if ($Value -notmatch '^(\d+)x(\d+)$') {
        throw "Size must look like WIDTHxHEIGHT, for example 1920x1080"
    }
    return @{ Width = [int]$Matches[1]; Height = [int]$Matches[2] }
}

if ($Rows -le 0 -or $Cols -le 0) {
    throw "Rows and Cols must be positive."
}

$source = Resolve-Path -LiteralPath $InputPath
Require-Tool "ffmpeg"
Require-Tool "ffprobe"

$probeJson = & ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate,duration -of json $source
$probe = $probeJson | ConvertFrom-Json
if (-not $probe.streams -or $probe.streams.Count -eq 0) {
    throw "No video stream found: $source"
}

$sourceWidth = [int]$probe.streams[0].width
$sourceHeight = [int]$probe.streams[0].height
$scaleFilter = $null

if ($ScreenSize) {
    $screen = Parse-Size $ScreenSize
    $tileWidth = $screen.Width
    $tileHeight = $screen.Height
    $canvasWidth = $tileWidth * $Cols
    $canvasHeight = $tileHeight * $Rows
    $scaleFilter = "scale=${canvasWidth}:${canvasHeight}:flags=lanczos"
} else {
    $tileWidth = [math]::Floor($sourceWidth / $Cols)
    $tileHeight = [math]::Floor($sourceHeight / $Rows)
    $canvasWidth = $tileWidth * $Cols
    $canvasHeight = $tileHeight * $Rows
    if ($canvasWidth -ne $sourceWidth -or $canvasHeight -ne $sourceHeight) {
        $scaleFilter = "scale=${canvasWidth}:${canvasHeight}:flags=lanczos"
        Write-Warning "Source ${sourceWidth}x${sourceHeight} is not evenly divisible by ${Cols}x${Rows}; scaling to ${canvasWidth}x${canvasHeight}."
    }
}

if (-not $OutputDir) {
    $baseName = [System.IO.Path]::GetFileNameWithoutExtension($source)
    $parent = Split-Path -Parent $source
    $OutputDir = Join-Path $parent $baseName
}
New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null

if (-not $Prefix) {
    $Prefix = [System.IO.Path]::GetFileNameWithoutExtension($source)
}

$tiles = @()
for ($row = 1; $row -le $Rows; $row++) {
    for ($col = 1; $col -le $Cols; $col++) {
        $filename = "{0}_r{1:D2}_c{2:D2}.mp4" -f $Prefix, $row, $col
        $tiles += [pscustomobject]@{
            file = (Join-Path $OutputDir $filename)
            row = $row
            col = $col
            x = ($col - 1) * $tileWidth
            y = ($row - 1) * $tileHeight
            width = $tileWidth
            height = $tileHeight
        }
    }
}

$manifest = [pscustomobject]@{
    source = "$source"
    source_width = $sourceWidth
    source_height = $sourceHeight
    canvas_width = $canvasWidth
    canvas_height = $canvasHeight
    rows = $Rows
    cols = $Cols
    tile_width = $tileWidth
    tile_height = $tileHeight
    tiles = $tiles
}

$manifest | ConvertTo-Json -Depth 5 | Set-Content -Encoding UTF8 -Path (Join-Path $OutputDir "manifest.json")
$tiles | Export-Csv -NoTypeInformation -Encoding UTF8 -Path (Join-Path $OutputDir "manifest.csv")

foreach ($tile in $tiles) {
    $filters = @()
    if ($scaleFilter) { $filters += $scaleFilter }
    $filters += "crop=$($tile.width):$($tile.height):$($tile.x):$($tile.y)"
    if ($Fps -gt 0) { $filters += "fps=$Fps" }

    $command = @(
        "ffmpeg", "-y",
        "-i", "$source",
        "-map", "0:v:0",
        "-vf", ($filters -join ","),
        "-c:v", $Codec,
        "-preset", $Preset,
        "-crf", "$Crf",
        "-pix_fmt", $PixFmt
    )

    if ($Audio -eq "none") {
        $command += "-an"
    } elseif ($Audio -eq "first" -and -not ($tile.row -eq 1 -and $tile.col -eq 1)) {
        $command += "-an"
    } else {
        $command += @("-map", "0:a?", "-c:a", "copy")
    }

    $command += $tile.file
    Write-Output ($command -join " ")

    if (-not $DryRun) {
        $exe = $command[0]
        $arguments = $command[1..($command.Count - 1)]
        & $exe @arguments
    }
}

Write-Output "Wrote $($tiles.Count) tile entries to $(Join-Path $OutputDir 'manifest.json')"
