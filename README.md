# TrulyMadly GenAI Date Planner

> **Multi-agent AI system for personalized date planning using real-time APIs**

An AI-powered assistant that transforms natural language requests into complete date plans by orchestrating weather data, venue recommendations, and personalized itineraries through a three-agent architecture.

---

## 🏗️ Architecture

**Planner-Executor-Verifier Pattern**

```
User Request → Planner → Executor → Verifier → JSON Response
                 ↓          ↓          ↓
              OpenAI   Real APIs   OpenAI
           (Parse NL) (Fetch Data) (Generate)
```

| Agent | Responsibility | Technology |
|-------|----------------|------------|
| **Planner** | Parse natural language into structured intent | OpenAI GPT-4o-mini + Pydantic |
| **Executor** | Fetch real-time weather & venue data | Python + External APIs |
| **Verifier** | Validate data & generate personalized plan | OpenAI GPT-4o-mini |

---

## 🚀 Quick Start

### Installation

```bash
# Clone and navigate
git clone https://github.com/ByteAcumen/trulymadly-genai-date-planner.git
cd trulymadly-genai-date-planner

# Setup environment
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Configure API keys
cp .env.example .env
# Add your keys to .env
```

### Environment Variables

```env
OPENAI_API_KEY=your_key_here
WEATHER_API_KEY=your_key_here
FOURSQUARE_API_KEY=your_key_here
```

Get free API keys:
- [OpenAI](https://platform.openai.com/api-keys)
- [OpenWeatherMap](https://openweathermap.org/api)
- [Foursquare](https://location.foursquare.com/developer/)

---

## 💻 Usage

### Option 1: API Server

```bash
uvicorn main:app
```

Server runs at `http://localhost:8000`
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

**Example Request:**
```bash
curl -X POST http://localhost:8000/plan \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Plan a romantic dinner in Mumbai"}'
```

### Option 2: CLI

```bash
python cli.py "Plan a romantic dinner in Mumbai"
```

---

## 📡 API Integrations

| API | Purpose | Data |
|-----|---------|------|
| **OpenAI GPT-4o-mini** | NL parsing & itinerary generation | Structured outputs |
| **OpenWeatherMap** | Real-time weather | Temperature, conditions |
| **Foursquare Places** | Venue search | Restaurants, cafes, ratings |

---

## 📁 Project Structure

```
trulymadly-genai-date-planner/
├── main.py              # FastAPI server
├── cli.py               # CLI interface
├── requirements.txt
├── .env.example
│
├── agents/              # Multi-agent system
│   ├── planner.py      # Intent parser
│   ├── executor.py     # API orchestrator
│   └── verifier.py     # Validation & generation
│
├── llm/                 # LLM abstraction
│   └── openai_client.py
│
├── tools/               # API wrappers
│   ├── weather.py
│   └── places.py
│
└── schemas/             # Pydantic models
    └── models.py
```

---

## 📝 Example Prompts

```
"Plan a romantic dinner in Mumbai within ₹3000"
"Suggest a cozy coffee date in Delhi for today"
"Find adventure activities in Bangalore"
"Quick lunch date in Pune right now"
```

---

## ✨ Features

✅ Multi-agent architecture (Planner-Executor-Verifier)  
✅ OpenAI structured outputs with Pydantic  
✅ Real-time weather & venue data  
✅ Natural language understanding  
✅ Both API and CLI interfaces  
✅ Error handling with graceful fallbacks  
✅ Type-safe with full validation  

---

## 🔧 Technical Highlights

- **Structured Outputs**: Pydantic models ensure type safety
- **Centralized LLM**: Single OpenAI client instance
- **Error Resilience**: Fallback plans when APIs fail
- **Clean Architecture**: Separation of concerns (agents/tools/schemas)
- **Async Support**: FastAPI for concurrent requests

---

## 📊 Response Example

```json
{
  "title": "Romantic Date in Mumbai",
  "city": "Mumbai",
  "weather": {
    "temperature": 28.5,
    "condition": "Clear"
  },
  "recommendations": [
    {
      "name": "The Table",
      "category": "Restaurant",
      "rating": 8.7
    }
  ],
  "itinerary": "Start your evening at Marine Drive...",
  "tips": ["Book in advance", "Perfect weather for rooftops"]
}
```

---

## ⚠️ Limitations

- **Geographic**: Optimized for Indian cities
- **Weather**: Current conditions only (free tier)
- **Rate Limits**: 1000 calls/month (Foursquare)
- **Availability**: Manual verification recommended

---

## 📜 License

MIT License

---

**Built for TrulyMadly GenAI Intern Assignment**
