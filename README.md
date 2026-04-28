# 🤖 Auto PR Review — AI-Powered CI/CD Pipeline

![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google_Gemini-8E75B2?style=for-the-badge&logo=google&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Cost](https://img.shields.io/badge/Cost-$0-brightgreen?style=for-the-badge)

> Ever wished you had a senior engineer available 24/7 to review every pull request the moment it lands — catching bugs, spotting security risks, and flagging unclear logic before anyone even hits "merge"? That's exactly what this project does, at zero cost.
>
> This repo wires together **GitHub Actions** and **Google Gemini 2.0 Flash** to build a fully automated AI code reviewer. Every time a pull request is opened, a workflow spins up, grabs the exact lines that changed, sends them to Gemini with a structured review prompt, and posts the AI's feedback directly as a PR comment — all within about 60 seconds.
>
> No paid services. No cloud accounts. No credit card. The entire pipeline runs on GitHub's free Actions tier and Google AI Studio's free Gemini quota. It's the same concept behind commercial tools like CodeRabbit and GitHub Copilot Reviews — built from scratch, fully transparent, and completely under your control.
---

## ✨ What this project does

This repo contains two GitHub Actions workflows:

| Workflow | Trigger | What it does |
|---|---|---|
| `ci.yml` | Every push to `main` | Lint → Test → Build Docker image → Push to GHCR |
| `ai-review.yml` | Every pull request | Fetch diff → Send to Gemini → Post AI review as PR comment |

The app itself is a small Flask todo API — it exists only as a target for the pipeline to lint, test, and containerize.

---

## 🏗️ Architecture

Data flow for the AI reviewer:

    PR opened → gh pr diff → stdin → ai_review.py → Gemini API → stdout → review.txt → gh pr comment

Two workflows run in parallel:

<img width="631" height="595" alt="image" src="https://github.com/user-attachments/assets/a8596e36-7574-4e0a-b398-a5033d8448b0" />

---

## 📁 Project structure

    Auto_PR_review/
    ├── app/
    │   ├── app.py              # Flask todo REST API
    │   ├── requirements.txt    # Python dependencies
    │   └── test_app.py         # pytest unit tests
    ├── scripts/
    │   └── ai_review.py        # Fetches diff, calls Gemini, prints review
    ├── Dockerfile              # Containerizes the Flask app
    └── .github/
        └── workflows/
            ├── ci.yml          # Lint → Test → Build → Push pipeline
            └── ai-review.yml   # PR diff → Gemini → PR comment

---

## 🛠️ Tech stack

| Tool | Purpose | Cost |
|---|---|---|
| GitHub Actions | CI/CD orchestration | ✅ Free (2,000 min/month) |
| Google Gemini 2.0 Flash | AI code review | ✅ Free (1,500 req/day) |
| Docker + GHCR | Container build and registry | ✅ Free for public repos |
| Flask | Sample app for the pipeline | ✅ Free |
| pytest + ruff | Testing and linting | ✅ Free |
| `gh` CLI | Fetch PR diff, post comments | ✅ Free |

> 💰 **Total cost: $0.** Everything runs on free tiers. No credit card required.

---

## 🚀 How to use this

### Prerequisites

- GitHub account
- Google AI Studio account (free) — [aistudio.google.com](https://aistudio.google.com)
- Docker installed locally
- GitHub CLI — `brew install gh` or `sudo apt install gh`

---

### Step 1 — Clone and set up

    git clone https://github.com/YOUR_USERNAME/Auto_PR_review.git
    cd Auto_PR_review

    python -m venv venv
    source venv/bin/activate      # Windows: venv\Scripts\activate
    pip install -r app/requirements.txt

---

### Step 2 — Get your Gemini API key

1. Go to [aistudio.google.com](https://aistudio.google.com)
2. Click **Get API key** → **Create API key**
3. Copy the key

---

### Step 3 — Add the key to GitHub Secrets

1. Go to your repo → **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Name: `GEMINI_API_KEY` — Value: paste your key
4. Click **Add secret**

---

### Step 4 — Trigger the AI reviewer

    git checkout -b my-feature
    git add . && git commit -m "My feature"
    gh pr create --title "Test AI reviewer" --body "Testing"

> ⏱️ Within ~60 seconds, Gemini's review will appear as a comment on your PR.

---

### Step 5 — Run locally (optional)

    docker build -t todo-app .
    docker run -p 5001:5000 todo-app
    # Visit http://localhost:5001/todos

    pytest app/ --cov=app --cov-report=term-missing

    ruff check app/

---

## 🧠 How the AI reviewer works

The core logic lives in `scripts/ai_review.py`:

1. Read the diff from stdin — piped in from `gh pr diff`
2. Build a prompt with the diff embedded at the bottom
3. POST the prompt to Gemini 2.0 Flash via the REST API
4. Print the review — the workflow saves it to `review.txt`
5. The workflow posts `review.txt` as a PR comment using `gh pr comment`

---

## 🌐 API endpoints (the sample app)

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/todos` | List all todos |
| `POST` | `/todos` | Create a todo — body: `{"task": "Buy milk"}` |
| `DELETE` | `/todos/<id>` | Delete a todo by ID |

---

## ✅ Advantages

- 💸 **Zero cost** — Gemini free tier gives 1,500 req/day, GitHub Actions gives 2,000 min/month
- 🔍 **Catches what humans miss** — spots hardcoded secrets, SQL injection vectors, and insecure defaults
- 🕐 **Always available** — runs on every PR, at any hour, without someone needing to be online
- ⚡ **Reduces review queue pressure** — AI handles the first pass, humans handle the judgement calls
- 👁️ **Fully transparent** — review is a plain PR comment, nothing is hidden or applied automatically
- 🔌 **Portable** — swap the Flask app for any language or framework, the pipeline stays the same

---

## ⚠️ Drawbacks and limitations

- 🚦 **Rate limiting** — free tier caps at 15 req/minute. Busy repos will hit 429 errors; retry logic handles spikes but a sustained load needs a paid tier
- ✂️ **Context window limits** — diffs over ~8,000 characters get truncated; large refactors may get an incomplete review
- 🧠 **No memory across reviews** — the AI sees only the current diff, not the full file or review history
- 🎭 **Hallucinations** — Gemini can flag false positives or miss real bugs; always treat it as a first-pass suggestion
- 🎯 **Prompt sensitivity** — review quality depends on the prompt; domain-specific codebases need a tailored prompt
- 🔒 **Public repo only for free GHCR** — pushing Docker images to GHCR is free only for public repos

---

## 🎯 Stretch goals

- [ ] **Severity gate** — fail the PR if Gemini flags anything as `CRITICAL`
- [ ] **Multi-file context** — send the full file alongside the diff for better context
- [ ] **Custom prompts per file type** — different prompts for Python vs YAML vs Dockerfile
- [ ] **SARIF output** — show findings natively in GitHub's Security tab
- [ ] **Ollama fallback** — fall back to a local model if Gemini rate-limits

---

## 📚 What I learned

- GitHub Actions workflows run in ephemeral Ubuntu VMs — nothing persists between runs
- The pipe operator (`|`) connects `gh pr diff` → Python → `review.txt` without any intermediate files
- Secrets are injected as environment variables at runtime and auto-redacted in logs — never hardcode API keys
- Gemini's response structure differs from OpenAI's — always check the docs when switching providers
- Rate limiting (429) is the first real-world problem you hit with free LLM tiers
- `fetch-depth: 0` is critical — without it, `gh pr diff` can't compute the diff

---

## 💰 AI cost

**$0.** All AI calls use the Google Gemini 2.0 Flash free tier (1,500 requests/day). No credit card required.
