from flask import Flask, render_template, jsonify, request
import requests
from datetime import datetime, timezone
import os

app = Flask(__name__)

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
GITHUB_USERNAME = os.environ.get("GITHUB_USERNAME", "")

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def get_repos():
    repos = []
    page = 1
    while True:
        url = f"https://api.github.com/user/repos?per_page=100&page={page}&type=all"
        r = requests.get(url, headers=HEADERS)
        if r.status_code != 200:
            break
        data = r.json()
        if not data:
            break
        repos.extend([{"name": repo["name"], "full_name": repo["full_name"]} for repo in data])
        page += 1
    return repos

def get_merged_prs(full_name, limit=50):
    url = f"https://api.github.com/repos/{full_name}/pulls?state=closed&per_page={limit}"
    r = requests.get(url, headers=HEADERS)
    if r.status_code != 200:
        return []
    prs = []
    for pr in r.json():
        if not pr.get("merged_at"):
            continue
        created = datetime.fromisoformat(pr["created_at"].replace("Z", "+00:00"))
        merged = datetime.fromisoformat(pr["merged_at"].replace("Z", "+00:00"))
        hours = (merged - created).total_seconds() / 3600
        prs.append({
            "number": pr["number"],
            "title": pr["title"],
            "author": pr["user"]["login"],
            "created_at": pr["created_at"],
            "merged_at": pr["merged_at"],
            "hours_to_merge": round(hours, 2),
            "days_to_merge": round(hours / 24, 2),
            "url": pr["html_url"],
        })
    return prs

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/repos")
def api_repos():
    repos = get_repos()
    return jsonify(repos)

@app.route("/api/prs")
def api_prs():
    full_name = request.args.get("repo")
    if not full_name:
        return jsonify({"error": "repo param required"}), 400
    prs = get_merged_prs(full_name)
    return jsonify(prs)

@app.route("/api/summary")
def api_summary():
    full_name = request.args.get("repo")
    if not full_name:
        return jsonify({"error": "repo param required"}), 400
    prs = get_merged_prs(full_name)
    if not prs:
        return jsonify({"total": 0, "avg_hours": 0, "min_hours": 0, "max_hours": 0, "prs": []})
    hours = [p["hours_to_merge"] for p in prs]
    return jsonify({
        "total": len(prs),
        "avg_hours": round(sum(hours) / len(hours), 2),
        "min_hours": round(min(hours), 2),
        "max_hours": round(max(hours), 2),
        "prs": prs
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
