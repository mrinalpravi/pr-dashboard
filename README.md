# PR Merge Time Dashboard

A beautiful Flask dashboard that shows how long your GitHub PRs take to merge.

## Credentials Required

| Credential | Where to get it |
|---|---|
| **GitHub Personal Access Token** | GitHub → Settings → Developer Settings → Personal Access Tokens (classic) → Generate. Scopes needed: `repo`, `read:org` |
| **GitHub Username** | Your GitHub login name |

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Set environment variables

**Mac/Linux:**
```bash
export GITHUB_TOKEN="ghp_your_token_here"
export GITHUB_USERNAME="your_username"
```

**Windows (Command Prompt):**
```cmd
set GITHUB_TOKEN=ghp_your_token_here
set GITHUB_USERNAME=your_username
```

**Windows (PowerShell):**
```powershell
$env:GITHUB_TOKEN="ghp_your_token_here"
$env:GITHUB_USERNAME="your_username"
```

### 3. Run the app
```bash
python app.py
```

### 4. Open your browser
Go to: http://localhost:5000

## Features

- 📊 **Line chart** — PR merge time trend over recent PRs
- 📦 **Distribution bar chart** — PRs bucketed by speed (<2h, 2–12h, 1–3d, etc.)
- 👤 **Author chart** — Average merge time by contributor
- 📋 **Sortable table** — All PRs with speed badges (Fast / Medium / Slow)
- 🔢 **Summary stats** — Total PRs, avg/min/max merge time

## Project Structure
```
pr_dashboard/
├── app.py               # Flask backend
├── requirements.txt
├── README.md
└── templates/
    └── index.html       # Frontend dashboard
```
