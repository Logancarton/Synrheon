[CmdletBinding()]
param(
    [switch]$Copy,
    [string]$OutFile
)

$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$CanonicalRepo = "https://github.com/Logancarton/Synrheon.git"
$CurrentStagePath = Join-Path $RepoRoot "docs\CURRENT_STAGE.md"
$ImplementationStatusPath = Join-Path $RepoRoot "docs\IMPLEMENTATION_STATUS.md"

function Add-Section {
    param(
        [System.Collections.Generic.List[string]]$Lines,
        [string]$Title,
        [string[]]$Content
    )

    $Lines.Add("")
    $Lines.Add("===== $Title =====")
    foreach ($line in $Content) {
        $Lines.Add([string]$line)
    }
}

function Invoke-GitText {
    param([string[]]$Arguments)

    $output = & git -C $RepoRoot @Arguments 2>&1
    if ($LASTEXITCODE -ne 0) {
        return @("[unavailable] " + (($output | ForEach-Object { "$_" }) -join " "))
    }

    if ($null -eq $output -or @($output).Count -eq 0) {
        return @("(none)")
    }

    return @($output | ForEach-Object { "$_" })
}

$lines = [System.Collections.Generic.List[string]]::new()

$lines.Add("SYNRHEON CONTEXT SNAPSHOT")
$lines.Add("Generated: $([DateTimeOffset]::Now.ToString('yyyy-MM-dd HH:mm:ss zzz'))")
$lines.Add("Canonical repository: $CanonicalRepo")
$lines.Add("Local path: $RepoRoot")

$gitAvailable = $null -ne (Get-Command git -ErrorAction SilentlyContinue)
$isGitRepo = $gitAvailable -and (Test-Path (Join-Path $RepoRoot ".git"))
$hasCommit = $false
$branchInfo = @()

if ($isGitRepo) {
    $branchInfo = & git -C $RepoRoot status --porcelain=v2 --branch
    $oidLine = $branchInfo |
        Where-Object { $_ -like "# branch.oid *" } |
        Select-Object -First 1
    $hasCommit = ($oidLine -and -not $oidLine.EndsWith("(initial)"))
}

if ($isGitRepo) {
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

    $origin = & git -C $RepoRoot remote get-url origin 2>$null
    if ($LASTEXITCODE -ne 0) {
        $origin = "(none configured)"
    }

    Add-Section $lines "GIT IDENTITY" @(
        "Branch: $branch"
        "HEAD: $(if ($hasCommit) { $oid } else { '(no commits yet)' })"
        "Origin: $origin"
    )

    Add-Section $lines "GIT STATUS" (Invoke-GitText @("status", "--short"))

    if ($hasCommit) {
        Add-Section $lines "RECENT COMMITS" (Invoke-GitText @("log", "--oneline", "-5"))
    } else {
        Add-Section $lines "RECENT COMMITS" @("(none yet)")
    }

    Add-Section $lines "UNCOMMITTED DIFF SUMMARY" (Invoke-GitText @("diff", "--stat"))
    Add-Section $lines "STAGED DIFF SUMMARY" (Invoke-GitText @("diff", "--cached", "--stat"))
} else {
    Add-Section $lines "GIT IDENTITY" @(
        "This directory is not currently detected as a Git worktree."
    )
}

if (Test-Path $CurrentStagePath) {
    Add-Section $lines "CURRENT STAGE" (Get-Content -Encoding UTF8 $CurrentStagePath)
} else {
    Add-Section $lines "CURRENT STAGE" @("[missing] docs/CURRENT_STAGE.md")
}

if (Test-Path $ImplementationStatusPath) {
    Add-Section $lines "IMPLEMENTATION STATUS" (Get-Content -Encoding UTF8 $ImplementationStatusPath)
} else {
    Add-Section $lines "IMPLEMENTATION STATUS" @("[missing] docs/IMPLEMENTATION_STATUS.md")
}

$keyFiles = @(
    "README.md",
    "AGENTS.md",
    "agent/ARCHITECTURE_STEWARD.md",
    ".agents/skills/synrheon-development-workflow/SKILL.md",
    ".claude/skills/synrheon-development-workflow.md",
    "docs/SCAFFOLD.md",
    "docs/ARCHITECTURE_PLAN.md",
    "docs/IMPLEMENTATION_STATUS.md",
    "docs/CURRENT_STAGE.md",
    "docs/DECISIONS.md",
    "docs/EXPERIMENTS.md",
    "docs/RESEARCH.md",
    "docs/PROMPT_TEMPLATES.md"
)

$keyFileState = foreach ($relativePath in $keyFiles) {
    $fullPath = Join-Path $RepoRoot ($relativePath -replace "/", "\")
    if (Test-Path $fullPath) {
        "[ok] $relativePath"
    } else {
        "[missing] $relativePath"
    }
}
Add-Section $lines "KEY PROJECT FILES" $keyFileState

$pythonCommand = $null
$venvPython = Join-Path $RepoRoot ".venv\Scripts\python.exe"

if (Test-Path $venvPython) {
    $pythonCommand = $venvPython
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonCommand = "python"
}

if ($pythonCommand) {
    $pythonVersion = & $pythonCommand --version 2>&1
    Add-Section $lines "PYTHON" @(
        "Command: $pythonCommand"
        "Version: $pythonVersion"
    )
} else {
    Add-Section $lines "PYTHON" @(
        "[unavailable] No .venv Python or 'python' command was found."
    )
}

Add-Section $lines "NEXT-THREAD START" @(
    "Tell the next chat to read README.md, AGENTS.md, agent/ARCHITECTURE_STEWARD.md,"
    ".agents/skills/synrheon-development-workflow/SKILL.md, docs/SCAFFOLD.md,"
    "docs/IMPLEMENTATION_STATUS.md, and docs/CURRENT_STAGE.md before material work."
    ""
    "Then provide the thread handoff from docs/PROMPT_TEMPLATES.md plus this snapshot."
)

$snapshot = $lines -join [Environment]::NewLine

if ($OutFile) {
    $resolvedOutFile = if ([System.IO.Path]::IsPathRooted($OutFile)) {
        $OutFile
    } else {
        Join-Path $RepoRoot $OutFile
    }

    $parent = Split-Path -Parent $resolvedOutFile
    if ($parent -and -not (Test-Path $parent)) {
        New-Item -ItemType Directory -Path $parent -Force | Out-Null
    }

    Set-Content -Path $resolvedOutFile -Value $snapshot -Encoding UTF8
    Write-Host "Context snapshot written to: $resolvedOutFile"
}

if ($Copy) {
    if (Get-Command Set-Clipboard -ErrorAction SilentlyContinue) {
        Set-Clipboard -Value $snapshot
        Write-Host "Context snapshot copied to clipboard."
    } else {
        Write-Warning "Set-Clipboard is unavailable. Snapshot was not copied."
    }
}

$snapshot
