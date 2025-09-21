# 🌍 AI-Powered Trip Planner

A comprehensive, personalized trip planning application that uses AI algorithms to create end-to-end itineraries tailored to individual budgets, interests, and real-time conditions. Built with a modern **database-driven architecture** using FastAPI, SQLAlchemy, and intelligent recommendation algorithms.

## Quick Start

### Setup & Installation
```bash
# Clone the repository
git clone <repository-url>
cd travel_itenary

# Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate # For Linux/macOS (Windows: .venv\Scripts\activate)

# Install dependencies
pip install -r requirements.txt

# Initialize database from JSON data
python3 migrate_to_database.py

# Run the application
python3 main.py
```

### Access Points
- **Application**: http://localhost:8000
- **API Documentation**: http://localhost:8000/api/docs
- **Interactive API**: http://localhost:8000/api/redoc

## 🚀 Features

### Core Functionality
- **AI-Powered Recommendations**: Advanced filtering and scoring algorithms that match activities and accommodations to user preferences
- **Budget Optimization**: Intelligent cost allocation across accommodation, activities, food, and transport
- **Real-time Weather Integration**: Weather-aware recommendations and activity suggestions
- **Personalized Itineraries**: Day-by-day detailed plans with optimized activity scheduling
- **Multi-criteria Filtering**: Interest-based, budget-based, and constraint-satisfaction algorithms
- **Database-Driven**: Scalable SQLite database with clean repository pattern

### Technical Features
- **FastAPI Backend**: High-performance async API with automatic documentation
- **SQLAlchemy ORM**: Professional database operations with clean architecture
- **Repository Pattern**: Clean separation of concerns with service layer
- **Smart Fallbacks**: Database-first approach with mock_data fallbacks
- **JSON Data Management**: Portable data format for easy deployment
- **Advanced Scoring System**: Multi-factor recommendation engine with weighted scoring

## 🏗️ System Architecture

### High-Level Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   FastAPI       │    │   Database      │
│   (Static)      │◄──►│   Backend       │◄──►│   (SQLite)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │ Recommendation  │
                    │    Engine       │
                    │  (AI Scoring)   │
                    └─────────────────┘
```

### Backend Architecture (Clean Architecture Pattern)
```
┌─────────────────────────────────────────────────────────────┐
│                    API Layer (main.py)                     │
├─────────────────────────────────────────────────────────────┤
│                 Service Layer (services.py)                │
├─────────────────────────────────────────────────────────────┤
│            Repository Layer (repositories.py)              │
├─────────────────────────────────────────────────────────────┤
│              Database Layer (database.py)                  │
├─────────────────────────────────────────────────────────────┤
│                SQLite Database + JSON Data                 │
└─────────────────────────────────────────────────────────────┘

                    ┌─────────────────────┐
                    │ Recommendation      │
                    │ Engine              │
                    │ (recommendation_    │
                    │  engine.py)         │
                    └─────────────────────┘
```

## 📁 Project Structure

```
travel_itenary/
├── app/                           # Main application package
│   ├── __init__.py               # Package initialization
│   ├── main.py                   # FastAPI app & API endpoints
│   ├── models.py                 # Pydantic data models
│   ├── database.py               # SQLAlchemy models & DB connection
│   ├── repositories.py           # Data access layer
│   ├── services.py               # Business logic layer
│   ├── recommendation_engine.py  # AI recommendation algorithms
│   └── mock_data.py              # Fallback data & utility functions
├── data/
│   └── travel_data.json          # Complete portable dataset
├── static/                       # Frontend files
│   ├── index.html               # Main UI
│   ├── script.js                # Frontend logic
│   └── styles.css               # Styling
├── main.py                       # Application entry point
├── migrate_to_database.py        # Database setup script
├── requirements.txt              # Python dependencies
├── travel_planner.db            # SQLite database file
└── README.md                    # This file
```

## 🔧 How It Works

### 1. **Data Flow Architecture**

```
User Request → API Endpoint → Service Layer → Repository Layer → Database
                    ↓
            Recommendation Engine (with Database Session)
                    ↓
            AI Scoring & Filtering → Response
```

### 2. **Key Components Explained**

#### **API Layer (`app/main.py`)**
- **Purpose**: HTTP endpoints and request/response handling
- **Key Features**: 
  - FastAPI with automatic OpenAPI documentation
  - CORS middleware for frontend integration
  - Error handling and validation
- **Main Endpoints**: `/destinations`, `/trip/plan`, `/activities`, `/hotels`

#### **Service Layer (`app/services.py`)**
- **Purpose**: Business logic and orchestration
- **Key Classes**:
  - `TravelDataService`: Destination and content management
  - `TripPlanningService`: Trip recommendation orchestration
  - `WeatherService`: Weather condition analysis
  - `AnalyticsService`: Travel trends and insights

#### **Repository Layer (`app/repositories.py`)**
- **Purpose**: Data access abstraction
- **Key Class**: `DataRepository`
- **Features**: Clean database queries, data transformation

#### **Database Layer (`app/database.py`)**
- **Purpose**: SQLAlchemy models and database connection
- **Models**: `Destination`, `Hotel`, `Activity`, `TripTemplate`, `UserPreferenceTemplate`
- **Features**: Automatic table creation, session management

#### **Recommendation Engine (`app/recommendation_engine.py`)**
- **Purpose**: AI-powered trip recommendations
- **Key Features**:
  - **Database-First**: Uses live database data
  - **Smart Fallbacks**: Falls back to mock_data if database fails
  - **Multi-Factor Scoring**: Interest match, budget fit, weather, popularity
  - **Constraint Satisfaction**: Optimizes daily itineraries
- **Architecture**: 
  ```python
  TripRecommendationEngine(db_session)
  ├── _get_destinations_data()     # Database → mock_data fallback
  ├── _calculate_trip_cost()       # Budget calculations
  ├── _get_weather_info()          # Weather scoring
  └── generate_trip_recommendation() # Main orchestration
  ```

### 3. **Database Schema**

```sql
-- Core destination information
destinations (
    id, key, name, country, description,
    latitude, longitude, best_months,
    avg_temp_min, avg_temp_max, currency,
    budget_daily_budget, budget_daily_mid, budget_daily_luxury,
    popular_areas, categories
)

-- Hotel accommodations
hotels (
    id, destination_id, name, category, rating,
    location, description, price_budget, price_mid, price_luxury,
    amenities
)

-- Activities and experiences
activities (
    id, destination_id, name, type, duration, rating,
    description, best_time, location,
    cost_budget, cost_mid, cost_luxury, categories
)

-- Pre-configured trip styles
trip_templates (
    id, name, description, interests, budget_type,
    travel_style, accommodation_type, activity_intensity,
    recommended_destinations, duration_min, duration_max, highlights
)

-- User behavior patterns
user_preference_templates (
    id, profile_type, interests, budget_preference,
    accommodation_type, activity_intensity, group_size_preference
)
```

### 4. **AI Recommendation Algorithm**

The recommendation engine uses a sophisticated multi-factor scoring system:

```python
Overall Score = (
    Interest Match Score × 0.35 +      # How well it matches user interests
    Budget Fit Score × 0.25 +          # How well it fits the budget
    Weather Factor × 0.15 +            # Weather favorability
    Popularity Score × 0.15 +          # User ratings and reviews
    Activity Intensity × 0.10          # Matches user's activity level
)
```

**Scoring Components:**
- **Interest Matching**: Weighted scoring based on user interests vs item categories
- **Budget Optimization**: Intelligent cost allocation with budget type modifiers
- **Weather Integration**: Best months analysis for optimal travel timing
- **Constraint Satisfaction**: Daily itinerary optimization with time/cost/location constraints

## 🚀 Quick Start

### **Setup & Installation**
```bash
# Clone the repository
git clone <repository-url>
cd travel_itenary

# Install dependencies
pip install -r requirements.txt

# Initialize database from JSON data
python3 migrate_to_database.py

# Run the application
python3 main.py
```

### **Access Points**
- **Application**: http://localhost:8000
- **API Documentation**: http://localhost:8000/api/docs
- **Interactive API**: http://localhost:8000/api/redoc

## 🎯 API Reference

### **Core Endpoints**

#### **Destination Management**
```http
GET    /destinations                    # List all destinations
GET    /destinations/{key}              # Get destination details
POST   /destinations/suggest            # AI destination suggestions
```

#### **Trip Planning**
```http
POST   /trip/plan                       # Generate complete trip recommendation
POST   /trip/optimize                   # Optimize existing trip
GET    /trip/templates                  # Get pre-configured trip templates
```

#### **Content Discovery**
```http
GET    /activities/{destination}        # Get destination activities
GET    /hotels/{destination}            # Get destination hotels
```

#### **Analytics & Insights**
```http
GET    /analytics/popular-destinations  # Travel trends and analytics
GET    /user/preferences/templates      # User behavior templates
```

### **Example API Usage**

#### **Plan a Trip**
```bash
curl -X POST "http://localhost:8000/trip/plan" \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "delhi",
    "start_date": "2025-02-15",
    "end_date": "2025-02-20",
    "travelers": 2,
    "preferences": {
      "interests": ["cultural", "historical"],
      "budget_type": "mid",
      "travel_style": "cultural",
      "accommodation_type": "mid",
      "activity_intensity": "medium"
    }
  }'
```

#### **Get Destination Suggestions**
```bash
curl -X POST "http://localhost:8000/destinations/suggest?interests=cultural&interests=historical&budget_type=mid"
```

## 🗄️ Database Management

### **Initial Setup**
The `migrate_to_database.py` script handles complete database initialization:
- Creates SQLite database and tables
- Loads data from `data/travel_data.json`
- Populates all tables with sample data
- Provides detailed progress feedback

### **Data Management**
- **Portable Format**: All data stored in `data/travel_data.json`
- **Version Control Friendly**: JSON format works well with Git
- **Easy Updates**: Modify JSON file and re-run migration
- **Backup & Restore**: Simple file-based backup system

## 🔧 Customization & Extension

### **Adding New Destinations**
1. Update `data/travel_data.json` with new destination data
2. Run `python3 migrate_to_database.py` to update database
3. Restart the application

### **Extending Recommendation Algorithm**
```python
# In app/recommendation_engine.py
def __init__(self, db: Optional[Session] = None):
    self.interest_weights = {
        "your_new_interest": {"category1": 1.0, "category2": 0.8}
    }
```

### **Custom Scoring Factors**
```python
# Add new scoring method
def calculate_custom_score(self, item, preferences):
    # Your custom scoring logic
    return score

# Update overall scoring in score_activity()
overall_score = (
    interest_score * 0.30 +
    budget_score * 0.25 +
    weather_score * 0.15 +
    popularity_score * 0.15 +
    custom_score * 0.15      # Your new factor
)
```

## 🧪 Testing

### **API Testing**
```bash
# Test health endpoint
curl http://localhost:8000/health

# Test destinations
curl http://localhost:8000/destinations

# Test trip planning
curl -X POST http://localhost:8000/trip/plan -H "Content-Type: application/json" -d @test_request.json
```

### **Database Testing**
```bash
# Verify database setup
python3 -c "from app.database import SessionLocal; print('Database OK')"

# Check data integrity
python3 -c "from app.repositories import DataRepository; from app.database import SessionLocal; db = SessionLocal(); repo = DataRepository(db); print(f'Destinations: {len(repo.get_all_destinations())}')"
```

## 📈 Performance & Scalability

### **Current Performance**
- **Database**: SQLite for development, easily upgradeable to PostgreSQL
- **Caching**: In-memory caching for recommendation calculations
- **API**: FastAPI with async support for high concurrency
