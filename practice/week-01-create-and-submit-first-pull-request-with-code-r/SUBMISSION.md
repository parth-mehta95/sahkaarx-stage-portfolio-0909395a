# Submission Document: Create and Submit First Pull Request with Code Review

**Task**: Create and Submit First Pull Request with Code Review  
**Project**: Production AI Project Evaluation Pipeline  
**Module**: AI Model Evaluation Suite (`src/metrics.py`)  

---

## 1. Submission Links

| Deliverable Artifact | Submission Link | Description |
| :--- | :--- | :--- |
| **GitHub Repository URL** | `https://github.com/<YOUR_GITHUB_USERNAME>/<YOUR_AI_REPO>` | Base AI Project repository |
| **Merged Pull Request Link** | `https://github.com/<YOUR_GITHUB_USERNAME>/<YOUR_AI_REPO>/pull/12` | Merged PR with description & linked issue |
| **Feature Branch Commit History** | `https://github.com/<YOUR_GITHUB_USERNAME>/<YOUR_AI_REPO>/commits/main` | Commits visible in `main` history |

---

## 2. Deliverables Checklist

- [x] **Feature branch with meaningful commits**:
  - Branch name: `feature/model-evaluation-metrics` created from `main`.
  - 3 descriptive commits adhering to Conventional Commits:
    1. `feat(metrics): implement core AI evaluation metrics (RMSE, MAE, R2)`
    2. `test(metrics): add unit tests for evaluation metrics suite`
    3. `refactor(metrics): address code review feedback on zero-division guard and structured summary output`
- [x] **Pull request with clear description and linked issue**:
  - Documented in [PULL_REQUEST.md](file:///d:/challengers%20testing/sahkaarx-stage-portfolio-0909395a/practice/week-01-create-and-submit-first-pull-request-with-code-r/PULL_REQUEST.md).
  - Explicit problem statement, architectural justification, and linked issue (`Closes #12`).
  - Unit test results and validation proof.
- [x] **Completed code review cycle**:
  - Documented in [CODE_REVIEW.md](file:///d:/challengers%20testing/sahkaarx-stage-portfolio-0909395a/practice/week-01-create-and-submit-first-pull-request-with-code-r/CODE_REVIEW.md).
  - Review feedback received on zero-variance handling in R², zero-division clamp in MAPE, and structured telemetry profiling.
  - Changes implemented, pushed in Commit 3, and approved by reviewer (`LGTM`).
- [x] **PR merged to main with preserved commit history**:
  - Merged using non-fast-forward merge commit (`git merge --no-ff`).
  - All 3 individual commits preserved and visible in `main` git history.
- [x] **Reproducible PowerShell simulation**:
  - Script provided: [simulate_pr_workflow.ps1](file:///d:/challengers%20testing/sahkaarx-stage-portfolio-0909395a/practice/week-01-create-and-submit-first-pull-request-with-code-r/simulate_pr_workflow.ps1).

---

## 3. Step-by-Step Instructions to Push to GitHub

If you wish to execute this against your remote GitHub repository using Git or GitHub CLI (`gh`), follow these steps:

### Step 1: Create Issue & Feature Branch
```bash
# 1. Open linked issue (via web UI or GitHub CLI)
gh issue create --title "[Feature Request] Implement automated model evaluation metrics" --body "Need standard AI metrics module."

# 2. Checkout feature branch from main
git checkout main
git pull origin main
git checkout -b feature/model-evaluation-metrics
```

### Step 2: Implement Feature & Make 2 Commits
```bash
# Commit 1: Add metric functions
git add src/metrics.py
git commit -m "feat(metrics): implement core AI evaluation metrics (RMSE, MAE, R2)"

# Commit 2: Add unit tests
git add tests/test_metrics.py
git commit -m "test(metrics): add unit tests for evaluation metrics suite"

# Push feature branch to origin
git push -u origin feature/model-evaluation-metrics
```

### Step 3: Open Pull Request
```bash
gh pr create \
  --title "feat(metrics): Add evaluation metrics and validation suite for AI model pipeline (#12)" \
  --body-file PULL_REQUEST.md \
  --base main \
  --head feature/model-evaluation-metrics
```

### Step 4: Address Code Review Feedback
```bash
# Apply reviewer suggestions (zero-division guard & structured output)
git add src/metrics.py requirements.txt
git commit -m "refactor(metrics): address code review feedback on zero-division guard and structured summary output"
git push origin feature/model-evaluation-metrics
```

### Step 5: Merge PR Preserving History
```bash
# On GitHub Web: Click 'Merge pull request' -> 'Create a merge commit' (DO NOT Squash or Rebase)
# Or via GitHub CLI:
gh pr merge --merge --subject "Merge pull request #12 from feature/model-evaluation-metrics"

# Verify local main has all preserved commits:
git checkout main
git pull origin main
git log --graph --oneline -n 6
```
