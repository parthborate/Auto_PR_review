# Auto PR Review — AI-Powered CI/CD Pipeline

> A GitHub Actions pipeline that automatically reviews every pull request using Gemini 2.0 Flash, flags bugs and security risks, and posts the review as a PR comment — at zero cost.

---

## What this project does

This repo contains two GitHub Actions workflows:

1. **CI Pipeline (`ci.yml`)** — runs on every push to `main`. Lints the code, runs unit tests with coverage, builds a Docker image, and pushes it to GitHub Container Registry (GHCR).

2. **AI PR Reviewer (`ai-review.yml`)** — runs on every pull request. Fetches the PR diff, sends it to Google Gemini 2.0 Flash, and posts the AI-generated code review as a comment directly on the PR.

The app itself is a small Flask todo API — it exists only as a target for the pipeline to lint, test, and containerize.

---

## Architecture

~~~
┌─────────────────────────────────┐     ┌──────────────────────────────────┐
│      Workflow 1: ci.yml         │     │    Workflow 2: ai-review.yml      │
│      Trigger: git push          │     │    Trigger: pull request opened   │
│                                 │     │                                   │
│  1. Lint (ruff)                 │     │  1. Fetch diff (gh pr diff)       │
│  2. Unit tests (pytest)         │     │  2. Send to Gemini 2.0 Flash      │
│  3. Build Docker image          │     │  3. Get AI review back            │
│  4. Push to ghcr.io             │     │  4. Post as PR comment            │
└─────────────────────────────────┘     └──────────────────────────────────┘
~~~

Data flow for the AI reviewer:

~~~
PR opened → gh pr diff → stdin → ai_review.py → Gemini API → stdout → review.txt → gh pr comment
~~~
---

## Tech stack

| Tool | Purpose | Cost |
|---|---|---|
| GitHub Actions | CI/CD orchestration | Free (2,000 min/month) |
| Google Gemini 2.0 Flash | AI code review | Free (1,500 req/day) |
| Docker + GHCR | Container build and registry | Free for public repos |
| Flask | Sample app for the pipeline | — |
| pytest + ruff | Testing and linting | — |
| `gh` CLI | Fetch PR diff, post comments | — |

**Total cost: $0.** Everything runs on free tiers.

---

## How to use this

### Prerequisites

- GitHub account
- Google AI Studio account (free) — [aistudio.google.com](https://aistudio.google.com)
- Docker installed locally
- GitHub CLI installed — `brew install gh` or `sudo apt install gh`

### Step 1 — Clone and set up

```bash
git clone https://github.com/YOUR_USERNAME/Auto_PR_review.git
cd Auto_PR_review

python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r app/requirements.txt
```

### Step 2 — Get your Gemini API key

1. Go to [aistudio.google.com](https://aistudio.google.com)
2. Click **Get API key** → **Create API key**
3. Copy the key

### Step 3 — Add the key to GitHub Secrets

1. Go to your repo on GitHub → **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Name: `GEMINI_API_KEY`, Value: paste your key
4. Click **Add secret**

### Step 4 — Trigger the AI reviewer

```bash
git checkout -b my-feature
# edit any file
git add . && git commit -m "My feature"
gh pr create --title "Test AI reviewer" --body "Testing"
```

Within ~60 seconds, Gemini's review will appear as a comment on your PR.

### Step 5 — Run locally (optional)

```bash
# Run the app
docker build -t todo-app .
docker run -p 5001:5000 todo-app
# Visit http://localhost:5001/todos

# Run tests
pytest app/ --cov=app --cov-report=term-missing

# Lint
ruff check app/
```

---

## How the AI reviewer works

The core logic is in `scripts/ai_review.py`:

```python
# 1. Read the diff from stdin (piped from gh pr diff)
diff = sys.stdin.read()

# 2. Build a prompt with the diff embedded
prompt = f"""You are a senior software engineer doing a code review...
--- DIFF ---
{diff}
"""

# 3. Send to Gemini and get the review back
response = httpx.post(
    f"https://generativelanguage.googleapis.com/.../gemini-2.0-flash:generateContent?key={api_key}",
    json={"contents": [{"parts": [{"text": prompt}]}]},
)

# 4. Print the review — gets saved to review.txt by the workflow
print(response.json()["candidates"][0]["content"]["parts"][0]["text"])
```

The workflow then posts `review.txt` as a PR comment using `gh pr comment`.

---

## API endpoints (the sample app)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/todos` | List all todos |
| POST | `/todos` | Create a todo — body: `{"task": "Buy milk"}` |
| DELETE | `/todos/<id>` | Delete a todo by ID |

---

## Advantages

- **Zero cost** — Gemini free tier gives 1,500 requests/day, GitHub Actions gives 2,000 minutes/month. No cloud account or credit card needed.
- **Catches what humans miss** — LLMs are good at spotting security antipatterns (hardcoded secrets, SQL injection vectors, insecure defaults) that reviewers gloss over in a hurry.
- **Always available** — the AI reviewer runs on every PR, at any hour, without someone needing to be online.
- **Reduces review queue pressure** — AI handles the first pass, so human reviewers only need to weigh in on the judgement calls.
- **Fully transparent** — the review is posted as a plain PR comment. Nothing is hidden, blocked, or applied automatically.
- **Portable** — the pattern works with any language or framework. Swap the Flask app for anything else; the pipeline stays the same.
- **Good portfolio signal** — demonstrates CI/CD, containerization, LLM integration, and prompt engineering awareness in one repo.

---

## Drawbacks and limitations

- **Rate limiting** — Gemini's free tier caps at 15 requests/minute. Rapid-fire PRs will hit 429 errors. The retry logic in `ai_review.py` handles transient spikes, but a sustained busy repo needs a paid tier or a queue.
- **Context window limits** — diffs larger than ~8,000 characters get truncated before being sent to Gemini. Large refactors may get an incomplete review.
- **No memory across reviews** — the AI sees only the current diff, not the full file or the history of previous reviews. It can miss bugs that only make sense in broader context.
- **Hallucinations** — Gemini can flag false positives or miss real bugs. The review should always be treated as a first-pass suggestion, not a definitive verdict.
- **Prompt sensitivity** — the quality of the review depends heavily on the prompt. Domain-specific codebases would benefit from a tailored prompt.
- **No severity gate (base version)** — the review is informational only. The pipeline does not fail the PR based on AI findings.
- **Public repo only for free GHCR** — pushing Docker images to GHCR is free only for public repos.
- **Single model dependency** — if Google changes Gemini's API or pricing, the reviewer breaks.

---

## Stretch goals

- **Severity gate** — parse the AI output for keywords like `CRITICAL` and fail the workflow if found, blocking the PR merge.
- **Multi-file context** — send the full file alongside the diff so the AI has more context for each change.
- **Custom prompts per file type** — use a different prompt for Python vs YAML vs Dockerfile.
- **SARIF output** — write findings in SARIF format so they appear natively in GitHub's Security tab.
- **Ollama fallback** — if Gemini rate-limits, fall back to a local Ollama model so CI never fully blocks.

---

## What I learned

- GitHub Actions workflows are triggered by events and run in ephemeral Ubuntu VMs — nothing persists between runs.
- The pipe operator (`|`) is the glue that connects `gh pr diff` → Python → `review.txt` without any intermediate files.
- Secrets are injected as environment variables at runtime and automatically redacted in logs — never hardcode API keys in source code.
- Gemini's response structure differs from OpenAI's — always check the docs when switching providers.
- Rate limiting (429) is the first real-world problem you hit with free LLM tiers. Retry logic is non-negotiable for production use.
- `fetch-depth: 0` in the checkout step is critical — without it, `gh pr diff` can't compute the diff.

---

## AI cost

**$0.** All AI calls use the Google Gemini 2.0 Flash free tier (1,500 requests/day). No credit card required.
