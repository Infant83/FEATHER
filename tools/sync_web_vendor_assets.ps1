param(
  [string]$Root = "."
)

$ErrorActionPreference = "Stop"

$rootPath = (Resolve-Path $Root).Path
$vendorRoot = Join-Path $rootPath "site/federnett/vendor"
$mathjaxDir = Join-Path $vendorRoot "mathjax"
$mermaidDir = Join-Path $vendorRoot "mermaid"

New-Item -ItemType Directory -Force -Path $mathjaxDir | Out-Null
New-Item -ItemType Directory -Force -Path $mermaidDir | Out-Null

$targets = @(
  @{
    Url = "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"
    Out = Join-Path $mathjaxDir "tex-svg.js"
  },
  @{
    Url = "https://cdnjs.cloudflare.com/ajax/libs/mermaid/10.9.1/mermaid.min.js"
    Out = Join-Path $mermaidDir "mermaid.min.js"
  }
)

foreach ($target in $targets) {
  Write-Host ("[sync] {0} -> {1}" -f $target.Url, $target.Out)
  Invoke-WebRequest -Uri $target.Url -OutFile $target.Out -UseBasicParsing
}

Write-Host "[sync] done"
