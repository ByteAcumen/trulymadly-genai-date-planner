import os
import requests
from typing import List, Optional
from schemas.models import PlaceData


class PlacesTool:
    """Foursquare Places API integration."""
    
    def __init__(self):
        self.api_key = os.getenv('FOURSQUARE_API_KEY')
        self.base_url = 'https://api.foursquare.com/v3/places/search'
    
    def search_places(
        self,
        city: str,
        category: str = 'restaurant',
        limit: int = 5
    ) -> List[PlaceData]:
        """
        Search for places/venues using Foursquare API.
        
        Args:
            city: City name
            category: Type of place (restaurant, cafe, attraction)
            limit: Number of results
            
        Returns:
            List of PlaceData objects
        """
        if not self.api_key:
            raise ValueError("FOURSQUARE_API_KEY not set in environment")
        
        headers = {
            'Authorization': self.api_key,
            'Accept': 'application/json'
        }
        
        params = {
            'near': f'{city},India',
            'categories': self._map_category(category),
            'limit': limit,
            'sort': 'RATING'
        }
        
        try:
            response = requests.get(
                self.base_url,
                headers=headers,
                params=params,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            places = []
            for result in data.get('results', []):
                place = PlaceData(
                    name=result['name'],
                    category=result.get('categories', [{}])[0].get('name', category),
                    address=self._format_address(result.get('location', {})),
                    rating=result.get('rating'),
                    price_level=result.get('price')
                )
                places.append(place)
            
            return places
        except requests.RequestException as e:
            print(f"Places API error: {e}")
            return []
    
    def _map_category(self, category: str) -> str:
        """Map general categories to Foursquare category IDs."""
        mapping = {
            'restaurant': '13065',
            'cafe': '13034',
            'bar': '13003',
            'attraction': '16000',
            'park': '16032'
        }
        return mapping.get(category.lower(), '13065')
    
    def _format_address(self, location: dict) -> str:
        """Format address from location data."""
        parts = []
        if 'address' in location:
            parts.append(location['address'])
        if 'locality' in location:
            parts.append(location['locality'])
        return ', '.join(parts) if parts else 'Address not available'
