[CmdletBinding()]
param(
    [Parameter(Position = 0)]
    [ValidateSet("help", "setup", "run", "verify", "status", "context")]
    [string]$Command = "help",

    [switch]$Copy,

    [string]$OutFile
)

$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$CanonicalRepo = "https://github.com/Logancarton/Synrheon.git"
$VenvPython = Join-Path $RepoRoot ".venv\Scripts\python.exe"

function Get-PythonCommand {
    if (Test-Path $VenvPython) {
        return $VenvPython
    }

    if (Get-Command python -ErrorAction SilentlyContinue) {
        return "python"
    }

    throw "Python was not found. Install Python 3.11+ and run '.\scripts\synrheon.ps1 setup'."
}

function Test-GitRepo {
    if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
        return $false
    }

    return (Test-Path (Join-Path $RepoRoot ".git"))
}

function Normalize-GitRemote {
    param([string]$Url)

    if (-not $Url) {
        return ""
    }

    $normalized = $Url.Trim().TrimEnd("/")

    if ($normalized.EndsWith(".git")) {
        $normalized = $normalized.Substring(0, $normalized.Length - 4)
    }

    return $normalized.ToLowerInvariant()
}

function Test-HasCommit {
    if (-not (Test-GitRepo)) {
        return $false
    }

    $branchInfo = & git -C $RepoRoot status --porcelain=v2 --branch
    $oidLine = $branchInfo |
        Where-Object { $_ -like "# branch.oid *" } |
        Select-Object -First 1

    if (-not $oidLine) {
        return $false
    }

    return (-not $oidLine.EndsWith("(initial)"))
}

function Show-Help {
    @"
Synrheon developer control script

Canonical repository:
  $CanonicalRepo

Commands:
  .\scripts\synrheon.ps1 setup
      Create .venv if needed and install Synrheon with development dependencies.

  .\scripts\synrheon.ps1 run
      Start Synrheon through the Python entry point.

  .\scripts\synrheon.ps1 verify
      Run pytest, compileall, git diff --check, and Git status.

  .\scripts\synrheon.ps1 status
      Show current stage, Git identity, recent commits, and changed files.

  .\scripts\synrheon.ps1 context
      Print a pasteable next-thread context snapshot.

  .\scripts\synrheon.ps1 context -Copy
      Print and copy the context snapshot to the clipboard.

  .\scripts\synrheon.ps1 context -OutFile context_snapshot.txt
      Print and save the context snapshot to a file.
"@
}

function Invoke-Setup {
    Push-Location $RepoRoot
    try {
        if (-not (Test-Path $VenvPython)) {
            if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
                throw "Python 3.11+ is required but the 'python' command was not found."
            }

            Write-Host "Creating .venv..."
            python -m venv .venv
        }

        Write-Host "Installing Synrheon and development dependencies..."
        & $VenvPython -m pip install --upgrade pip
        if ($LASTEXITCODE -ne 0) { throw "pip upgrade failed." }

        & $VenvPython -m pip install -e ".[dev]"
        if ($LASTEXITCODE -ne 0) { throw "Synrheon development install failed." }

        Write-Host ""
        Write-Host "Setup complete."
        Write-Host "Run: .\scripts\synrheon.ps1 run"

        if (Test-GitRepo) {
            $origin = & git -C $RepoRoot remote get-url origin 2>$null
            if ($LASTEXITCODE -eq 0) {
                if ((Normalize-GitRemote "$origin") -ne (Normalize-GitRemote $CanonicalRepo)) {
                    Write-Warning "Git origin is '$origin', not the canonical Synrheon repository '$CanonicalRepo'."
                }
            } else {
                Write-Warning "No Git origin is configured. Canonical repository: $CanonicalRepo"
            }
        }
    }
    finally {
        Pop-Location
    }
}

function Invoke-Run {
    $python = Get-PythonCommand

    Push-Location $RepoRoot
    try {
        & $python -m synrheon
    }
    finally {
        Pop-Location
    }
}

function Invoke-Verify {
    $python = Get-PythonCommand

    Push-Location $RepoRoot
    try {
        Write-Host "== pytest =="
        & $python -m pytest
        if ($LASTEXITCODE -ne 0) { throw "pytest failed." }

        Write-Host ""
        Write-Host "== compileall =="
        & $python -m compileall -q src tests
        if ($LASTEXITCODE -ne 0) { throw "compileall failed." }

        if (Test-GitRepo) {
            Write-Host ""
            Write-Host "== git diff --check =="
            & git -C $RepoRoot diff --check
            if ($LASTEXITCODE -ne 0) { throw "git diff --check failed." }

            Write-Host ""
            Write-Host "== git status --short =="
            & git -C $RepoRoot status --short
        } else {
            Write-Warning "Not a Git worktree; Git verification was skipped."
        }

        Write-Host ""
        Write-Host "Automated verification completed."
        Write-Host "Remember: Synrheon cognitive verification still requires live-organism behavior."
    }
    finally {
        Pop-Location
    }
}

function Invoke-Status {
    Write-Host "Synrheon"
    Write-Host "Canonical repository: $CanonicalRepo"
    Write-Host "Local path: $RepoRoot"
    Write-Host ""

    $currentStage = Join-Path $RepoRoot "docs\CURRENT_STAGE.md"
    if (Test-Path $currentStage) {
        $stageLine = Get-Content -Encoding UTF8 $currentStage |
            Where-Object { $_ -match '^\*\*Stage ' } |
            Select-Object -First 1

        if ($stageLine) {
            Write-Host "Current: $($stageLine.Trim('*'))"
        } else {
            Write-Host "Current stage: docs/CURRENT_STAGE.md exists"
        }
    } else {
        Write-Warning "docs/CURRENT_STAGE.md is missing."
    }

    if (Test-GitRepo) {
        $branchInfo = & git -C $RepoRoot status --porcelain=v2 --branch

        $branchLine = $branchInfo |
            Where-Object { $_ -like "# branch.head *" } |
            Select-Object -First 1

        $oidLine = $branchInfo |
            Where-Object { $_ -like "# branch.oid *" } |
            Select-Object -First 1

        $branch = if ($branchLine) {
            $branchLine.Substring("# branch.head ".Length)
        } else {
            "(unknown)"
        }

        $oid = if ($oidLine) {
            $oidLine.Substring("# branch.oid ".Length)
        } else {
            "(unknown)"
        }

        Write-Host "Branch: $branch"

        if ($oid -eq "(initial)" -or $oid -eq "(unknown)") {
            Write-Host "HEAD: (no commits yet)"
        } else {
            $shortHead = if ($oid.Length -gt 7) { $oid.Substring(0, 7) } else { $oid }
            Write-Host "HEAD: $shortHead"
        }

        $origin = & git -C $RepoRoot remote get-url origin 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Origin: $origin"
            if ((Normalize-GitRemote "$origin") -ne (Normalize-GitRemote $CanonicalRepo)) {
                Write-Warning "Origin does not match the canonical Synrheon repository."
            }
        } else {
            Write-Warning "No Git origin is configured."
        }

        Write-Host ""
        Write-Host "Recent commits:"
        if ($oid -eq "(initial)" -or $oid -eq "(unknown)") {
            Write-Host "(none yet)"
        } else {
            & git -C $RepoRoot log --oneline -5
        }

        Write-Host ""
        Write-Host "Changed files:"
        $status = & git -C $RepoRoot status --short
        if ($status) {
            $status
        } else {
            Write-Host "(clean)"
        }
    } else {
        Write-Warning "This directory is not currently detected as a Git worktree."
    }
}

switch ($Command) {
    "help" {
        Show-Help
    }
    "setup" {
        Invoke-Setup
    }
    "run" {
        Invoke-Run
    }
    "verify" {
        Invoke-Verify
    }
    "status" {
        Invoke-Status
    }
    "context" {
        $contextScript = Join-Path $PSScriptRoot "context.ps1"

        $contextArgs = @{}
        if ($Copy) {
            $contextArgs["Copy"] = $true
        }
        if ($OutFile) {
            $contextArgs["OutFile"] = $OutFile
        }

        & $contextScript @contextArgs
    }
}
