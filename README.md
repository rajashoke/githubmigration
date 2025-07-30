# Bitbucket cloud to GitHub Migration

This repository provides a Python script and an accompanying GitHub Actions workflow that streamline and automate the process of migrating repositories from a Bitbucket workspace to GitHub

---

## Key Features
Workspace Repository Discovery
Automatically fetches all repositories from a specified Bitbucket workspace using the Bitbucket API.

Full-Fidelity Cloning
Clones each repository from Bitbucket using --mirror to retain complete Git history, including branches and tags.

Automated GitHub Repository Creation
Creates corresponding repositories on GitHub using the GitHub CLI and REST API, ensuring consistency in naming and structure.

Preserved Repository Migration
Pushes mirrored repositories to GitHub while maintaining full commit history and repository metadata.

Migration Summary Report
Generates a detailed CSV report outlining the migration status for each repository, including success or failure information.

Artifact Archiving
Uploads migration logs and reports as artifacts within GitHub Actions for easy tracking, auditing, and troubleshooting.

---

## Prerequisites

Bitbucket Personal Access Token (PAT)
A Bitbucket PAT with repository read access is required to fetch and clone repositories from the workspace.

GitHub Personal Access Token (PAT)
A GitHub PAT with permissions to create repositories and push code is needed to set up and migrate content to GitHub.

GitHub Repository for Workflow Hosting
A dedicated GitHub repository is required to host the migration script and GitHub Actions workflow that drive the automation process.

---

---

## Prerequisites In Local Machines

- Python 3.x
- `git` and `gh` CLI tools
- Dependencies: `requests` (`pip install requests`)

---

## Setup

### 1. Add GitHub Secrets

Add the following secrets to your GitHub repository (Settings > Secrets and Variables > Actions):

| Secret Name          | Description                                  |
|----------------------|----------------------------------------------|
| `AEGITHUB_PAT`        | GitHub Personal Access Token (PAT)           |
| `BITBUCKET_PAT`      | Bitbucket Personal Access Token (PAT)        |
| `GITHUB_ORGANISATION`| Your GitHub organization or username         |
| `BITBUCKET_KEY`      | (Optional) Bitbucket workspace key if needed  
| `ENTERPRISE_GIT_URL` | (Optional) Enterprise GitHub URL if used     |
| `ENTERPRISE_BITBUCKET_URL` | (Optional) Enterprise Bitbucket URL    |

> **Note:** `AEGITHUB_PAT` is used instead of `GITHUB_PAT` due to naming restrictions.

### 2. Update `migration.yml` if needed

Make sure the environment variables in the workflow YAML (`migration.yml`) correctly reference your secrets, e.g.:

```yaml
env:
  GITHUB_PAT: ${{ secrets.AEGITHUB_PAT }}
  BITBUCKET_PAT: ${{ secrets.BITBUCKET_PAT }}
  GITHUB_ORGANISATION: ${{ secrets.GITHUB_ORGANISATION }}
  BITBUCKET_KEY: ${{ secrets.BITBUCKET_KEY }}
  ENTERPRISE_GIT_URL: ${{ secrets.ENTERPRISE_GIT_URL }}
  ENTERPRISE_BITBUCKET_URL: ${{ secrets.ENTERPRISE_BITBUCKET_URL }}

  The workflow generates and uploads the following logs:

| File Name              | Purpose                                   |
|------------------------|-------------------------------------------|
| `github_migration.log` | Full log of the migration steps            |
| `migration_report.csv` | CSV report of success/failure per repo     |

> These can be downloaded from the **Artifacts** section of the workflow run.

---

## Log Preview

**migration_report.csv**
**github_migration.log**
