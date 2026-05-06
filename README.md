# Learning Reminder Agent

Sends you a weekly email every Monday morning (9 AM IST) with your current week's AI engineering learning tasks.

Based on the [16-week AI Engineering Roadmap](https://eeshanbembi.com/ai-engineering/).

## How It Works

- GitHub Actions cron runs every Monday
- Calculates which week you're on based on `START_DATE`
- Sends a formatted HTML email with that week's tasks, resources, and goal
- Automatically stops after 16 weeks

## Setup

1. Fork/clone this repo
2. Add GitHub Secrets (Settings → Secrets → Actions):
   - `GMAIL_ADDRESS` — your Gmail address
   - `GMAIL_APP_PASSWORD` — your Gmail App Password ([create one here](https://myaccount.google.com/apppasswords))
3. Set `START_DATE` in the workflow file to your actual start date
4. That's it — emails arrive every Monday

## Manual Test

Trigger manually: Actions → "Weekly Learning Reminder" → "Run workflow"

## Curriculum

| Week | Topic | Phase |
|------|-------|-------|
| 1 | Overview of LLMs | Foundations |
| 2 | Tokenization & Embeddings | Foundations |
| 3 | Transformer Architecture | Foundations |
| 4 | Build GPT | Foundations |
| 5 | LLM Training at Scale | Training |
| 6 | Quantization & Fine-Tuning | Training |
| 7 | RAG Fundamentals | RAG & Retrieval |
| 8 | Hands-On RAG | RAG & Retrieval |
| 9 | Agents & Tool Calling | Agents & Production |
| 10 | MCP & Context Engineering | Agents & Production |
| 11 | Evals & Production | Agents & Production |
| 12 | Reasoning Models | Agents & Production |
| 13 | Image & Video Models | Multimodal & Capstone |
| 14 | Diffusion Models | Multimodal & Capstone |
| 15 | Capstone Build | Multimodal & Capstone |
| 16 | Polish & Publish | Multimodal & Capstone |
