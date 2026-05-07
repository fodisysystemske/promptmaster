# PROMPTMASTER — Windows training ingest (PowerShell 5+)
param([string]$Root = ".")

Set-Location $Root
Write-Host "=== PROMPTMASTER Live Book ingest ==="

try {
    python -m promptmaster_training.cli verify-livebook
    python -m promptmaster_training.cli totem-demo
} catch {
    Write-Warning "Install package first: pip install -e ."
    throw
}

$files = @(
    "promptmaster.json",
    "promptmaster_livebook_volume2.md",
    "promptmaster_training/prompts/UNIVERSAL_TOTEM_V2_SYSTEM.md",
    "promptmaster_training/integrations/CURSOR_RULES.fragment.md",
    "promptmaster_training/integrations/CLAUDE_PROJECT.md",
    "promptmaster_training/integrations/GENERIC_LLM_BOOTSTRAP.md"
)
foreach ($f in $files) {
    if (Test-Path $f) {
        $w = (Get-Content $f -Raw).Split([char[]]@(), [StringSplitOptions]::RemoveEmptyEntries).Count
        Write-Host "[OK] $f (approx words $w)"
    } else {
        Write-Error "[MISSING] $f"
        exit 2
    }
}
Write-Host "=== Done ==="
