# Quick Start Guide

## Before You Begin

You need 3 free API keys:

1. **OpenAI**: https://platform.openai.com → API Keys
2. **OpenWeatherMap**: https://openweathermap.org/api → Sign up → Get Key (instant)
3. **Foursquare**: https://location.foursquare.com/developer → Create App → Get API Key

## Setup (5 minutes)

```bash
cd trulymadly-genai-date-planner

# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure environment
copy .env.example .env
# Edit .env and add your 3 API keys

# 3. Run the server
uvicorn main:app

# Server starts at http://localhost:8000
# API Docs: http://localhost:8000/docs
```

## Test It

Open http://localhost:8000/docs and try:

```json
{
  "prompt": "Plan a romantic dinner in Mumbai this Saturday"
}
```

## Push to GitHub

```bash
# Create repo on GitHub first (public): trulymadly-genai-date-planner

git remote add origin https://github.com/YOUR_USERNAME/trulymadly-genai-date-planner.git
git branch -M main
git push -u origin main
```

## Submit

Form link: https://forms.gle/YjoQcqhuhr3w5XtHA

Submit:
- Your GitHub repo URL
- Ensure README.md has all sections
- Verify .env is in .gitignore (not uploaded)

Done! 🚀
