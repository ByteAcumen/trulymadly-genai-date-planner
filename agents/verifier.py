from llm import get_openai_client
from schemas.models import DatePlan, WeatherData, PlaceData
from typing import Dict, List


class VerifierAgent:
    """
    Verifier Agent: Validates data and generates final recommendations.
    Uses LLM to create personalized output.
    """
    
    def __init__(self):
        self.client = get_openai_client()

    
    async def verify(self, execution_data: Dict) -> DatePlan:
        """
        Verify data quality and generate final date plan.
        
        Args:
            execution_data: Data from ExecutorAgent
            
        Returns:
            Complete DatePlan with recommendations
        """
        plan = execution_data['plan']
        weather = execution_data['weather']
        places = execution_data['places']
        
        if not weather or not places:
            return self._fallback_plan(plan, weather, places)
        
        itinerary = await self._generate_itinerary(plan, weather, places)
        tips = self._generate_tips(weather, plan.vibe)
        
        return DatePlan(
            title=f"{plan.vibe.title()} Date in {plan.city}",
            city=plan.city,
            weather=weather,
            recommendations=places[:3],
            itinerary=itinerary,
            budget_estimate=plan.budget,
            tips=tips
        )
    
    async def _generate_itinerary(
        self,
        plan,
        weather: WeatherData,
        places: List[PlaceData]
    ) -> str:
        """Generate personalized itinerary using LLM."""
        venue_list = "\n".join([
            f"- {p.name} ({p.category}): {p.address}"
            for p in places[:3]
        ])
        
        prompt = f"""Create a romantic date itinerary for {plan.city}.
Vibe: {plan.vibe}
Weather: {weather.temperature}°C, {weather.condition}
Budget: {plan.budget or 'flexible'}

Top venues:
{venue_list}

Write a brief, engaging 3-4 sentence itinerary."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Verifier error: {e}")
            return f"Enjoy a {plan.vibe} date at {places[0].name if places else 'a local venue'}."
    
    def _generate_tips(self, weather: WeatherData, vibe: str) -> List[str]:
        """Generate contextual tips."""
        tips = []
        
        if not weather.suitable_for_outdoor:
            tips.append(f"Weather is {weather.condition.lower()} - choose indoor venues")
        
        if weather.temperature > 30:
            tips.append("It's warm - stay hydrated and choose AC venues")
        elif weather.temperature < 20:
            tips.append("Pleasant weather - perfect for outdoor settings")
        
        if vibe == 'romantic':
            tips.append("Book in advance for better seating")
        
        return tips[:3]
    
    def _fallback_plan(self, plan, weather, places) -> DatePlan:
        """Fallback when APIs fail."""
        return DatePlan(
            title=f"Date Plan for {plan.city}",
            city=plan.city,
            weather=weather or WeatherData(
                temperature=25,
                condition="Clear",
                humidity=60,
                suitable_for_outdoor=True
            ),
            recommendations=places or [],
            itinerary=f"Plan a {plan.vibe} date in {plan.city}. Check local venues.",
            budget_estimate=plan.budget,
            tips=["API data unavailable - verify details locally"]
        )
