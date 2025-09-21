"""
Service layer for business logic.
Provides clean separation between API controllers and data access.
"""

from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
import random
from datetime import datetime

from .repositories import DataRepository
from .recommendation_engine import TripRecommendationEngine
from .models import TripRequest

class TravelDataService:
    """Service for travel data operations."""
    
    def __init__(self, db: Session):
        self.db = db
        self.repo = DataRepository(db)
    
    def get_all_destinations(self) -> List[Dict[str, Any]]:
        """Get all destinations with their data."""
        destinations = self.repo.destinations.get_all()
        return [self.repo.destinations.get_destination_data(dest.key) for dest in destinations]
    
    def get_destination_by_key(self, key: str) -> Optional[Dict[str, Any]]:
        """Get destination data by key."""
        return self.repo.destinations.get_destination_data(key)
    
    def get_hotels_for_destination(self, destination_key: str, budget_type: str = "mid") -> List[Dict[str, Any]]:
        """Get hotels for a destination filtered by budget type."""
        return self.repo.hotels.get_hotels_data(destination_key)
    
    def get_activities_for_destination(self, destination_key: str, interests: List[str] = None) -> List[Dict[str, Any]]:
        """Get activities for a destination filtered by interests."""
        return self.repo.activities.get_activities_data(destination_key, interests)
    
    def get_trip_templates(self) -> List[Dict[str, Any]]:
        """Get all trip templates."""
        return self.repo.trip_templates.get_templates_data()
    
    def get_user_preference_templates(self) -> List[Dict[str, Any]]:
        """Get all user preference templates."""
        return self.repo.user_preferences.get_templates_data()

class WeatherService:
    """Service for weather-related operations."""
    
    def __init__(self, db: Session):
        self.db = db
        self.repo = DataRepository(db)
    
    def get_weather_conditions(self, destination_key: str, travel_month: int) -> Dict[str, Any]:
        """Simulate real-time weather conditions."""
        dest_data = self.repo.destinations.get_destination_data(destination_key)
        if not dest_data:
            return {"temperature": 20, "condition": "unknown", "is_good_weather": False}
        
        temp_range = dest_data["avg_temp_range"]
        best_months = dest_data["best_months"]
        
        # Simulate weather based on month
        is_good_weather = travel_month in best_months
        temp = random.randint(temp_range["min"], temp_range["max"])
        
        conditions = ["sunny", "partly_cloudy", "cloudy", "rainy"]
        weather_condition = random.choice(conditions[:2] if is_good_weather else conditions)
        
        return {
            "temperature": temp,
            "condition": weather_condition,
            "humidity": random.randint(40, 90),
            "is_good_weather": is_good_weather,
            "best_months": best_months
        }

class TripPlanningService:
    """Service for trip planning and recommendations."""
    
    def __init__(self, db: Session):
        self.db = db
        self.data_service = TravelDataService(db)
        self.weather_service = WeatherService(db)
        self.recommendation_engine = TripRecommendationEngine(db)
    
    def plan_trip(self, request: TripRequest) -> Dict[str, Any]:
        """Plan a trip based on user request."""
        # Get destination data
        destination_data = self.data_service.get_destination_by_key(request.destination)
        if not destination_data:
            raise ValueError(f"Destination '{request.destination}' not found")
        
        # Get hotels and activities
        hotels = self.data_service.get_hotels_for_destination(
            request.destination, 
            request.preferences.budget_type
        )
        activities = self.data_service.get_activities_for_destination(
            request.destination, 
            request.preferences.interests
        )
        
        # Get weather information
        start_date = datetime.fromisoformat(request.start_date)
        weather_info = self.weather_service.get_weather_conditions(
            request.destination, 
            start_date.month
        )
        
        # Generate recommendation using the engine
        recommendation = self.recommendation_engine.generate_trip_recommendation(
            request, destination_data, hotels, activities, weather_info
        )
        
        return recommendation
    
    def optimize_trip(self, request: TripRequest) -> Dict[str, Any]:
        """Optimize an existing trip based on new preferences."""
        # For now, this is the same as planning a new trip
        # In the future, this could include more sophisticated optimization
        return self.plan_trip(request)
    
    def suggest_destinations(self, interests: List[str], budget_type: str) -> List[Dict[str, Any]]:
        """Suggest destinations based on interests and budget."""
        destinations = self.data_service.get_all_destinations()
        
        # Score destinations based on interest match and budget fit
        scored_destinations = []
        for dest in destinations:
            # Calculate interest match score
            interest_score = len(set(interests) & set(dest["categories"])) / len(interests) if interests else 0
            
            # Calculate budget fit score
            budget_key = f"budget_daily_{budget_type}"
            budget_score = 1.0  # Default score
            
            # Add destination with score
            scored_destinations.append({
                **dest,
                "recommendation_score": (interest_score * 0.7) + (budget_score * 0.3)
            })
        
        # Sort by score and return top destinations
        scored_destinations.sort(key=lambda x: x["recommendation_score"], reverse=True)
        return scored_destinations[:5]

class AnalyticsService:
    """Service for analytics and popular destinations."""
    
    def __init__(self, db: Session):
        self.db = db
        self.data_service = TravelDataService(db)
    
    def get_popular_destinations(self) -> Dict[str, Any]:
        """Get analytics for popular destinations."""
        destinations = self.data_service.get_all_destinations()
        
        # Simulate popularity data (in production, this would come from actual usage data)
        popular_destinations = []
        for i, dest in enumerate(destinations):
            popularity_score = random.uniform(3.5, 5.0)
            # Extract key from destination name (simplified approach)
            key = dest["name"].lower().split(",")[0].replace(" ", "_")
            if "delhi" in dest["name"].lower():
                key = "delhi"
            elif "mumbai" in dest["name"].lower():
                key = "mumbai"
            elif "goa" in dest["name"].lower():
                key = "goa"
            elif "jaipur" in dest["name"].lower() or "rajasthan" in dest["name"].lower():
                key = "rajasthan"
            elif "kerala" in dest["name"].lower():
                key = "kerala"
            elif "himachal" in dest["name"].lower():
                key = "himachal"
            elif "ladakh" in dest["name"].lower():
                key = "ladakh"
            elif "andaman" in dest["name"].lower():
                key = "andaman"
            
            popular_destinations.append({
                "destination": dest["name"],
                "key": key,
                "popularity_score": round(popularity_score, 1),
                "total_bookings": random.randint(100, 1000),
                "avg_rating": round(random.uniform(4.0, 4.8), 1)
            })
        
        # Sort by popularity
        popular_destinations.sort(key=lambda x: x["popularity_score"], reverse=True)
        
        return {
            "popular_destinations": popular_destinations[:5],
            "trending_categories": ["adventure", "wellness", "cultural", "beach"],
            "peak_season_months": [11, 12, 1, 2, 3],
            "avg_trip_duration": 7.5,
            "most_requested_budget": "mid"
        }
