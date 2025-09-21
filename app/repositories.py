"""
Repository pattern for data access.
Provides clean abstraction layer between business logic and database.
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from .database import Destination, Hotel, Activity, TripTemplate, UserPreferenceTemplate

class DestinationRepository:
    """Repository for destination-related database operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self) -> List[Destination]:
        """Get all destinations."""
        return self.db.query(Destination).all()
    
    def get_by_key(self, key: str) -> Optional[Destination]:
        """Get destination by key."""
        return self.db.query(Destination).filter(Destination.key == key).first()
    
    def get_by_categories(self, categories: List[str]) -> List[Destination]:
        """Get destinations that match any of the given categories."""
        destinations = []
        for dest in self.db.query(Destination).all():
            if any(cat in dest.categories for cat in categories):
                destinations.append(dest)
        return destinations
    
    def get_destination_data(self, key: str) -> Optional[Dict[str, Any]]:
        """Get comprehensive destination data."""
        dest = self.get_by_key(key)
        if not dest:
            return None
        
        return {
            "name": dest.name,
            "country": dest.country,
            "categories": dest.categories,
            "best_months": dest.best_months,
            "avg_temp_range": {"min": dest.avg_temp_min, "max": dest.avg_temp_max},
            "currency": dest.currency,
            "avg_daily_budget": {
                "budget": dest.budget_daily_budget,
                "mid": dest.budget_daily_mid,
                "luxury": dest.budget_daily_luxury
            },
            "description": dest.description,
            "popular_areas": dest.popular_areas,
            "coordinates": {"lat": dest.latitude, "lng": dest.longitude}
        }

class HotelRepository:
    """Repository for hotel-related database operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_destination(self, destination_key: str, budget_type: str = "mid") -> List[Hotel]:
        """Get hotels for a destination filtered by budget type."""
        dest = self.db.query(Destination).filter(Destination.key == destination_key).first()
        if not dest:
            return []
        
        hotels = self.db.query(Hotel).filter(Hotel.destination_id == dest.id).all()
        
        # Filter by budget type preference (hotels that support the budget type)
        filtered_hotels = []
        for hotel in hotels:
            if budget_type == "budget" and hotel.price_budget > 0:
                filtered_hotels.append(hotel)
            elif budget_type == "mid" and hotel.price_mid > 0:
                filtered_hotels.append(hotel)
            elif budget_type == "luxury" and hotel.price_luxury > 0:
                filtered_hotels.append(hotel)
        
        return filtered_hotels if filtered_hotels else hotels
    
    def get_hotels_data(self, destination_key: str) -> List[Dict[str, Any]]:
        """Get hotel data in the format expected by the recommendation engine."""
        hotels = self.get_by_destination(destination_key)
        
        return [{
            "name": hotel.name,
            "category": hotel.category,
            "rating": hotel.rating,
            "price_per_night": {
                "budget": hotel.price_budget,
                "mid": hotel.price_mid,
                "luxury": hotel.price_luxury
            },
            "amenities": hotel.amenities,
            "location": hotel.location,
            "description": hotel.description
        } for hotel in hotels]

class ActivityRepository:
    """Repository for activity-related database operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_destination(self, destination_key: str, interests: List[str] = None) -> List[Activity]:
        """Get activities for a destination filtered by interests."""
        dest = self.db.query(Destination).filter(Destination.key == destination_key).first()
        if not dest:
            return []
        
        activities = self.db.query(Activity).filter(Activity.destination_id == dest.id).all()
        
        if not interests:
            return activities
        
        # Filter activities based on user interests
        filtered_activities = []
        for activity in activities:
            if any(interest in activity.categories for interest in interests):
                filtered_activities.append(activity)
        
        return filtered_activities if filtered_activities else activities
    
    def get_activities_data(self, destination_key: str, interests: List[str] = None) -> List[Dict[str, Any]]:
        """Get activity data in the format expected by the recommendation engine."""
        activities = self.get_by_destination(destination_key, interests)
        
        return [{
            "name": activity.name,
            "type": activity.type,
            "duration": activity.duration,
            "cost": {
                "budget": activity.cost_budget,
                "mid": activity.cost_mid,
                "luxury": activity.cost_luxury
            },
            "rating": activity.rating,
            "description": activity.description,
            "best_time": activity.best_time,
            "location": activity.location,
            "categories": activity.categories
        } for activity in activities]

class TripTemplateRepository:
    """Repository for trip template operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self) -> List[TripTemplate]:
        """Get all trip templates."""
        return self.db.query(TripTemplate).all()
    
    def get_templates_data(self) -> List[Dict[str, Any]]:
        """Get trip templates in API format."""
        templates = self.get_all()
        
        return [{
            "name": template.name,
            "description": template.description,
            "preferences": {
                "interests": template.interests,
                "budget_type": template.budget_type,
                "travel_style": template.travel_style,
                "accommodation_type": template.accommodation_type,
                "activity_intensity": template.activity_intensity
            },
            "recommended_destinations": template.recommended_destinations,
            "duration_range": [template.duration_min, template.duration_max],
            "highlights": template.highlights
        } for template in templates]

class UserPreferenceTemplateRepository:
    """Repository for user preference template operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self) -> List[UserPreferenceTemplate]:
        """Get all user preference templates."""
        return self.db.query(UserPreferenceTemplate).all()
    
    def get_by_profile_type(self, profile_type: str) -> Optional[UserPreferenceTemplate]:
        """Get user preference template by profile type."""
        return self.db.query(UserPreferenceTemplate).filter(
            UserPreferenceTemplate.profile_type == profile_type
        ).first()
    
    def get_templates_data(self) -> List[Dict[str, Any]]:
        """Get user preference templates in API format."""
        templates = self.get_all()
        
        return [{
            "profile_type": template.profile_type,
            "interests": template.interests,
            "budget_preference": template.budget_preference,
            "accommodation_type": template.accommodation_type,
            "activity_intensity": template.activity_intensity,
            "group_size_preference": template.group_size_preference
        } for template in templates]

class DataRepository:
    """Unified repository providing access to all data repositories."""
    
    def __init__(self, db: Session):
        self.db = db
        self.destinations = DestinationRepository(db)
        self.hotels = HotelRepository(db)
        self.activities = ActivityRepository(db)
        self.trip_templates = TripTemplateRepository(db)
        self.user_preferences = UserPreferenceTemplateRepository(db)
