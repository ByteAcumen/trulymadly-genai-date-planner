import json
from llm import get_openai_client
from schemas.models import PlannerOutput


class PlannerAgent:
    """
    Planner Agent: Parses user requests into structured data.
    Uses OpenAI with structured outputs.
    """
    
    def __init__(self):
        self.client = get_openai_client()

    
    async def analyze(self, prompt: str) -> PlannerOutput:
        """
        Parse user's natural language request into structured format.
        
        Args:
            prompt: User's date planning request
            
        Returns:
            PlannerOutput with extracted city, vibe, budget, etc.
        """
        system_prompt = """You are a date planning expert. Extract structured information from user requests.
Extract: city, date/time (if mentioned), budget (in INR if mentioned), vibe (romantic/fun/adventure/cozy), and preferences.
Always infer a vibe even if not explicitly stated."""

        try:
            response = self.client.beta.chat.completions.parse(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                response_format=PlannerOutput
            )
            
            return response.choices[0].message.parsed
        except Exception as e:
            print(f"Planner error: {e}")
            return PlannerOutput(
                city="Mumbai",
                vibe="romantic",
                preferences=[]
            )
