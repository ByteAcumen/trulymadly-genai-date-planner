import os
import requests
from typing import Optional
from schemas.models import WeatherData


class WeatherTool:
    """OpenWeatherMap API integration."""
    
    def __init__(self):
        self.api_key = os.getenv('WEATHER_API_KEY')
        self.base_url = 'https://api.openweathermap.org/data/2.5/weather'
    
    def get_weather(self, city: str) -> Optional[WeatherData]:
        """
        Fetch real-time weather data for a city.
        
        Args:
            city: City name (e.g., "Mumbai", "Bangalore")
            
        Returns:
            WeatherData object or None if request fails
        """
        if not self.api_key:
            raise ValueError("WEATHER_API_KEY not set in environment")
        
        params = {
            'q': f'{city},IN',
            'appid': self.api_key,
            'units': 'metric'
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            temp = data['main']['temp']
            condition = data['weather'][0]['main']
            humidity = data['main']['humidity']
            
            suitable = self._is_outdoor_suitable(temp, condition)
            
            return WeatherData(
                temperature=temp,
                condition=condition,
                humidity=humidity,
                suitable_for_outdoor=suitable
            )
        except requests.RequestException as e:
            print(f"Weather API error: {e}")
            return None
    
    def _is_outdoor_suitable(self, temp: float, condition: str) -> bool:
        """Determine if weather is suitable for outdoor activities."""
        if condition.lower() in ['rain', 'thunderstorm', 'snow']:
            return False
        if temp < 10 or temp > 40:
            return False
        return True
