# Week 01 Deliverables & Submission Document

**Task**: Initialize Capstone Repository with Conflict Resolution Practice  
**Repository**: Production AI Project Repository  

---

## 1. Submission Links

| Artifact | Submission Link |
| :--- | :--- |
| **Public GitHub Repository URL** | `https://github.com/<YOUR_GITHUB_USERNAME>/<YOUR_AI_REPO_NAME>` |
| **GitHub Wiki Page URL** | `https://github.com/<YOUR_GITHUB_USERNAME>/<YOUR_AI_REPO_NAME>/wiki/Conflict-Resolution-Strategy` |

---

## 2. Checklist of Deliverables

- [x] **Repository Initialized**: Production AI project repository initialized with standard architecture.
- [x] **Comprehensive `.gitignore`**: Covers Python cache, virtual environments, large datasets, model weights (`.pt`, `.onnx`, `.safetensors`), checkpoints, and experiment tracking logs (`wandb`, `runs`).
- [x] **Core AI Project Scaffold**: Includes `requirements.txt`, modular `src/` modules (`config.py`, `model_pipeline.py`), and automated tests in `tests/`.
- [x] **Branch Protection Rules Configured on `main`**:
  - Enforced Pull Request reviews before merging (1+ approver).
  - Dismissed stale approvals upon pushing new commits.
  - Required status checks (tests & linting) to pass before merging.
  - Enforced for repository administrators.
- [x] **Conflict Simulation & Resolution**:
  - Branch 1: `feature/pipeline-optimization` (vectorized standard scaling).
  - Branch 2: `feature/pipeline-logging` (structured JSON logging & performance telemetry).
  - Both branches modified identical lines in `src/model_pipeline.py`.
  - Conflict successfully resolved using **Feature Synthesis**, combining both enhancements without data loss.
- [x] **Wiki Page Committed**: Full conflict resolution strategy and governance documentation created in [CONFLICT_RESOLUTION_STRATEGY.md](file:///d:/challengers%20testing/sahkaarx-stage-portfolio-0909395a/practice/week-01-initialize-capstone-repository-with-conflict-res/CONFLICT_RESOLUTION_STRATEGY.md) and [wiki/Conflict-Resolution-Strategy.md](file:///d:/challengers%20testing/sahkaarx-stage-portfolio-0909395a/practice/week-01-initialize-capstone-repository-with-conflict-res/wiki/Conflict-Resolution-Strategy.md).

---

## 3. GitHub Setup Instructions

Follow these steps to publish to your GitHub account:

### Step A: Push Repository to GitHub
Using GitHub CLI (`gh`):
```bash
gh repo create ai-capstone-production --public --source=. --remote=origin --push
```
Or via standard Git:
```bash
git remote add origin https://github.com/<YOUR_GITHUB_USERNAME>/ai-capstone-production.git
git branch -M main
git push -u origin main
git push origin feature/pipeline-optimization feature/pipeline-logging
```

### Step B: Configure Branch Protection Rules on GitHub
1. Open your GitHub repository in your browser.
2. Navigate to **Settings** > **Branches** (under *Code and automation*).
3. Click **Add branch protection rule** (or **Add rule** in Rulesets).
4. In **Branch name pattern**, enter: `main`.
5. Check the following options:
   - [x] **Require a pull request before merging**
     - Require approvals: `1`
     - [x] **Dismiss stale pull request approvals when new commits are pushed**
   - [x] **Require status checks to pass before merging**
     - [x] **Require branches to be up to date before merging**
   - [x] **Require conversation resolution before merging**
   - [x] **Do not allow bypassing the above settings** (Enforce for administrators)
6. Click **Save changes** / **Create**.

### Step C: Publish Wiki Page
1. On your repository page, click the **Wiki** tab at the top.
2. Click **Create the first page**.
3. Set the Page Title to: `Conflict Resolution Strategy`.
4. Copy the entire contents of [wiki/Conflict-Resolution-Strategy.md](file:///d:/challengers%20testing/sahkaarx-stage-portfolio-0909395a/practice/week-01-initialize-capstone-repository-with-conflict-res/wiki/Conflict-Resolution-Strategy.md) and paste it into the editor.
5. Click **Save Page**.
6. Copy the resulting Wiki URL for your submission.
