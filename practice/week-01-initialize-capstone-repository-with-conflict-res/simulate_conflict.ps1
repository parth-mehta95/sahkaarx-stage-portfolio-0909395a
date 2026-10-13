# ==============================================================================
# Git Merge Conflict Simulation & Resolution Demonstration Script
# For Windows PowerShell
# ==============================================================================

Write-Host ">>> Initializing Conflict Simulation in temporary playground..." -ForegroundColor Cyan

$tempDir = Join-Path $PSScriptRoot "git_simulation_repo"
if (Test-Path $tempDir) {
    Remove-Item -Recurse -Force $tempDir
}
New-Item -ItemType Directory -Path $tempDir | Out-Null
Push-Location $tempDir

try {
    # 1. Initialize Git Repository
    git init -b main
    git config user.name "AI Engineer"
    git config user.email "ai.engineer@example.com"

    # 2. Add initial project scaffold
    $initialContent = @"
import numpy as np

def preprocess_data(data):
    # Baseline preprocessing: raw array cast
    raw_arr = np.array(data, dtype=np.float32)
    return raw_arr
"@
    New-Item -ItemType Directory -Path "src" -Force | Out-Null
    Set-Content -Path "src/model_pipeline.py" -Value $initialContent
    git add src/model_pipeline.py
    git commit -m "feat: initial pipeline scaffold on main"

    # 3. Create Feature Branch A (Optimization)
    Write-Host "`n>>> Creating feature/pipeline-optimization branch..." -ForegroundColor Green
    git checkout -b feature/pipeline-optimization
    $optContent = @"
import numpy as np

def preprocess_data(data):
    # Feature Branch A: Vectorized batch standard scaling
    raw_arr = np.array(data, dtype=np.float32)
    mean_val = np.mean(raw_arr, axis=0)
    std_val = np.std(raw_arr, axis=0)
    safe_std = np.where(std_val == 0, 1.0, std_val)
    return (raw_arr - mean_val) / (safe_std + 1e-8)
"@
    Set-Content -Path "src/model_pipeline.py" -Value $optContent
    git add src/model_pipeline.py
    git commit -m "feat(pipeline): implement vectorized batch standard scaling"

    # 4. Create Feature Branch B (Logging & Telemetry)
    Write-Host "`n>>> Creating feature/pipeline-logging branch from main..." -ForegroundColor Green
    git checkout main
    git checkout -b feature/pipeline-logging
    $logContent = @"
import json
import logging
import time
import numpy as np

logger = logging.getLogger("AIPipeline")

def preprocess_data(data):
    # Feature Branch B: Execution duration telemetry & structured logging
    start_time = time.perf_counter()
    raw_arr = np.array(data, dtype=np.float32)
    scaled = raw_arr / 255.0
    elapsed_ms = (time.perf_counter() - start_time) * 1000.0
    logger.info(json.dumps({"event": "preprocess_done", "duration_ms": elapsed_ms}))
    return scaled
"@
    Set-Content -Path "src/model_pipeline.py" -Value $logContent
    git add src/model_pipeline.py
    git commit -m "feat(pipeline): add structured json logging and runtime telemetry"

    # 5. Merge Branch A into main
    Write-Host "`n>>> Merging feature/pipeline-optimization into main..." -ForegroundColor Cyan
    git checkout main
    git merge feature/pipeline-optimization -m "Merge branch 'feature/pipeline-optimization' into main"

    # 6. Attempt to merge Branch B into main (TRIGGERS CONFLICT)
    Write-Host "`n>>> Attempting to merge feature/pipeline-logging into main (Expecting CONFLICT)..." -ForegroundColor Yellow
    git merge feature/pipeline-logging

    Write-Host "`n>>> Inspecting Git Status after Conflict Trigger:" -ForegroundColor Magenta
    git status --short

    # 7. Apply Feature Synthesis Resolution
    Write-Host "`n>>> Resolving conflict using Feature Synthesis Strategy..." -ForegroundColor Green
    $resolvedContent = @"
import json
import logging
import time
import numpy as np

logger = logging.getLogger("AIPipeline")

def preprocess_data(data):
    # RESOLVED: Synthesizing Vectorized Normalization (Branch A) + Structured Telemetry (Branch B)
    start_time = time.perf_counter()
    raw_arr = np.array(data, dtype=np.float32)

    mean_val = np.mean(raw_arr, axis=0)
    std_val = np.std(raw_arr, axis=0)
    safe_std = np.where(std_val == 0, 1.0, std_val)
    scaled = (raw_arr - mean_val) / (safe_std + 1e-8)

    elapsed_ms = (time.perf_counter() - start_time) * 1000.0
    logger.info(json.dumps({"event": "preprocess_done", "duration_ms": elapsed_ms}))
    return scaled
"@
    Set-Content -Path "src/model_pipeline.py" -Value $resolvedContent
    git add src/model_pipeline.py
    git commit -m "Merge branch 'feature/pipeline-logging': synthesize vectorized scaling with structured telemetry"

    Write-Host "`n>>> Merge Conflict Successfully Resolved!" -ForegroundColor Green
    Write-Host "`n>>> Commit Graph Topology:" -ForegroundColor Cyan
    git log --graph --oneline --all

} finally {
    Pop-Location
}
