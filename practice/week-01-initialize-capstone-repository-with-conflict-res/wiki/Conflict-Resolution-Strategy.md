# Conflict Resolution Strategy & Repository Governance

Welcome to the AI Capstone Repository Wiki. This document specifies the engineering standards, branch protection rules, and merge conflict resolution protocols established for our production AI repository.

---

## 1. Executive Summary

In a production AI/ML team, multiple engineers concurrently contribute model architectures, data preprocessing transformations, evaluation pipelines, and telemetry integrations. Without standardized Git governance, simultaneous changes to critical pipeline files lead to uncoordinated overwrites, broken builds, or regressions.

This repository enforces:
- Strict branch protection on `main` to ensure code stability.
- Mandatory code review via Pull Requests.
- A standardized, systematic merge conflict resolution procedure centered on **feature synthesis** rather than unilateral overwrites.

---

## 2. Branch Protection Rules on `main`

The `main` branch represents deployable, production-ready code. Direct pushes are disabled.

### Applied Configuration

| Setting | Value | Rationale |
| :--- | :--- | :--- |
| **Branch name pattern** | `main` | Targets default production branch |
| **Require a pull request before merging** | **Enabled** | Prevents direct, unreviewed commits to production |
| **Require approvals** | `1` | Mandates at least one peer review before merging |
| **Dismiss stale pull request approvals when new commits are pushed** | **Enabled** | Re-triggers review requirement if PR code changes |
| **Require status checks to pass before merging** | **Enabled** | Ensures CI test suites (`pytest`, `flake8`) pass green |
| **Require branches to be up to date before merging** | **Enabled** | Eliminates silent divergence from `main` |
| **Require conversation resolution before merging** | **Enabled** | Guarantees all reviewer comments are answered |
| **Do not allow bypassing the above settings** | **Enabled (Enforce for Admins)** | Universal adherence across the entire engineering team |

---

## 3. Git Workflow & Branching Topology

We follow GitHub Flow with descriptive branch prefixes:

```
main (protected)
  │
  ├── feature/pipeline-optimization  (Batch standard scaling & vectorization)
  │
  └── feature/pipeline-logging       (Structured JSON logging & runtime metrics)
```

- `feature/<feature-name>`: New AI pipeline components or architectural improvements.
- `bugfix/<issue-name>`: Targeted defect fixes.
- `experiment/<experiment-name>`: Exploratory model training scripts (isolated).

---

## 4. Conflict Scenario Simulation

### The Scenario
Two machine learning engineers simultaneously branched off `main` at commit `v1.0.0-init` to improve `src/model_pipeline.py` within the `preprocess_data` function:

1. **Engineer A (`feature/pipeline-optimization`)**:
   - Refactored `preprocess_data` using vectorized batch standard scaling (`mean`, `std`, safe division) to improve throughput on large numerical datasets.
   - Merged into `main` first via PR #1.

2. **Engineer B (`feature/pipeline-logging`)**:
   - Concurrently modified the exact same function to add structured JSON logging and execution duration telemetry.
   - Attempted to merge into `main` via PR #2, triggering a **Git Merge Conflict** due to overlapping line edits.

### Visualizing the Conflict in Git

When attempting `git merge feature/pipeline-logging` into `main`, Git flags:
```text
Auto-merging src/model_pipeline.py
CONFLICT (content): Merge conflict in src/model_pipeline.py
Automatic merge failed; fix conflicts and then commit the result.
```

The conflict block inside `src/model_pipeline.py`:
```python
<<<<<<< HEAD
        # Vectorized batch standard scaling (Feature Branch A)
        self.mean_ = np.mean(raw_arr, axis=0)
        self.std_ = np.std(raw_arr, axis=0)
        safe_std = np.where(self.std_ == 0, 1.0, self.std_)
        scaled_data = (raw_arr - self.mean_) / (safe_std + self.epsilon)
        return scaled_data
=======
        # Structured runtime telemetry logging (Feature Branch B)
        start_time = time.perf_counter()
        scaled_data = raw_arr / 255.0  # Simple scaling
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        logger.info(json.dumps({
            "event": "preprocess_completed",
            "duration_ms": elapsed_ms
        }))
        return scaled_data
>>>>>>> feature/pipeline-logging
```

---

## 5. Step-by-Step Conflict Resolution Protocol

Our resolution strategy follows an active **Feature Synthesis Principle**: *Neither engineer's work is discarded. Instead, both improvements are synthesized into a coherent, high-performance, observable pipeline.*

### Step 1: Detect and Inspect
Verify conflicting files and review both incoming and current commits:
```bash
git status
git diff --name-only --diff-filter=U
git log --merge -p src/model_pipeline.py
```

### Step 2: Open Conflict in Resolution Tool
Inspect `src/model_pipeline.py` using VS Code Merge Editor or Git CLI:
- Identify `HEAD` (current branch / `main` with vectorized scaling).
- Identify incoming change (`feature/pipeline-logging` with structured logging).

### Step 3: Perform Intelligent Synthesis
Combine the timer initialization and structured telemetry from Branch B with the high-performance vectorized scaling from Branch A:

```python
        # Combined & Synthesized Result:
        start_time = time.perf_counter()
        raw_arr = np.array(data, dtype=np.float32)

        if raw_arr.size == 0:
            logger.warning(json.dumps({"event": "preprocess_warning", "msg": "Empty input array"}))
            return np.empty((0, 0), dtype=np.float32)

        # 1. Vectorized batch standard scaling (from feature/pipeline-optimization)
        self.mean_ = np.mean(raw_arr, axis=0)
        self.std_ = np.std(raw_arr, axis=0)
        safe_std = np.where(self.std_ == 0, 1.0, self.std_)
        scaled_data = (raw_arr - self.mean_) / (safe_std + self.epsilon)

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        # 2. Structured telemetry logging (from feature/pipeline-logging)
        logger.info(
            json.dumps({
                "event": "preprocess_completed",
                "input_shape": list(raw_arr.shape),
                "output_shape": list(scaled_data.shape),
                "duration_ms": round(elapsed_ms, 3),
            })
        )

        return scaled_data
```

### Step 4: Validate Functionality
Never commit a merge conflict resolution without running tests locally:
```bash
pytest tests/test_pipeline.py -v
flake8 src/ tests/
```

### Step 5: Stage and Commit the Resolution
Once tests pass, finalize the merge commit with a descriptive message explaining the resolution rationale:
```bash
git add src/model_pipeline.py
git commit -m "Merge branch 'feature/pipeline-logging': synthesize vectorized scaling with structured telemetry"
```

---

## 6. Conflict Prevention Best Practices in AI Projects

1. **Modular Code Boundaries**: Keep model architectures (`models/`), data transformations (`datasets/`), and logging/monitoring (`telemetry/`) in separate files to minimize concurrent edits on the same lines.
2. **Track Large Binaries with DVC / Git LFS**: Never commit model weights (`.pt`, `.onnx`) or raw datasets (`.parquet`, `.csv`) directly into Git. Merging binary files in Git is destructive and impossible to resolve cleanly.
3. **Daily Rebase against Upstream**: Feature branches should run `git fetch origin` followed by `git rebase origin/main` daily to identify divergences early when they are minor.
4. **Pre-commit Formatting**: Use `black` and `ruff` in git pre-commit hooks to eliminate cosmetic diffs and indentation mismatches that trigger artificial merge conflicts.

---

## 7. Command Cheat Sheet

| Task | Git Command |
| :--- | :--- |
| Check unresolved files | `git status` |
| View conflict markers | `git diff` |
| View commits on both branches affecting the conflict | `git log --merge -p <file>` |
| Abort a conflicted merge attempt | `git merge --abort` |
| Stage resolved file | `git add <file>` |
| Finalize merge commit | `git commit` |
| View visual branch merge graph | `git log --graph --oneline --all` |
