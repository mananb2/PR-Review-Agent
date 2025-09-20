import os
import requests

# === CONFIG ===
# Direct token embedding for your assignment (not recommended in real projects)
TOKEN = "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"
REPO = os.getenv("PR_REPO", "mananb2/PR-Review-Agent")  # default: this repo
SERVER = "github"

def fetch_prs(server, repo, token):
    """Fetch open PRs from GitHub API"""
    if server == "github":
        url = f"https://api.github.com/repos/{repo}/pulls"
        headers = {"Authorization": f"token {token}"}
    else:
        raise ValueError("❌ Unsupported server")

    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return r.json()

def analyze_pr(pr):
    """Simple PR analysis for structure and readability"""
    feedback = []
    title = pr.get("title", "")
    body = pr.get("body", "")

    if len(title) < 5:
        feedback.append("⚠️ PR title is too short, please describe changes better.")

    if not body or len(body.strip()) < 10:
        feedback.append("⚠️ PR description is too minimal, add context or testing steps.")

    files_url = pr.get("url") + "/files"
    files = requests.get(files_url, headers={"Authorization": f"token {TOKEN}"}).json()
    for f in files:
        filename = f.get("filename", "")
        if filename.endswith(".py") and f.get("changes", 0) > 200:
            feedback.append(f"⚠️ Large changes in `{filename}`, consider splitting into smaller PRs.")

    if not feedback:
        feedback.append("✅ Looks good overall!")

    return feedback

def review_prs():
    prs = fetch_prs(SERVER, REPO, TOKEN)
    print(f"📂 Found {len(prs)} open PR(s).")
    for pr in prs:
        print(f"\n🔹 Reviewing PR #{pr['number']}: {pr['title']}")
        feedback = analyze_pr(pr)
        for fb in feedback:
            print(" -", fb)

if __name__ == "__main__":
    review_prs()
