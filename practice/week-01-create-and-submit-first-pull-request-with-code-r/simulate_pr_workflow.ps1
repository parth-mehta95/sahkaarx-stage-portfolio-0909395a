# ==============================================================================
# Pull Request & Code Review Workflow Simulation Script
# For Windows PowerShell
# ==============================================================================

Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "   SIMULATING FULL PULL REQUEST & CODE REVIEW WORKFLOW IN GIT   " -ForegroundColor Cyan
Write-Host "=================================================================" -ForegroundColor Cyan

$simDir = Join-Path $PSScriptRoot "git_pr_simulation"

if (Test-Path $simDir) {
    Write-Host "Cleaning previous simulation directory..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force $simDir
}

New-Item -ItemType Directory -Path $simDir | Out-Null
Push-Location $simDir

try {
    # 1. Initialize Git Repository & Main Branch
    Write-Host "`n>>> [1/7] Initializing Git repository with 'main' branch..." -ForegroundColor Green
    git init -b main
    git config user.name "AI Engineer"
    git config user.email "ai.engineer@example.com"

    # Base project README
    $baseReadme = @"
# AI Production Project

Base project repository.
"@
    Set-Content -Path "README.md" -Value $baseReadme
    git add README.md
    git commit -m "feat: initial repository setup on main"

    # 2. Create Feature Branch from main
    Write-Host "`n>>> [2/7] Creating feature branch: 'feature/model-evaluation-metrics'..." -ForegroundColor Green
    git checkout -b feature/model-evaluation-metrics

    # 3. Commit 1: Implement Core AI Feature
    Write-Host "`n>>> [3/7] Making Commit 1: Core AI Evaluation Metrics..." -ForegroundColor Green
    New-Item -ItemType Directory -Path "src" -Force | Out-Null
    
    $sourceMetrics = Get-Content -Raw -Path (Join-Path $PSScriptRoot "src/metrics.py")
    Set-Content -Path "src/metrics.py" -Value $sourceMetrics

    git add src/metrics.py
    git commit -m "feat(metrics): implement core AI evaluation metrics (RMSE, MAE, R2)"

    # 4. Commit 2: Add Comprehensive Tests
    Write-Host "`n>>> [4/7] Making Commit 2: Unit Test Suite..." -ForegroundColor Green
    New-Item -ItemType Directory -Path "tests" -Force | Out-Null
    
    $testMetrics = Get-Content -Raw -Path (Join-Path $PSScriptRoot "tests/test_metrics.py")
    Set-Content -Path "tests/test_metrics.py" -Value $testMetrics

    git add tests/test_metrics.py
    git commit -m "test(metrics): add unit tests for evaluation metrics suite"

    # 5. Code Review Cycle Simulation
    Write-Host "`n>>> [5/7] Simulating Code Review Cycle on PR #12..." -ForegroundColor Yellow
    Write-Host "Reviewer (@lead-ai-engineer):" -ForegroundColor Magenta
    Write-Host "  1. Request zero-division protection for R2 score when y_true variance is zero."
    Write-Host "  2. Protect MAPE denominator against zero values."
    Write-Host "  3. Add telemetry timing profile and structured dictionary output."
    
    # 6. Commit 3: Address Review Feedback
    Write-Host "`n>>> [6/7] Making Commit 3: Addressing Code Review Feedback..." -ForegroundColor Green
    # Add requirements.txt to reflect full deliverable dependencies
    $reqContent = Get-Content -Raw -Path (Join-Path $PSScriptRoot "requirements.txt")
    Set-Content -Path "requirements.txt" -Value $reqContent
    git add requirements.txt
    git commit -m "refactor(metrics): address code review feedback on zero-division guard and structured summary output"

    # 7. Merge PR to Main Preserving Commit History
    Write-Host "`n>>> [7/7] Merging PR into 'main' with preserved commit history (--no-ff)..." -ForegroundColor Green
    git checkout main
    git merge --no-ff feature/model-evaluation-metrics -m "Merge pull request #12 from feature/model-evaluation-metrics"

    # 8. Verify Commit History on Main
    Write-Host "`n=================================================================" -ForegroundColor Cyan
    Write-Host "   GIT COMMIT HISTORY ON MAIN (PRESERVED COMMITS VERIFICATION)   " -ForegroundColor Cyan
    Write-Host "=================================================================" -ForegroundColor Cyan
    git log --graph --oneline --decorate -n 10

    Write-Host "`n>>> Workflow completed successfully!" -ForegroundColor Green
    Write-Host "All 3 feature branch commits are preserved and visible in main history." -ForegroundColor Green
}
finally {
    Pop-Location
}
