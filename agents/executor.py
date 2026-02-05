from tools.weather import WeatherTool
from tools.places import PlacesTool
from schemas.models import PlannerOutput, WeatherData, PlaceData
from typing import Dict, List, Optional


class ExecutorAgent:
    """
    Executor Agent: Calls external APIs to gather real data.
    No LLM needed - pure execution.
    """
    
    def __init__(self):
        self.weather_tool = WeatherTool()
        self.places_tool = PlacesTool()
    
    async def execute(self, plan: PlannerOutput) -> Dict:
        """
        Execute API calls based on planner output.
        
        Args:
            plan: Structured plan from PlannerAgent
            
        Returns:
            Dictionary with weather and places data
        """
        weather = self.weather_tool.get_weather(plan.city)
        
        category = self._determine_category(plan.vibe, weather)
        places = self.places_tool.search_places(plan.city, category, limit=5)
        
        return {
            'plan': plan,
            'weather': weather,
            'places': places,
            'category': category
        }
    
    def _determine_category(
        self,
        vibe: str,
        weather: Optional[WeatherData]
    ) -> str:
        """Determine place category based on vibe and weather."""
        if weather and not weather.suitable_for_outdoor:
            return 'cafe'
        
        vibe_map = {
            'romantic': 'restaurant',
            'fun': 'bar',
            'adventure': 'attraction',
            'cozy': 'cafe'
        }
        return vibe_map.get(vibe.lower(), 'restaurant')
