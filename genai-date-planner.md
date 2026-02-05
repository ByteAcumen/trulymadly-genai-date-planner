# GenAI Date Planner

## Goal
Build a multi-agent AI system that creates personalized date plans using real APIs. Must pass TrulyMadly's mandatory requirements.

## Success Criteria
- [ ] Runs with `uvicorn main:app`
- [ ] Multi-agent: Planner → Executor → Verifier
- [ ] Uses LLM with structured outputs (Pydantic)
- [ ] Integrates 2+ real APIs
- [ ] No hardcoded responses
- [ ] Complete README with all sections

## Tech Stack

| Component | Choice | Why |
|-----------|--------|-----|
| Framework | FastAPI | Single command run, async |
| LLM | OpenAI GPT-4 | Structured outputs, tool calling |
| Validation | Pydantic v2 | Type-safe, JSON schema |
| Weather API | OpenWeatherMap | Free tier, reliable |
| Places API | Foursquare | Free tier, no billing |

## Architecture

```
POST /plan {"prompt": "..."}
         │
         ▼
    ┌─────────┐     Structured output:
    │ PLANNER │────→ city, date, budget, vibe
    └────┬────┘
         ▼
    ┌──────────┐    API calls:
    │ EXECUTOR │───→ Weather + Places
    └────┬─────┘
         ▼
    ┌──────────┐    Final validation:
    │ VERIFIER │───→ Recommendations
    └────┬─────┘
         ▼
    JSON Response
```

## File Structure

```
trulymadly-genai-date-planner/
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── agents/
│   ├── __init__.py
│   ├── planner.py
│   ├── executor.py
│   └── verifier.py
├── tools/
│   ├── __init__.py
│   ├── weather.py
│   └── places.py
└── schemas/
    ├── __init__.py
    └── models.py
```

## Tasks

### Phase 1: Foundation
- [ ] Create `schemas/models.py` with Pydantic models → Verify: import succeeds
- [ ] Create `tools/weather.py` with OpenWeatherMap → Verify: returns real data
- [ ] Create `tools/places.py` with Foursquare → Verify: returns venues

### Phase 2: Agents
- [ ] Create `agents/planner.py` → Verify: parses "romantic dinner Mumbai" correctly
- [ ] Create `agents/executor.py` → Verify: calls both APIs, returns data
- [ ] Create `agents/verifier.py` → Verify: generates recommendations

### Phase 3: Integration
- [ ] Create `main.py` with FastAPI `/plan` endpoint → Verify: `uvicorn main:app` starts
- [ ] Wire all agents together → Verify: POST returns complete JSON

### Phase 4: Documentation
- [ ] Update README.md with all required sections
- [ ] Verify .env.example has all keys
- [ ] Add 5 example prompts
- [ ] Document limitations

### Phase 5: Deploy
- [ ] Git init and commit
- [ ] Push to GitHub
- [ ] Final test: clone fresh, run, verify

## Done When
- [ ] `uvicorn main:app` starts without errors
- [ ] POST /plan returns structured JSON with real data
- [ ] README has: setup, env vars, architecture, APIs, prompts, limitations
- [ ] GitHub repo is public and accessible

## Notes
- No emojis in code
- Minimal comments (only where truly needed)
- Professional variable names
- Error handling for API failures
