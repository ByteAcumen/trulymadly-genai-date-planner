# 🌟 TrulyMadly GenAI Date Planner

> **AI-powered date planning assistant using multi-agent architecture and real-time API integrations**

A sophisticated multi-agent system that transforms natural language requests into personalized date plans by orchestrating real-time weather data, venue recommendations, and AI-powered itinerary generation.

---

## 📋 Table of Contents

- [Architecture](#-architecture)
- [Features](#-features)
- [Quick Start](#-quick-start)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Project Structure](#-project-structure)
- [Technical Details](#-technical-details)
- [Limitations](#-limitations)
- [License](#-license)

---

## 🏗️ Architecture

The system implements a **Planner-Executor-Verifier** pattern with three specialized AI agents:

```
┌─────────────────────────────────────────────────────────────┐
│                     USER REQUEST                             │
│            "Plan a romantic dinner in Mumbai"                │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
        ┌──────────────────────────┐
        │   🧠 PLANNER AGENT       │
        │  (OpenAI GPT-4o-mini)    │
        │                          │
        │  Parses natural language │
        │  Extracts: city, vibe,   │
        │  budget, preferences     │
        └──────────┬───────────────┘
                   │ PlannerOutput (Pydantic)
                   ▼
        ┌──────────────────────────┐
        │   ⚙️ EXECUTOR AGENT      │
        │  (Pure Python)           │
        │                          │
        │  Calls external APIs:    │
        │  • OpenWeatherMap        │
        │  • Foursquare Places     │
        └──────────┬───────────────┘
                   │ Execution Data
                   ▼
        ┌──────────────────────────┐
        │   ✅ VERIFIER AGENT      │
        │  (OpenAI GPT-4o-mini)    │
        │                          │
        │  Validates data quality  │
        │  Generates personalized  │
        │  itinerary & tips        │
        └──────────┬───────────────┘
                   │
                   ▼
        ┌──────────────────────────┐
        │   📦 JSON RESPONSE       │
        │  • Title & Summary       │
        │  • Weather Conditions    │
        │  • Venue Recommendations │
        │  • Detailed Itinerary    │
        │  • Smart Tips            │
        └──────────────────────────┘
```

### Agent Responsibilities

| Agent | Input | Output | Technology |
|-------|-------|--------|------------|
| **Planner** | Natural language prompt | Structured intent (city, budget, vibe, preferences) | OpenAI Structured Outputs + Pydantic |
| **Executor** | Structured intent | Real-time data (weather + venues) | Python + External APIs |
| **Verifier** | Execution data | Final date plan with itinerary | OpenAI Chat Completion |

---

## ✨ Features

- 🤖 **Multi-Agent AI System** - Three specialized agents working in concert
- 🌍 **Real-Time Data** - Live weather and venue information
- 📝 **Natural Language** - Understands casual date planning requests
- 🎯 **Smart Matching** - Weather-adaptive venue suggestions
- 💡 **Contextual Tips** - Personalized recommendations based on conditions
- 🚀 **Dual Interface** - API server + CLI for flexibility
- ⚡ **Error Resilient** - Graceful fallbacks when APIs are unavailable
- 🔒 **Type Safe** - Pydantic models ensure data validation

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- API keys (free tiers available):
  - [OpenAI](https://platform.openai.com/api-keys)
  - [OpenWeatherMap](https://openweathermap.org/api)
  - [Foursquare](https://location.foursquare.com/developer/)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/ByteAcumen/trulymadly-genai-date-planner.git
cd trulymadly-genai-date-planner

# 2. Create virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
# Edit .env and add your API keys
```

### Environment Setup

Create a `.env` file with your API keys:

```env
OPENAI_API_KEY=your_openai_key_here
WEATHER_API_KEY=your_openweathermap_key_here
FOURSQUARE_API_KEY=your_foursquare_key_here
```

---

## 💻 Usage

### Option 1: API Server (Recommended)

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

The server runs at `http://localhost:8000`

**Interactive API Documentation:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

**Example API Request:**

```bash
curl -X POST http://localhost:8000/plan \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Plan a romantic dinner in Mumbai this Saturday"}'
```

**Example Response:**

```json
{
  "title": "Romantic Date in Mumbai",
  "city": "Mumbai",
  "weather": {
    "temperature": 28.5,
    "condition": "Clear",
    "humidity": 65,
    "suitable_for_outdoor": true
  },
  "recommendations": [
    {
      "name": "The Table",
      "category": "Restaurant",
      "address": "Kalaprakalp, Mumbai",
      "rating": 8.7
    }
  ],
  "itinerary": "Start your evening with a sunset walk at Marine Drive...",
  "budget_estimate": 3000,
  "tips": [
    "Book in advance for better seating",
    "Pleasant weather - perfect for outdoor settings"
  ]
}
```

### Option 2: Command Line Interface

Run directly from the terminal:

```bash
python cli.py "Plan a romantic dinner in Mumbai"
```

**CLI Output:**

```
🎯 TrulyMadly GenAI Date Planner
==================================================

📝 Prompt: Plan a romantic dinner in Mumbai

🤖 Initializing AI agents...
📊 Planner Agent analyzing request...
   ✓ Extracted: Mumbai, romantic vibe
🔧 Executor Agent calling APIs...
   ✓ Weather: 28°C
   ✓ Found 5 venues
✅ Verifier Agent generating final plan...

==================================================
🎉 Romantic Date in Mumbai
==================================================

📍 City: Mumbai
🌤️  Weather: 28°C, Clear

🏨 Top Recommendations:
   1. The Table (Restaurant)
      📍 Kalaprakalp, Mumbai
      ⭐ 8.7/10

📅 Itinerary:
   Start your evening with a sunset walk...

💡 Tips:
   • Book in advance for better seating
   • Pleasant weather - perfect for outdoor settings

==================================================
✨ Date plan generated successfully!
==================================================
```

---

## 📡 API Documentation

### Endpoints

#### `POST /plan`

Creates a personalized date plan.

**Request Body:**
```json
{
  "prompt": "string (natural language date planning request)"
}
```

**Response:** `DatePlan` object with recommendations and itinerary

#### `GET /health`

Health check endpoint showing environment status.

**Response:**
```json
{
  "status": "healthy",
  "environment": {
    "OPENAI_API_KEY": "✓",
    "WEATHER_API_KEY": "✓",
    "FOURSQUARE_API_KEY": "✓"
  }
}
```

#### `GET /`

Service metadata and version information.

---

## 📚 Example Prompts

Try these test cases:

```python
# 1. Romantic with budget
"Plan a romantic candlelight dinner in Mumbai within ₹3000"

# 2. Weather-adaptive
"Suggest an indoor date in Delhi for a rainy day"

# 3. Adventure themed
"Find adventure activities in Pune for next weekend"

# 4. Spontaneous
"Quick coffee date in Bangalore right now"

# 5. Specific preferences
"Cozy rooftop dinner in Hyderabad with live music"
```

---

## 📁 Project Structure

```
trulymadly-genai-date-planner/
│
├── 📄 main.py                  # FastAPI application entry point
├── 📄 cli.py                   # Command-line interface
├── 📄 requirements.txt         # Python dependencies
├── 📄 .env.example            # Environment template
├── 📄 .gitignore              # Git ignore rules
├── 📄 README.md               # This file
│
├── 📂 agents/                  # Multi-agent system
│   ├── __init__.py
│   ├── planner.py             # Intent extraction (LLM-powered)
│   ├── executor.py            # API orchestration (pure Python)
│   └── verifier.py            # Validation & generation (LLM-powered)
│
├── 📂 llm/                     # LLM client abstraction
│   ├── __init__.py
│   └── openai_client.py       # Centralized OpenAI client factory
│
├── 📂 tools/                   # External API integrations
│   ├── __init__.py
│   ├── weather.py             # OpenWeatherMap client
│   └── places.py              # Foursquare Places client
│
└── 📂 schemas/                 # Data models
    ├── __init__.py
    └── models.py              # Pydantic schemas for type safety
```

---

## 🔧 Technical Details

### Integrated APIs

| API | Purpose | Data Retrieved | Rate Limit |
|-----|---------|----------------|------------|
| **OpenAI GPT-4o-mini** | Intent parsing & itinerary generation | Structured outputs, natural language | Pay-per-use |
| **OpenWeatherMap** | Real-time weather data | Temperature, conditions, humidity | 1000 calls/day (free) |
| **Foursquare Places** | Venue search & recommendations | Restaurants, cafes, ratings, addresses | 1000 calls/month (free) |

### Technology Stack

- **Framework**: FastAPI (async web framework)
- **LLM**: OpenAI GPT-4o-mini with structured outputs
- **Validation**: Pydantic v2 for runtime type checking
- **HTTP Client**: `httpx` for async API calls
- **Environment**: `python-dotenv` for configuration

### Key Design Decisions

| Decision | Chosen | Alternative | Rationale |
|----------|--------|-------------|-----------|
| **LLM Model** | GPT-4o-mini | GPT-4 | 60% cheaper, sufficient accuracy |
| **Places API** | Foursquare | Google Places | No billing required for free tier |
| **Framework** | FastAPI | Flask | Better async support, auto-docs |
| **Error Handling** | Graceful fallbacks | Fail fast | Better user experience |

---

## ⚠️ Limitations

### Current Constraints

1. **Geographic Scope**: Optimized for Indian cities. International support requires API parameter adjustments.

2. **Weather Forecasting**: OpenWeatherMap free tier provides current conditions only. Future dates use current weather as a proxy.

3. **Rate Limits**:
   - Foursquare: 1000 calls/month
   - OpenWeatherMap: 1000 calls/day
   - No caching implemented

4. **Venue Availability**: API doesn't verify real-time table availability or business hours. Recommendations should be manually verified.

5. **LLM Costs**: OpenAI charges per token. Monitor usage in production.

### Future Improvements

- [ ] Request caching to reduce API calls
- [ ] Cost tracking per request
- [ ] Parallel tool execution for faster responses
- [ ] Support for more cities (international)
- [ ] Real-time availability integration
- [ ] User preference learning

---

## 📊 Performance

- **Average Response Time**: 3-5 seconds (with API calls)
- **Fallback Mode**: <1 second (when APIs unavailable)
- **Memory Usage**: ~150MB (base + loaded models)
- **Concurrent Requests**: Supports async handling

---

## 🧪 Development

### Running Tests

```bash
# Test the CLI
python cli.py "Test prompt"

# Test the API server
uvicorn main:app --reload
# Visit http://localhost:8000/docs to test interactively
```

### Code Quality

- **Type Safety**: All functions use type hints
- **Error Handling**: Try-except blocks with meaningful fallbacks
- **Logging**: Structured error messages for debugging
- **Documentation**: Docstrings for all public methods

---

## 📜 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

Built as part of the TrulyMadly GenAI Intern Assignment.

For questions or feedback: [hemantahir6@gmail.com]

---

## 🙏 Acknowledgments

- OpenAI for GPT-4o-mini API
- OpenWeatherMap for weather data
- Foursquare for venue recommendations
- FastAPI community for excellent documentation

---

<p align="center">
  <strong>Made with ❤️ for TrulyMadly</strong>
</p>
