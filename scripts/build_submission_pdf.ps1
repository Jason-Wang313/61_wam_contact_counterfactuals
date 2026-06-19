param(
  [string]$RepoRoot = (Resolve-Path "$PSScriptRoot\..").Path
)

$ErrorActionPreference = "Stop"

$paperDir = Join-Path $RepoRoot "paper"
$downloadsPdf = "C:\Users\wangz\Downloads\61.pdf"
$desktopPdf = "C:\Users\wangz\Desktop\61.pdf"

Push-Location $RepoRoot
try {
  python "scripts\render_latex_tables.py"
}
finally {
  Pop-Location
}

Push-Location $paperDir
try {
  pdflatex -interaction=nonstopmode -halt-on-error main.tex
  bibtex main
  pdflatex -interaction=nonstopmode -halt-on-error main.tex
  pdflatex -interaction=nonstopmode -halt-on-error main.tex
}
finally {
  Pop-Location
}

Copy-Item -LiteralPath (Join-Path $paperDir "main.pdf") -Destination $downloadsPdf -Force

if (Test-Path $desktopPdf) {
  throw "Desktop artifact exists and must not be produced: $desktopPdf"
}

$pdf = Get-Item -LiteralPath $downloadsPdf
"Wrote $($pdf.FullName) ($($pdf.Length) bytes)"
