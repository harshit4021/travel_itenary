from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class Event(BaseModel):
    """Represents an event or activity that happens at a place."""
    name: str
    time: str
    description: Optional[str] = None
    cost: float


class VisitPlace(BaseModel):
    """Represents a single place visited during a trip."""
    name: str
    times: str
    description: Optional[str] = None
    cost_per_visitplace: float
    events: Optional[List[Event]] = None   # ✅ Events inside VisitPlace


class Itinerary(BaseModel):
    """Represents the itinerary for a single day."""
    date: str
    number_of_persons: int
    places: Optional[List[VisitPlace]] = None   # ✅ places include events internally


class Hotel(BaseModel):
    """Represents hotel details for accommodation during the trip."""
    name: str
    check_in: str
    check_out: str
    cost_per_night: float
    address: Optional[str] = None


class Trip(BaseModel):
    """The complete trip plan with all details."""
    destination: str
    start_date: str
    end_date: str
    travelers: int
    itinerary: List[Itinerary]
    hotels: Optional[List[Hotel]] = None
    total_budget: Optional[float] = None


# Enums for user preferences
class BudgetType(str, Enum):
    BUDGET = "budget"
    MID = "mid"
    LUXURY = "luxury"


class TravelStyle(str, Enum):
    ADVENTURE = "adventure"
    CULTURAL = "cultural"
    RELAXATION = "relaxation"
    BUSINESS = "business"
    FAMILY = "family"


class AccommodationType(str, Enum):
    BUDGET = "budget"
    MID = "mid"
    LUXURY = "luxury"
    BOUTIQUE = "boutique"


# User preference and request models
class UserPreferences(BaseModel):
    """User travel preferences for personalized recommendations."""
    interests: List[str] = Field(..., description="List of user interests (e.g., adventure, cultural, culinary)")
    budget_type: BudgetType = Field(default=BudgetType.MID, description="Budget preference")
    travel_style: TravelStyle = Field(default=TravelStyle.CULTURAL, description="Preferred travel style")
    accommodation_type: AccommodationType = Field(default=AccommodationType.MID, description="Accommodation preference")
    activity_intensity: str = Field(default="medium", description="Preferred activity intensity (low/medium/high)")
    dietary_restrictions: Optional[List[str]] = Field(default=None, description="Any dietary restrictions")
    accessibility_needs: Optional[List[str]] = Field(default=None, description="Accessibility requirements")
    group_size_preference: str = Field(default="any", description="Preferred group size for activities")


class TripRequest(BaseModel):
    """Request model for trip planning."""
    destination: str = Field(..., description="Destination city/country")
    start_date: str = Field(..., description="Trip start date (YYYY-MM-DD)")
    end_date: str = Field(..., description="Trip end date (YYYY-MM-DD)")
    travelers: int = Field(..., gt=0, description="Number of travelers")
    budget_total: Optional[float] = Field(default=None, description="Total budget for the trip")
    preferences: UserPreferences = Field(..., description="User travel preferences")
    special_requests: Optional[str] = Field(default=None, description="Any special requests or notes")


class WeatherInfo(BaseModel):
    """Weather information for destination."""
    temperature: int
    condition: str
    is_favorable: bool
    recommendation: str


class CostBreakdown(BaseModel):
    """Detailed cost breakdown for the trip."""
    accommodation: float
    activities: float
    food: float
    transport: float
    total: float
    per_person: float
    per_day: float


class RecommendationScore(BaseModel):
    """Scoring details for recommendations."""
    overall_score: float = Field(..., ge=0, le=10, description="Overall recommendation score (0-10)")
    interest_match: float = Field(..., ge=0, le=10, description="How well it matches user interests")
    budget_fit: float = Field(..., ge=0, le=10, description="How well it fits the budget")
    weather_factor: float = Field(..., ge=0, le=10, description="Weather favorability score")
    popularity_score: float = Field(..., ge=0, le=10, description="General popularity score")


class EnhancedActivity(BaseModel):
    """Enhanced activity model with recommendation scoring."""
    name: str
    type: str
    duration: int
    cost: Dict[str, float]
    rating: float
    description: str
    best_time: str
    location: str
    categories: List[str]
    recommendation_score: Optional[RecommendationScore] = None


class EnhancedHotel(BaseModel):
    """Enhanced hotel model with recommendation scoring."""
    name: str
    category: str
    rating: float
    price_per_night: Dict[str, float]
    amenities: List[str]
    location: str
    description: str
    recommendation_score: Optional[RecommendationScore] = None


class TripRecommendation(BaseModel):
    """Complete trip recommendation with all details."""
    trip: Trip
    weather_info: WeatherInfo
    cost_breakdown: CostBreakdown
    recommended_hotels: List[EnhancedHotel]
    recommended_activities: List[EnhancedActivity]
    personalization_notes: List[str] = Field(default=[], description="Notes about personalization")
    confidence_score: float = Field(..., ge=0, le=10, description="Overall confidence in recommendation")


class DestinationSuggestion(BaseModel):
    """Destination suggestion based on preferences."""
    name: str
    country: str
    description: str
    categories: List[str]
    best_months: List[int]
    avg_daily_budget: Dict[str, float]
    match_score: float = Field(..., ge=0, le=10, description="How well it matches user preferences")
    reasons: List[str] = Field(default=[], description="Reasons why this destination is recommended")
