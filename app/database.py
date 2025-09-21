"""
Database configuration and models for the AI-powered trip planner.
Uses SQLAlchemy ORM with SQLite for development and easy deployment.
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, Text, JSON, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.dialects.sqlite import JSON as SQLiteJSON
import os

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./travel_planner.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Association tables for many-to-many relationships
destination_categories = Table(
    'destination_categories',
    Base.metadata,
    Column('destination_id', Integer, ForeignKey('destinations.id')),
    Column('category', String(50))
)

activity_categories = Table(
    'activity_categories',
    Base.metadata,
    Column('activity_id', Integer, ForeignKey('activities.id')),
    Column('category', String(50))
)

hotel_amenities = Table(
    'hotel_amenities',
    Base.metadata,
    Column('hotel_id', Integer, ForeignKey('hotels.id')),
    Column('amenity', String(50))
)

class Destination(Base):
    __tablename__ = "destinations"
    
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(50), unique=True, index=True)  # e.g., "delhi", "mumbai"
    name = Column(String(100), nullable=False)
    country = Column(String(50), nullable=False)
    description = Column(Text)
    
    # Geographic data
    latitude = Column(Float)
    longitude = Column(Float)
    
    # Climate data
    best_months = Column(JSON)  # List of month numbers
    avg_temp_min = Column(Integer)
    avg_temp_max = Column(Integer)
    
    # Budget information
    currency = Column(String(10), default="INR")
    budget_daily_budget = Column(Integer)
    budget_daily_mid = Column(Integer)
    budget_daily_luxury = Column(Integer)
    
    # Popular areas
    popular_areas = Column(JSON)  # List of area names
    
    # Relationships
    hotels = relationship("Hotel", back_populates="destination")
    activities = relationship("Activity", back_populates="destination")
    
    # Categories (many-to-many)
    categories = Column(JSON)  # Store as JSON for simplicity

class Hotel(Base):
    __tablename__ = "hotels"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    destination_id = Column(Integer, ForeignKey("destinations.id"))
    
    # Hotel details
    category = Column(String(20))  # budget, mid, luxury
    rating = Column(Float)
    location = Column(String(100))
    description = Column(Text)
    
    # Pricing
    price_budget = Column(Integer)
    price_mid = Column(Integer)
    price_luxury = Column(Integer)
    
    # Amenities
    amenities = Column(JSON)  # List of amenities
    
    # Relationships
    destination = relationship("Destination", back_populates="hotels")

class Activity(Base):
    __tablename__ = "activities"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    destination_id = Column(Integer, ForeignKey("destinations.id"))
    
    # Activity details
    type = Column(String(50))  # historical, adventure, cultural, etc.
    duration = Column(Integer)  # in hours
    rating = Column(Float)
    description = Column(Text)
    best_time = Column(String(20))  # morning, afternoon, evening
    location = Column(String(100))
    
    # Pricing
    cost_budget = Column(Integer)
    cost_mid = Column(Integer)
    cost_luxury = Column(Integer)
    
    # Categories
    categories = Column(JSON)  # List of categories
    
    # Relationships
    destination = relationship("Destination", back_populates="activities")

class TripTemplate(Base):
    __tablename__ = "trip_templates"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    
    # Template preferences
    interests = Column(JSON)  # List of interests
    budget_type = Column(String(20))
    travel_style = Column(String(20))
    accommodation_type = Column(String(20))
    activity_intensity = Column(String(20))
    
    # Recommendations
    recommended_destinations = Column(JSON)  # List of destination keys
    duration_min = Column(Integer)
    duration_max = Column(Integer)
    highlights = Column(JSON)  # List of highlights

class UserPreferenceTemplate(Base):
    __tablename__ = "user_preference_templates"
    
    id = Column(Integer, primary_key=True, index=True)
    profile_type = Column(String(50), unique=True)
    interests = Column(JSON)
    budget_preference = Column(String(20))
    accommodation_type = Column(String(20))
    activity_intensity = Column(String(20))
    group_size_preference = Column(String(20))

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create tables
def create_tables():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_tables()
    print("Database tables created successfully!")
