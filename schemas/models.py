from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class DateRequest(BaseModel):
    """User's date planning request."""
    prompt: str = Field(..., description="Natural language date planning request")


class PlannerOutput(BaseModel):
    """Structured output from Planner agent."""
    city: str = Field(..., description="Target city for the date")
    date_time: Optional[str] = Field(None, description="Preferred date/time")
    budget: Optional[int] = Field(None, description="Budget in INR")
    vibe: str = Field(..., description="Desired atmosphere: romantic, fun, adventure, cozy")
    preferences: List[str] = Field(default_factory=list, description="Additional preferences")


class WeatherData(BaseModel):
    """Weather information from API."""
    temperature: float = Field(..., description="Temperature in Celsius")
    condition: str = Field(..., description="Weather condition")
    humidity: int = Field(..., description="Humidity percentage")
    suitable_for_outdoor: bool = Field(..., description="Weather suitable for outdoor activities")


class PlaceData(BaseModel):
    """Venue/place information."""
    name: str
    category: str
    address: str
    rating: Optional[float] = None
    price_level: Optional[int] = None


class DatePlan(BaseModel):
    """Final date plan response."""
    title: str = Field(..., description="Plan title")
    city: str
    weather: WeatherData
    recommendations: List[PlaceData] = Field(..., description="Recommended venues")
    itinerary: str = Field(..., description="Detailed plan description")
    budget_estimate: Optional[int] = None
    tips: List[str] = Field(default_factory=list, description="Additional tips")
