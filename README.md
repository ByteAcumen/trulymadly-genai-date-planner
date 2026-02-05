# TrulyMadly GenAI Date Planner

Multi-agent AI system for personalized date planning using real-time API data.

## Architecture

The system uses a **Planner-Executor-Verifier** architecture with three specialized agents:

```
User Request (POST /plan)
        │
        ▼
┌─────────────────┐
│  PLANNER AGENT  │  Parses natural language → Structured intent
└────────┬────────┘  (OpenAI GPT-4o-mini with Pydantic)
         ▼
┌─────────────────┐
│ EXECUTOR AGENT  │  Fetches real data from APIs
└────────┬────────┘  (Weather + Foursquare Places)
         ▼
┌─────────────────┐
│ VERIFIER AGENT  │  Validates & generates recommendations
└────────┬────────┘  (OpenAI with context-aware prompts)
         ▼
   JSON Response
```

### Agent Responsibilities

| Agent | Purpose | Technology |
|-------|---------|-----------|
| **Planner** | Parse user intent (city, budget, vibe, preferences) | OpenAI Structured Outputs |
| **Executor** | Call Weather + Places APIs, aggregate data | Pure Python (no LLM) |
| **Verifier** | Validate data quality, generate personalized itinerary | OpenAI Chat Completion |

## Setup Instructions

### Prerequisites
- Python 3.10+
- API Keys (free tiers available)

### Installation

```bash
# Clone repository
git clone https://github.com/ByteAcumen/trulymadly-genai-date-planner.git
cd trulymadly-genai-date-planner

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys
```

### Environment Variables

Create a `.env` file with the following keys:

| Variable | Get From | Required |
|----------|----------|----------|
| `OPENAI_API_KEY` | [platform.openai.com](https://platform.openai.com) | ✅ |
| `WEATHER_API_KEY` | [openweathermap.org/api](https://openweathermap.org/api) | ✅ |
| `FOURSQUARE_API_KEY` | [location.foursquare.com/developer](https://location.foursquare.com/developer) | ✅ |

See `.env.example` for the template.

### Running Locally

**Option 1: API Server** (recommended for testing multiple requests)

```bash
uvicorn main:app
```

The server starts at `http://localhost:8000`

- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

**Option 2: CLI** (direct command-line usage)

```bash
python cli.py "Plan a romantic dinner in Mumbai"
```

The CLI runs the complete multi-agent flow without starting a server.

## Integrated APIs

| API | Purpose | Endpoint Used | Data Retrieved |
|-----|---------|---------------|----------------|
| **OpenAI GPT-4o-mini** | Intent parsing & itinerary generation | `chat.completions` | Structured outputs, recommendations |
| **OpenWeatherMap** | Real-time weather data | `/data/2.5/weather` | Temperature, conditions, outdoor suitability |
| **Foursquare Places** | Venue search | `/v3/places/search` | Restaurants, cafes, attractions with ratings |

## Example Prompts

Test the system with these prompts via `POST /plan`:

```bash
curl -X POST http://localhost:8000/plan \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Plan a romantic candlelight dinner in Mumbai this Saturday"}'
```

### Recommended Test Cases

1. **Romantic Date**
   ```
   "Plan a romantic dinner in Mumbai for this Saturday evening"
   ```

2. **Budget-Conscious**
   ```
   "Suggest a fun date in Bangalore within ₹2000 budget"
   ```

3. **Weather-Adaptive**
   ```
   "Create a cozy indoor date plan in Delhi for today"
   ```

4. **Adventure Theme**
   ```
   "Find adventure activities in Pune for next weekend"
   ```

5. **Spontaneous**
   ```
   "Quick coffee date in Hyderabad right now"
   ```

## Known Limitations

1. **Geographic Scope**: Currently optimized for Indian cities. International support requires API parameter adjustments.

2. **Weather Forecast**: OpenWeatherMap free tier provides current conditions only. Future dates use current weather as proxy.

3. **Rate Limits**: Foursquare free tier has 1000 calls/month. Executor implements basic error handling but no request caching.

4. **Venue Availability**: API doesn't verify real-time table availability or business hours. Recommendations should be verified manually.

5. **LLM Hallucination**: While structured outputs reduce errors, LLM-generated itinerary text may occasionally include generic suggestions.

## Trade-offs

| Decision | Chosen | Alternative | Reasoning |
|----------|--------|-------------|-----------|
| Places API | Foursquare | Google Places | No billing required for free tier |
| LLM Model | GPT-4o-mini | GPT-4 | 60% cheaper, sufficient for this use case |
| Async Framework | FastAPI native | aiohttp | Simpler, fewer dependencies |
| Error Handling | Fallback plans | Fail fast | Better UX even when APIs are down |

## Project Structure

```
trulymadly-genai-date-planner/
├── main.py                 # FastAPI application
├── cli.py                  # CLI interface
├── requirements.txt        # Dependencies
├── .env.example           # Environment template
├── .gitignore
├── README.md
│
├── agents/                # Multi-agent system
│   ├── planner.py        # Intent parser
│   ├── executor.py       # API orchestrator
│   └── verifier.py       # Validation & generation
│
├── llm/                   # LLM client abstraction
│   └── openai_client.py  # Centralized OpenAI client
│
├── tools/                 # External API wrappers
│   ├── weather.py        # OpenWeatherMap client
│   └── places.py         # Foursquare client
│
└── schemas/               # Pydantic models
    └── models.py         # Request/Response schemas
```

## License

MIT License - see LICENSE file for details.

---

*Built for the TrulyMadly GenAI Intern Assignment*

