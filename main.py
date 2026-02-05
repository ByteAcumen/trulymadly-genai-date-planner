import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from agents import PlannerAgent, ExecutorAgent, VerifierAgent
from schemas import DateRequest, DatePlan

load_dotenv()

app = FastAPI(
    title="TrulyMadly GenAI Date Planner",
    description="Multi-agent AI system for personalized date planning",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

planner = PlannerAgent()
executor = ExecutorAgent()
verifier = VerifierAgent()


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "active",
        "service": "TrulyMadly GenAI Date Planner",
        "version": "1.0.0"
    }


@app.post("/plan", response_model=DatePlan)
async def create_date_plan(request: DateRequest):
    """
    Create a personalized date plan.
    
    Multi-agent flow:
    1. Planner: Parse user intent
    2. Executor: Fetch weather + places data
    3. Verifier: Validate and generate recommendations
    """
    try:
        plan_output = await planner.analyze(request.prompt)
        execution_data = await executor.execute(plan_output)
        final_plan = await verifier.verify(execution_data)
        
        return final_plan
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Detailed health check with API status."""
    required_keys = ["OPENAI_API_KEY", "WEATHER_API_KEY", "FOURSQUARE_API_KEY"]
    env_status = {key: "✓" if os.getenv(key) else "✗" for key in required_keys}
    
    return {
        "status": "healthy",
        "environment": env_status
    }


if __name__ == "__main__":
    import uvicorn
    
    required_vars = ["OPENAI_API_KEY", "WEATHER_API_KEY", "FOURSQUARE_API_KEY"]
    missing = [var for var in required_vars if not os.getenv(var)]
    
    if missing:
        print(f"❌ Missing environment variables: {', '.join(missing)}")
        print("Copy .env.example to .env and add your API keys")
    else:
        print("✅ All environment variables set")
        print("🚀 Starting server on http://localhost:8000")
        print("📖 API docs: http://localhost:8000/docs")
        uvicorn.run(app, host="0.0.0.0", port=8000)

