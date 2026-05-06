# Contributing to Carbon Emission Calculator

Thank you for taking the time to contribute! This document covers everything you need to get your changes reviewed and merged cleanly.

---

##  Table of Contents

- [Getting Started](#-getting-started)
- [Project Setup](#-project-setup)
- [Running Tests](#-running-tests)
- [Linting](#-linting)
- [Formatting](#-formatting)
- [Branch & Commit Rules](#-branch--commit-rules)
- [Pull Request Rules](#-pull-request-rules)
- [Code Review](#-code-review)

---

##  Getting Started

1. **Fork** the repository and clone your fork locally:
   ```bash
   git clone https://github.com/<your-username>/Carbon-Emission-Calculator.git
   cd Carbon-Emission-Calculator
   ```

2. Add the upstream remote so you can stay in sync:
   ```bash
   git remote add upstream https://github.com/original-owner/Carbon-Emission-Calculator.git
   ```

3. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate      # macOS / Linux
   venv\Scripts\activate         # Windows
   ```

4. Install all dependencies, including dev tools:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

> **Note:** If `requirements-dev.txt` does not exist yet, install the dev tools manually:
> ```bash
> pip install pytest pytest-django coverage flake8 black isort
> ```

---

##  Running Tests

This project uses **pytest** with the **pytest-django** plugin.

### Run the full test suite
```bash
pytest
```

### Run a specific test file
```bash
pytest emission_app/tests/test_views.py
```

### Run a specific test by name
```bash
pytest -k "test_dashboard_requires_login"
```

### Run with verbose output
```bash
pytest -v
```

### Run with coverage report
```bash
coverage run -m pytest
coverage report -m                  # Summary in terminal
coverage html                       # Full HTML report → htmlcov/index.html
```

> **Minimum coverage threshold:** All PRs must maintain **80% coverage or above**. The CI pipeline will fail if coverage drops below this.

---

##  Linting

This project uses **Flake8** to enforce PEP 8 style and catch common errors.

### Run the linter
```bash
flake8 .
```

### Run against a specific file or directory
```bash
flake8 emission_app/views.py
flake8 emission_app/
```

### Flake8 configuration

Flake8 is configured in `setup.cfg` (or `.flake8`):

```ini
[flake8]
max-line-length = 100
exclude =
    migrations,
    venv,
    .git,
    __pycache__
ignore =
    E501,   # Line too long — handled by Black
    W503    # Line break before binary operator — conflicts with Black
```

> All linting errors must be resolved before a PR will be reviewed. The CI pipeline runs `flake8` automatically on every push.

---

##  Formatting

This project uses **Black** for code formatting and **isort** for import ordering. Do not manually adjust formatting — run these tools instead.

### Format all Python files with Black
```bash
black .
```

### Format a specific file
```bash
black emission_app/views.py
```

### Sort imports with isort
```bash
isort .
```

### Check formatting without making changes (useful in CI)
```bash
black --check .
isort --check-only .
```

### isort configuration

isort is configured to be compatible with Black in `setup.cfg`:

```ini
[isort]
profile = black
skip = migrations, venv
```

> **Always run Black and isort before committing.** The CI pipeline checks formatting and will reject unformatted code.

### Run everything in one go
```bash
isort . && black . && flake8 .
```

---

##  Branch & Commit Rules

### Branch naming

Create a new branch for every piece of work. Never commit directly to `main`.

| Type | Pattern | Example |
|---|---|---|
| New feature | `feature/<short-description>` | `feature/goal-progress-chart` |
| Bug fix | `fix/<short-description>` | `fix/negative-quantity-crash` |
| Documentation | `docs/<short-description>` | `docs/update-contributing` |
| Refactor | `refactor/<short-description>` | `refactor/dashboard-queries` |
| Tests | `test/<short-description>` | `test/emission-record-save` |

```bash
git checkout -b feature/your-feature-name
```

### Commit message format

Follow the **Conventional Commits** specification:

```
<type>(<scope>): <short summary>

[optional body — explain WHY, not WHAT]

[optional footer — e.g. Closes #42]
```

**Types:** `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

**Examples:**

```
feat(goals): add weekly period window calculation

fix(activity): reject zero and negative quantity inputs

docs(contributing): add lint and format instructions

test(views): add dashboard redirect test for unauthenticated users
```

**Rules:**
- Summary line must be **50 characters or fewer**
- Use the **imperative mood** — "add feature", not "added feature"
- Do not end the summary line with a period
- Reference relevant issue numbers in the footer: `Closes #12`

---

## 📬 Pull Request Rules

### Before opening a PR

Run this checklist locally:

```bash
# 1. Sync with upstream to avoid merge conflicts
git fetch upstream
git rebase upstream/main

# 2. Format and sort imports
isort . && black .

# 3. Check for lint errors
flake8 .

# 4. Run the full test suite with coverage
coverage run -m pytest && coverage report -m
```

All four steps must pass cleanly before submitting.

### PR checklist

When opening a PR, confirm each item in the PR description:

- [ ] Code follows the project's formatting and lint standards
- [ ] All existing tests pass
- [ ] New tests are included for any new behaviour or bug fix
- [ ] Coverage has not dropped below 80%
- [ ] Docstrings and inline comments are updated where relevant
- [ ] The PR title follows the Conventional Commits format
- [ ] The branch is rebased on the latest `main`

### PR size

Keep PRs **small and focused**. A PR should do one thing. If you find yourself writing "and also..." in the PR description, split it into two PRs.

| Size | Lines changed | Status |
|---|---|---|
| Ideal | < 200 |  Reviewed quickly |
| Acceptable | 200–500 |  Needs clear description |
| Too large | > 500 |  Please split |

### Draft PRs

Open a **Draft PR** early if you want feedback on direction before the implementation is complete. Mark it ready for review only when the checklist above is fully satisfied.

---

## 👀 Code Review

### As an author

- Respond to all review comments before requesting a re-review
- Use the **"Resolve conversation"** button only after the concern is addressed, not to dismiss it
- Do not force-push to a PR branch after review has started — append new commits instead so reviewers can see the diff

### As a reviewer

- Approve only when all checklist items are met and CI is green
- Prefer asking questions over making demands: _"Could this use `select_related` to avoid N+1?"_ rather than _"Fix this."_
- Label comments by severity:
  - `nit:` — Minor style preference, no action required
  - `suggestion:` — Worth considering but not blocking
  - `blocker:` — Must be resolved before merge

### Merging

- PRs require **at least one approving review** before merging
- Use **Squash and Merge** to keep the `main` history clean
- The PR author merges their own PR after approval
- Delete the branch after merging

---

##  Questions

If you are unsure about anything, open a **GitHub Discussion** or leave a comment on the relevant issue before starting work. It is much easier to align on approach before code is written than after.