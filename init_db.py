#!/usr/bin/env python3
"""
Database initialization script for deployment.
Creates tables and populates with data from JSON file.
"""

import json
import sys
from pathlib import Path
from sqlalchemy.orm import Session

def init_database():
    """Initialize database with data from JSON file."""
    try:
        # Import after ensuring the app directory is in path
        from app.database import SessionLocal, create_tables
        from app.database import Destination, Hotel, Activity, TripTemplate, UserPreferenceTemplate
        
        print("🗄️ Creating database tables...")
        create_tables()
        print("✅ Database tables created")
        
        # Load data from JSON
        json_path = Path(__file__).parent / "data" / "travel_data.json"
        if not json_path.exists():
            print("❌ travel_data.json not found")
            return False
            
        with open(json_path, 'r') as f:
            data = json.load(f)
        
        print(f"📖 Loaded data: {len(data['destinations'])} destinations")
        
        # Get database session
        db = SessionLocal()
        
        try:
            # Clear existing data
            print("🗑️ Clearing existing data...")
            db.query(UserPreferenceTemplate).delete()
            db.query(TripTemplate).delete()
            db.query(Activity).delete()
            db.query(Hotel).delete()
            db.query(Destination).delete()
            db.commit()
            
            # Add destinations
            print("📍 Adding destinations...")
            for dest_data in data["destinations"]:
                destination = Destination(
                    key=dest_data["key"],
                    name=dest_data["name"],
                    country=dest_data["country"],
                    description=dest_data["description"],
                    latitude=dest_data["latitude"],
                    longitude=dest_data["longitude"],
                    best_months=dest_data["best_months"],
                    avg_temp_min=dest_data["avg_temp_min"],
                    avg_temp_max=dest_data["avg_temp_max"],
                    currency=dest_data["currency"],
                    budget_daily_budget=dest_data["budget_daily_budget"],
                    budget_daily_mid=dest_data["budget_daily_mid"],
                    budget_daily_luxury=dest_data["budget_daily_luxury"],
                    popular_areas=dest_data["popular_areas"],
                    categories=dest_data["categories"]
                )
                db.add(destination)
            db.commit()
            
            # Get destination mappings for foreign keys
            destinations = {dest.key: dest.id for dest in db.query(Destination).all()}
            
            # Add hotels
            if "hotels" in data:
                print("🏨 Adding hotels...")
                hotel_count = 0
                for dest_key, hotels_list in data["hotels"].items():
                    if dest_key in destinations:
                        for hotel_data in hotels_list:
                            hotel = Hotel(
                                name=hotel_data["name"],
                                destination_id=destinations[dest_key],
                                category=hotel_data["category"],
                                rating=hotel_data["rating"],
                                location=hotel_data["location"],
                                description=hotel_data["description"],
                                price_budget=hotel_data["price_per_night"]["budget"],
                                price_mid=hotel_data["price_per_night"]["mid"],
                                price_luxury=hotel_data["price_per_night"]["luxury"],
                                amenities=hotel_data["amenities"]
                            )
                            db.add(hotel)
                            hotel_count += 1
                db.commit()
                print(f"✅ Added {hotel_count} hotels")
            
            # Add activities
            if "activities" in data:
                print("🎯 Adding activities...")
                activity_count = 0
                for dest_key, activities_list in data["activities"].items():
                    if dest_key in destinations:
                        for activity_data in activities_list:
                            activity = Activity(
                                name=activity_data["name"],
                                destination_id=destinations[dest_key],
                                type=activity_data["type"],
                                duration=activity_data["duration"],
                                rating=activity_data["rating"],
                                description=activity_data["description"],
                                best_time=activity_data["best_time"],
                                location=activity_data["location"],
                                cost_budget=activity_data["cost"]["budget"],
                                cost_mid=activity_data["cost"]["mid"],
                                cost_luxury=activity_data["cost"]["luxury"],
                                categories=activity_data["categories"]
                            )
                            db.add(activity)
                            activity_count += 1
                db.commit()
                print(f"✅ Added {activity_count} activities")
            
            # Add trip templates
            print("📋 Adding trip templates...")
            for template_data in data["trip_templates"]:
                template = TripTemplate(
                    name=template_data["name"],
                    description=template_data["description"],
                    interests=template_data["interests"],
                    budget_type=template_data["budget_type"],
                    travel_style=template_data["travel_style"],
                    accommodation_type=template_data["accommodation_type"],
                    activity_intensity=template_data["activity_intensity"],
                    recommended_destinations=template_data["recommended_destinations"],
                    duration_min=template_data["duration_min"],
                    duration_max=template_data["duration_max"],
                    highlights=template_data["highlights"]
                )
                db.add(template)
            db.commit()
            
            # Add user preference templates
            print("👤 Adding user preference templates...")
            for template_data in data["user_preference_templates"]:
                template = UserPreferenceTemplate(
                    profile_type=template_data["profile_type"],
                    interests=template_data["interests"],
                    budget_preference=template_data["budget_preference"],
                    accommodation_type=template_data["accommodation_type"],
                    activity_intensity=template_data["activity_intensity"],
                    group_size_preference=template_data["group_size_preference"]
                )
                db.add(template)
            db.commit()
            
            print("🎉 Database initialization completed successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Database initialization failed: {e}")
            db.rollback()
            return False
        finally:
            db.close()
            
    except Exception as e:
        print(f"❌ Failed to initialize database: {e}")
        return False

if __name__ == "__main__":
    success = init_database()
    sys.exit(0 if success else 1)
