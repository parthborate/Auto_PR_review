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

<img width="631" height="595" alt="image" src="https://github.com/user-attachments/assets/a8596e36-7574-4e0a-b398-a5033d8448b0" />

**Data flow for the AI reviewer:**
