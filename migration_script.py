import os
import csv
import requests
import logging
import subprocess


# Setup logging
logging.basicConfig(
    filename='github_migration.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

BITBUCKET_WORKSPACE = "professionalworkspace"
GITHUB_USERNAME = "rajashoke"

# Tokens (use GitHub Actions secrets in real usage)
BITBUCKET_PAT = os.getenv("BITBUCKET_PAT")
GITHUB_PAT = os.getenv("GITHUB_PAT")

# Headers
bitbucket_headers = {
    "Authorization": f"Bearer {BITBUCKET_PAT}"
}
github_headers = {
    "Authorization": f"token {GITHUB_PAT}",
    "Accept": "application/vnd.github+json"
}

# CSV report setup
report_file = "migration_report.csv"
csv_headers = [
    "Repository", "Cloned from Bitbucket", "Created on GitHub",
    "Pushed to GitHub", "Status", "Message"
]
with open(report_file, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(csv_headers)

def run_cmd(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.returncode, result.stdout.strip(), result.stderr.strip()

def fetch_bitbucket_repos():
    url = f"https://api.bitbucket.org/2.0/repositories/{BITBUCKET_WORKSPACE}?pagelen=100"
    repos = []

    while url:
        response = requests.get(url, headers=bitbucket_headers)
        if response.status_code != 200:
            logging.error(f"Failed to fetch repos: {response.text}")
            break
        data = response.json()
        repos += data.get("values", [])
        url = data.get("next")

    return repos

def clone_push_repo(repo):
    repo_slug = repo["slug"]
    repo_name = repo["name"]
    bitbucket_git_url = repo["links"]["clone"][0]["href"]  # HTTPS clone

    # Clone Bitbucket repo
    logging.info(f"Cloning {repo_slug} from Bitbucket...")
    code, out, err = run_cmd(f"git clone --mirror {bitbucket_git_url}")
    cloned = code == 0
    logging.info(out or err)

    # Create GitHub repo
    github_repo_url = f"https://api.github.com/user/repos"
    payload = {"name": repo_slug, "private": False}

    response = requests.post(github_repo_url, headers=github_headers, json=payload)
    created = response.status_code == 201 or "name already exists" in response.text
    logging.info(f"Creating {repo_slug} on GitHub: {response.status_code} - {response.text}")

    # Push to GitHub
    os.chdir(f"{repo_slug}.git")
    github_push_url = f"https://{GITHUB_USERNAME}:{GITHUB_PAT}@github.com/{GITHUB_USERNAME}/{repo_slug}.git"
    run_cmd(f"git remote set-url origin {github_push_url}")
    code, out, err = run_cmd("git push --mirror")
    pushed = code == 0
    logging.info(out or err)
    os.chdir("..")

    # Clean up
    run_cmd(f"rm -rf {repo_slug}.git")

    # Status logging and CSV
    status = "Success" if all([cloned, created, pushed]) else "Failed"
    message = ""
    if not cloned: message += "Clone failed. "
    if not created: message += "GitHub repo creation failed. "
    if not pushed: message += "Push failed. "

    with open(report_file, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([repo_slug, cloned, created, pushed, status, message.strip()])

def main():
    repos = fetch_bitbucket_repos()
    if not repos:
        logging.error("No repositories found.")
        return

    for repo in repos:
        try:
            clone_push_repo(repo)
        except Exception as e:
            logging.error(f"Error migrating {repo['slug']}: {str(e)}")
            with open(report_file, mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([repo['slug'], False, False, False, "Failed", str(e)])

if __name__ == "__main__":
    main()
