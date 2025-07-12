import requests
import pandas as pd

# Replace with your values:
REPO_OWNER = "Yash Doke"
REPO_NAME = "YsD9954"

import os
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

def fetch_commits():
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/commits"
    commits = []
    page = 1

    while True:
        response = requests.get(url, headers=headers, params={"per_page": 100, "page": page})
        if response.status_code != 200 or not response.json():
            break

        for commit in response.json():
            commit_date = commit['commit']['author']['date'][:10]
            commits.append(commit_date)
        page += 1

    df = pd.DataFrame(commits, columns=["date"])
    df = df.groupby("date").size().reset_index(name="commits")
    df.to_csv("github_commits.csv", index=False)
    print("✅ GitHub commits saved to 'data/github_commits.csv'")

if __name__ == "__main__":
    fetch_commits()
