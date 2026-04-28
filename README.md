# 🤖 Auto PR Review — AI-Powered CI/CD Pipeline

![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google_Gemini-8E75B2?style=for-the-badge&logo=google&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Cost](https://img.shields.io/badge/Cost-$0-brightgreen?style=for-the-badge)

> A GitHub Actions pipeline that automatically reviews every pull request using **Gemini 2.0 Flash**, flags bugs and security risks, and posts the review as a PR comment — at zero cost.

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

```mermaid
flowchart LR
  subgraph W1["Workflow 1 — ci.yml (git push)"]
    A[git push] --> B[Lint - ruff]
    B --> C[Unit tests - pytest]
    C --> D[Docker build]
    D --> E[Push to ghcr.io]
  end

  subgraph W2["Workflow 2 — ai-review.yml (pull request)"]
    F[PR opened] --> G[Fetch PR diff]
    G --> H[Build prompt]
    H --> I[Call Gemini API]
    I --> J[Post PR comment]
  end
```

**Data flow for the AI reviewer:**
