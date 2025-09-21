"""
AI-powered recommendation engine for personalized trip planning.
Implements sophisticated filtering, scoring, and optimization algorithms.
"""

import random
import math
from typing import List, Dict, Any, Tuple
from datetime import datetime, timedelta
from collections import defaultdict

from .models import (
    TripRequest, UserPreferences, TripRecommendation, Trip, Itinerary, 
    VisitPlace, Event, Hotel, WeatherInfo, CostBreakdown, RecommendationScore,
    EnhancedActivity, EnhancedHotel, DestinationSuggestion
)
from sqlalchemy.orm import Session
from typing import Optional


class TripRecommendationEngine:
    """
    Advanced AI recommendation engine for personalized trip planning.
    Uses multiple algorithms for scoring, filtering, and optimization.
    Now supports both database-driven and fallback approaches.
    """
    
    def __init__(self, db: Optional[Session] = None):
        self.db = db
        self.interest_weights = {
            "adventure": {"adventure": 1.0, "nature": 0.8, "sports": 0.7},
            "cultural": {"cultural": 1.0, "historical": 0.9, "educational": 0.8},
            "relaxation": {"relaxation": 1.0, "wellness": 0.9, "beach": 0.8},
            "culinary": {"culinary": 1.0, "food": 1.0, "cultural": 0.6},
            "nature": {"nature": 1.0, "adventure": 0.7, "photography": 0.8},
            "historical": {"historical": 1.0, "cultural": 0.9, "educational": 0.8},
            "urban": {"urban": 1.0, "entertainment": 0.8, "shopping": 0.7},
            "spiritual": {"spiritual": 1.0, "cultural": 0.7, "wellness": 0.6}
        }
    
    def _get_destinations_data(self) -> Dict[str, Any]:
        """Get destinations data from database or fallback to mock_data."""
        if self.db:
            try:
                from .repositories import DataRepository
                repo = DataRepository(self.db)
                destinations = repo.get_all_destinations()
                # Convert to the format expected by the recommendation engine
                destinations_dict = {}
                for dest in destinations:
                    destinations_dict[dest.key] = {
                        "name": dest.name,
                        "country": dest.country,
                        "categories": dest.categories,
                        "description": dest.description,
                        "best_months": dest.best_months,
                        "avg_temp_range": {"min": dest.avg_temp_min, "max": dest.avg_temp_max},
                        "currency": dest.currency,
                        "avg_daily_budget": {
                            "budget": dest.budget_daily_budget,
                            "mid": dest.budget_daily_mid,
                            "luxury": dest.budget_daily_luxury
                        },
                        "popular_areas": dest.popular_areas,
                        "coordinates": {"lat": dest.latitude, "lng": dest.longitude}
                    }
                return destinations_dict
            except Exception as e:
                print(f"Warning: Database query failed, falling back to mock_data: {e}")
        
        # Fallback to mock_data
        from .mock_data import DESTINATIONS
        return DESTINATIONS
    
    def _get_weather_info(self, destination: str, travel_month: int) -> WeatherInfo:
        """Get weather information from database or fallback to mock_data."""
        try:
            # Simple weather info based on destination data
            destinations_data = self._get_destinations_data()
            dest_data = destinations_data.get(destination)
            
            if dest_data and "best_months" in dest_data:
                is_favorable = travel_month in dest_data["best_months"]
                condition = "sunny" if is_favorable else "cloudy"
                temp_range = dest_data.get("avg_temp_range", {"min": 20, "max": 30})
                
                return WeatherInfo(
                    condition=condition,
                    temperature=f"{temp_range['min']}-{temp_range['max']}°C",
                    is_favorable=is_favorable,
                    description=f"Weather is {'favorable' if is_favorable else 'acceptable'} for travel"
                )
        except Exception as e:
            print(f"Warning: Weather info generation failed: {e}")
        
        # Fallback to mock_data
        try:
            from .mock_data import get_weather_conditions
            weather_data = get_weather_conditions(destination, travel_month)
            return WeatherInfo(
                condition=weather_data["condition"],
                temperature=weather_data["temperature"],
                is_favorable=weather_data["is_favorable"],
                description=weather_data["description"]
            )
        except Exception:
            # Default weather info
            return WeatherInfo(
                condition="partly_cloudy",
                temperature="20-25°C",
                is_favorable=True,
                description="Weather conditions are generally favorable"
            )
    
    def _calculate_trip_cost(self, destination: str, days: int, travelers: int, budget_type: str) -> Dict[str, float]:
        """Calculate trip cost using database data or fallback to mock_data."""
        try:
            # Try to calculate using database data
            destinations_data = self._get_destinations_data()
            dest_data = destinations_data.get(destination)
            
            if dest_data and "avg_daily_budget" in dest_data:
                daily_budget = dest_data["avg_daily_budget"].get(budget_type, dest_data["avg_daily_budget"]["mid"])
                
                # Simple cost breakdown calculation
                accommodation_cost = (daily_budget * 0.4) * days * travelers  # 40% for accommodation
                activity_cost = (daily_budget * 0.3) * days * travelers       # 30% for activities
                food_cost = (daily_budget * 0.2) * days * travelers           # 20% for food
                transport_cost = (daily_budget * 0.1) * days * travelers      # 10% for local transport
                
                total_cost = accommodation_cost + activity_cost + food_cost + transport_cost
                
                return {
                    "accommodation": accommodation_cost,
                    "activities": activity_cost,
                    "food": food_cost,
                    "transport": transport_cost,
                    "total": total_cost,
                    "per_person": total_cost / travelers,
                    "per_day": total_cost / days
                }
        except Exception as e:
            print(f"Warning: Database cost calculation failed, falling back to mock_data: {e}")
        
        # Fallback to mock_data
        try:
            from .mock_data import calculate_trip_cost
            return calculate_trip_cost(destination, days, travelers, budget_type)
        except Exception:
            # Default cost calculation
            base_daily_cost = {"budget": 2000, "mid": 4000, "luxury": 8000}
            daily_budget = base_daily_cost.get(budget_type, 4000)
            
            accommodation_cost = (daily_budget * 0.4) * days * travelers
            activity_cost = (daily_budget * 0.3) * days * travelers
            food_cost = (daily_budget * 0.2) * days * travelers
            transport_cost = (daily_budget * 0.1) * days * travelers
            total_cost = accommodation_cost + activity_cost + food_cost + transport_cost
            
            return {
                "accommodation": accommodation_cost,
                "activities": activity_cost,
                "food": food_cost,
                "transport": transport_cost,
                "total": total_cost,
                "per_person": total_cost / travelers,
                "per_day": total_cost / days
            }
    
    def calculate_interest_match_score(self, user_interests: List[str], item_categories: List[str]) -> float:
        """
        Calculate how well an item matches user interests using weighted scoring.
        """
        if not user_interests or not item_categories:
            return 5.0  # Neutral score
        
        total_score = 0.0
        max_possible_score = 0.0
        
        for user_interest in user_interests:
            interest_weights = self.interest_weights.get(user_interest, {user_interest: 1.0})
            max_possible_score += max(interest_weights.values())
            
            for category in item_categories:
                if category in interest_weights:
                    total_score += interest_weights[category]
                elif category == user_interest:
                    total_score += 1.0
        
        # Normalize to 0-10 scale
        if max_possible_score > 0:
            normalized_score = (total_score / max_possible_score) * 10
            return min(10.0, normalized_score)
        
        return 5.0
    
    def calculate_budget_fit_score(self, item_cost: float, user_budget: float, budget_type: str) -> float:
        """
        Calculate how well an item fits within the user's budget.
        """
        if user_budget <= 0:
            return 8.0  # Default good score if no budget specified
        
        cost_ratio = item_cost / user_budget
        
        # Budget type modifiers
        budget_multipliers = {"budget": 0.7, "mid": 1.0, "luxury": 1.5}
        adjusted_ratio = cost_ratio / budget_multipliers.get(budget_type, 1.0)
        
        if adjusted_ratio <= 0.5:
            return 10.0  # Excellent fit
        elif adjusted_ratio <= 0.8:
            return 8.0   # Good fit
        elif adjusted_ratio <= 1.0:
            return 6.0   # Acceptable fit
        elif adjusted_ratio <= 1.2:
            return 4.0   # Slightly over budget
        else:
            return 2.0   # Over budget
    
    def calculate_weather_factor_score(self, destination: str, travel_month: int) -> float:
        """
        Calculate weather favorability score for the destination and time.
        """
        # Try to get weather info from database first
        if self.db:
            try:
                destinations_data = self._get_destinations_data()
                dest_data = destinations_data.get(destination)
                if dest_data and "best_months" in dest_data:
                    # Simple weather scoring based on best months
                    if travel_month in dest_data["best_months"]:
                        return 9.0
                    else:
                        return 5.0
            except Exception as e:
                print(f"Warning: Database weather query failed, falling back to mock_data: {e}")
        
        # Fallback to mock_data
        try:
            from .mock_data import get_weather_conditions
            weather_info = get_weather_conditions(destination, travel_month)
            
            if weather_info["is_favorable"]:
                return 9.0
            elif weather_info["condition"] in ["sunny", "partly_cloudy"]:
                return 7.0
            elif weather_info["condition"] == "cloudy":
                return 6.0
            else:
                return 4.0
        except Exception:
            # Default weather score if all else fails
            return 6.0
    
    def score_activity(self, activity: Dict[str, Any], preferences: UserPreferences, 
                      destination: str, travel_month: int, daily_budget: float) -> RecommendationScore:
        """
        Score an activity based on user preferences and contextual factors.
        """
        # Interest match score
        interest_score = self.calculate_interest_match_score(
            preferences.interests, activity.get("categories", [])
        )
        
        # Budget fit score
        activity_cost = activity["cost"].get(preferences.budget_type.value, activity["cost"]["mid"])
        budget_score = self.calculate_budget_fit_score(activity_cost, daily_budget * 0.3, preferences.budget_type.value)
        
        # Weather factor
        weather_score = self.calculate_weather_factor_score(destination, travel_month)
        
        # Popularity score (based on rating)
        popularity_score = (activity.get("rating", 4.0) / 5.0) * 10
        
        # Activity intensity matching
        intensity_preferences = {"low": 1, "medium": 2, "high": 3}
        activity_intensity = len(activity.get("categories", [])) + activity.get("duration", 2)
        user_intensity = intensity_preferences.get(preferences.activity_intensity, 2)
        
        intensity_match = 10 - abs(activity_intensity - user_intensity * 2)
        intensity_match = max(0, min(10, intensity_match))
        
        # Calculate overall score with weights
        overall_score = (
            interest_score * 0.35 +
            budget_score * 0.25 +
            weather_score * 0.15 +
            popularity_score * 0.15 +
            intensity_match * 0.10
        )
        
        return RecommendationScore(
            overall_score=round(overall_score, 2),
            interest_match=round(interest_score, 2),
            budget_fit=round(budget_score, 2),
            weather_factor=round(weather_score, 2),
            popularity_score=round(popularity_score, 2)
        )
    
    def score_hotel(self, hotel: Dict[str, Any], preferences: UserPreferences, 
                   daily_budget: float) -> RecommendationScore:
        """
        Score a hotel based on user preferences and budget.
        """
        # Budget fit score
        hotel_cost = hotel["price_per_night"].get(preferences.budget_type.value, hotel["price_per_night"]["mid"])
        budget_score = self.calculate_budget_fit_score(hotel_cost, daily_budget * 0.5, preferences.budget_type.value)
        
        # Accommodation type matching
        accommodation_match = 10.0 if hotel["category"] == preferences.accommodation_type.value else 6.0
        
        # Amenity matching based on interests
        amenity_score = 5.0
        if "spa" in hotel.get("amenities", []) and "wellness" in preferences.interests:
            amenity_score += 2.0
        if "gym" in hotel.get("amenities", []) and "adventure" in preferences.interests:
            amenity_score += 1.5
        if "restaurant" in hotel.get("amenities", []) and "culinary" in preferences.interests:
            amenity_score += 1.5
        
        amenity_score = min(10.0, amenity_score)
        
        # Popularity score (based on rating)
        popularity_score = (hotel.get("rating", 4.0) / 5.0) * 10
        
        # Overall score
        overall_score = (
            budget_score * 0.4 +
            accommodation_match * 0.3 +
            amenity_score * 0.2 +
            popularity_score * 0.1
        )
        
        return RecommendationScore(
            overall_score=round(overall_score, 2),
            interest_match=round(amenity_score, 2),
            budget_fit=round(budget_score, 2),
            weather_factor=8.0,  # Hotels are weather-independent
            popularity_score=round(popularity_score, 2)
        )
    
    def optimize_daily_itinerary(self, activities: List[Dict[str, Any]], 
                                preferences: UserPreferences, daily_budget: float) -> List[Dict[str, Any]]:
        """
        Optimize daily itinerary using constraint satisfaction and scoring.
        """
        # Score all activities
        scored_activities = []
        for activity in activities:
            score = self.score_activity(activity, preferences, "paris", 6, daily_budget)  # Default values
            activity_with_score = activity.copy()
            activity_with_score["score"] = score.overall_score
            scored_activities.append(activity_with_score)
        
        # Sort by score
        scored_activities.sort(key=lambda x: x["score"], reverse=True)
        
        # Select activities based on constraints
        selected_activities = []
        total_cost = 0
        total_duration = 0
        used_locations = set()
        
        # Activity intensity constraints
        intensity_limits = {"low": 2, "medium": 3, "high": 4}
        max_activities = intensity_limits.get(preferences.activity_intensity, 3)
        
        for activity in scored_activities:
            activity_cost = activity["cost"].get(preferences.budget_type.value, activity["cost"]["mid"])
            
            # Check constraints
            if (len(selected_activities) >= max_activities or
                total_cost + activity_cost > daily_budget * 0.6 or
                total_duration + activity["duration"] > 10 or
                activity["location"] in used_locations):
                continue
            
            selected_activities.append(activity)
            total_cost += activity_cost
            total_duration += activity["duration"]
            used_locations.add(activity["location"])
        
        return selected_activities
    
    def generate_trip_recommendation(self, request: TripRequest, destination_data: Dict[str, Any] = None, 
                                   hotels: List[Dict[str, Any]] = None, activities: List[Dict[str, Any]] = None,
                                   weather_info: Dict[str, Any] = None) -> TripRecommendation:
        """
        Generate a complete personalized trip recommendation.
        Can work with provided data (new architecture) or fetch data internally (legacy).
        """
        # Support both new architecture (with provided data) and legacy architecture
        if destination_data is None:
            # Try database first, then fallback to mock_data
            destinations_data = self._get_destinations_data()
            destination_data = destinations_data.get(request.destination)
            if not destination_data:
                raise ValueError(f"Destination '{request.destination}' not found")
        
        if hotels is None:
            # Fallback to mock_data for hotels (database integration would need more work)
            from .mock_data import get_hotels_for_destination
            hotels = get_hotels_for_destination(request.destination, request.preferences.budget_type.value)
        
        if activities is None:
            # Fallback to mock_data for activities (database integration would need more work)
            from .mock_data import get_activities_for_destination
            activities = get_activities_for_destination(request.destination, request.preferences.interests)
        
        if weather_info is None:
            start_date = datetime.fromisoformat(request.start_date)
            weather_info = self._get_weather_info(request.destination, start_date.month)
        else:
            # Convert dict to expected format
            is_favorable = weather_info.get("is_good_weather", True)
            weather_info = WeatherInfo(
                temperature=weather_info.get("temperature", 25),
                condition=weather_info.get("condition", "sunny"),
                is_favorable=is_favorable,
                recommendation="Great weather for travel!" if is_favorable else "Pack accordingly for weather conditions"
            )
        
        # Calculate trip duration
        start_date = datetime.fromisoformat(request.start_date)
        end_date = datetime.fromisoformat(request.end_date)
        duration = (end_date - start_date).days
        travel_month = start_date.month
        
        # Get cost breakdown
        cost_data = self._calculate_trip_cost(request.destination, duration, request.travelers, request.preferences.budget_type.value)
        cost_breakdown = CostBreakdown(**cost_data)
        
        # Score and enhance hotels
        enhanced_hotels = []
        daily_budget = cost_breakdown.per_day / request.travelers
        
        for hotel in hotels:
            score = self.score_hotel(hotel, request.preferences, daily_budget)
            enhanced_hotel = EnhancedHotel(**hotel, recommendation_score=score)
            enhanced_hotels.append(enhanced_hotel)
        
        enhanced_hotels.sort(key=lambda x: x.recommendation_score.overall_score, reverse=True)
        
        # Score activities (activities already provided)
        enhanced_activities = []
        
        for activity in activities:
            score = self.score_activity(activity, request.preferences, request.destination, travel_month, daily_budget)
            enhanced_activity = EnhancedActivity(**activity, recommendation_score=score)
            enhanced_activities.append(enhanced_activity)
        
        enhanced_activities.sort(key=lambda x: x.recommendation_score.overall_score, reverse=True)
        
        # Generate daily itineraries
        itineraries = []
        for day in range(duration):
            current_date = start_date + timedelta(days=day)
            
            # Optimize activities for this day
            daily_activities = self.optimize_daily_itinerary(activities, request.preferences, daily_budget)
            
            # Create visit places from activities
            places = []
            for i, activity in enumerate(daily_activities):
                activity_cost = activity["cost"].get(request.preferences.budget_type.value, activity["cost"]["mid"])
                
                # Create events within the place
                events = [Event(
                    name=activity["name"],
                    time=activity["best_time"],
                    description=activity["description"],
                    cost=activity_cost
                )]
                
                place = VisitPlace(
                    name=activity["location"],
                    times=f"{activity['best_time']} ({activity['duration']}h)",
                    description=f"Visit to {activity['location']} for {activity['name']}",
                    cost_per_visitplace=activity_cost,
                    events=events
                )
                places.append(place)
            
            itinerary = Itinerary(
                date=current_date.strftime("%Y-%m-%d"),
                number_of_persons=request.travelers,
                places=places
            )
            itineraries.append(itinerary)
        
        # Select best hotel
        selected_hotels = []
        if enhanced_hotels:
            best_hotel = enhanced_hotels[0]
            hotel = Hotel(
                name=best_hotel.name,
                check_in=request.start_date,
                check_out=request.end_date,
                cost_per_night=best_hotel.price_per_night[request.preferences.budget_type.value],
                address=best_hotel.location
            )
            selected_hotels.append(hotel)
        
        # Create trip
        trip = Trip(
            destination=destination_data["name"],
            start_date=request.start_date,
            end_date=request.end_date,
            travelers=request.travelers,
            itinerary=itineraries,
            hotels=selected_hotels,
            total_budget=cost_breakdown.total
        )
        
        # Generate personalization notes
        personalization_notes = []
        if request.preferences.interests:
            personalization_notes.append(f"Customized for your interests: {', '.join(request.preferences.interests)}")
        
        if request.preferences.budget_type.value != "mid":
            personalization_notes.append(f"Optimized for {request.preferences.budget_type.value} budget preferences")
        
        if weather_info.is_favorable:
            personalization_notes.append("Great weather conditions for your travel dates!")
        else:
            personalization_notes.append("Weather considerations have been factored into recommendations")
        
        # Calculate confidence score
        avg_activity_score = sum(a.recommendation_score.overall_score for a in enhanced_activities[:5]) / min(5, len(enhanced_activities))
        avg_hotel_score = sum(h.recommendation_score.overall_score for h in enhanced_hotels[:3]) / min(3, len(enhanced_hotels))
        weather_factor = 9.0 if weather_info.is_favorable else 6.0
        
        confidence_score = (avg_activity_score * 0.5 + avg_hotel_score * 0.3 + weather_factor * 0.2)
        
        return TripRecommendation(
            trip=trip,
            weather_info=weather_info,
            cost_breakdown=cost_breakdown,
            recommended_hotels=enhanced_hotels[:3],
            recommended_activities=enhanced_activities[:10],
            personalization_notes=personalization_notes,
            confidence_score=round(confidence_score, 2)
        )
    
    def suggest_destinations(self, preferences: UserPreferences, 
                           budget_range: Tuple[float, float] = None) -> List[DestinationSuggestion]:
        """
        Suggest destinations based on user preferences and budget.
        """
        suggestions = []
        destinations_data = self._get_destinations_data()
        
        for dest_key, dest_data in destinations_data.items():
            # Calculate interest match
            interest_score = self.calculate_interest_match_score(
                preferences.interests, dest_data["categories"]
            )
            
            # Budget compatibility
            daily_budget = dest_data["avg_daily_budget"].get(preferences.budget_type.value, 100)
            budget_score = 10.0
            if budget_range:
                min_budget, max_budget = budget_range
                if daily_budget < min_budget * 0.8:
                    budget_score = 6.0
                elif daily_budget > max_budget * 1.2:
                    budget_score = 4.0
            
            # Overall match score
            match_score = (interest_score * 0.7 + budget_score * 0.3)
            
            # Generate reasons
            reasons = []
            if interest_score >= 8.0:
                matching_interests = [cat for cat in dest_data["categories"] if cat in preferences.interests]
                if matching_interests:
                    reasons.append(f"Perfect for {', '.join(matching_interests)} enthusiasts")
            
            if budget_score >= 8.0:
                reasons.append(f"Great value for {preferences.budget_type.value} travelers")
            
            if dest_data.get("best_months"):
                reasons.append(f"Best visited in months: {', '.join(map(str, dest_data['best_months']))}")
            
            suggestion = DestinationSuggestion(
                name=dest_data["name"],
                country=dest_data["country"],
                description=dest_data["description"],
                categories=dest_data["categories"],
                best_months=dest_data["best_months"],
                avg_daily_budget=dest_data["avg_daily_budget"],
                match_score=round(match_score, 2),
                reasons=reasons
            )
            suggestions.append(suggestion)
        
        # Sort by match score
        suggestions.sort(key=lambda x: x.match_score, reverse=True)
        return suggestions


# Global instance
recommendation_engine = TripRecommendationEngine()
