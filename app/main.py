"""
FastAPI backend for AI-powered trip planner.
Clean, database-driven architecture with repository pattern.
"""

from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional, Dict, Any
import traceback
from sqlalchemy.orm import Session
from pathlib import Path

from .models import TripRequest, TripRecommendation, EnhancedActivity, EnhancedHotel, BudgetType
from .database import get_db, create_tables
from .services import TravelDataService, TripPlanningService, AnalyticsService

# Initialize FastAPI app
app = FastAPI(
    title="AI-Powered Trip Planner",
    description="Personalized trip planning with AI recommendations, budget optimization, and real-time conditions",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
static_path = Path(__file__).parent.parent / "static"
if static_path.exists():
    app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

# Startup event
@app.on_event("startup")
async def startup_event():
    print("🌍 Starting AI-Powered Trip Planner v2.0...")
    print("📍 Server will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/api/docs")
    print("🎯 Frontend Interface: http://localhost:8000")
    
    # Create database tables
    create_tables()
    print("🗄️ Database initialized successfully")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main frontend page."""
    html_path = Path(__file__).parent.parent / "static" / "index.html"
    if html_path.exists():
        return HTMLResponse(content=html_path.read_text(), status_code=200)
    
    # Fallback HTML
    return HTMLResponse(content="""
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Trip Planner v2.0</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #2c3e50; text-align: center; }
            .api-link { display: inline-block; margin: 10px; padding: 10px 20px; background: #3498db; color: white; text-decoration: none; border-radius: 5px; }
            .api-link:hover { background: #2980b9; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🌍 AI-Powered Trip Planner v2.0</h1>
            <p>Database-driven architecture with clean separation of concerns!</p>
            <a href="/api/docs" class="api-link">📚 API Documentation</a>
            <a href="/destinations" class="api-link">🏛️ Available Destinations</a>
            <a href="/health" class="api-link">💚 Health Check</a>
        </div>
    </body>
    </html>
    """, status_code=200)

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "AI Trip Planner",
        "version": "2.0.0",
        "architecture": "Database-driven with Repository Pattern",
        "features": [
            "SQLAlchemy ORM with SQLite",
            "Repository Pattern",
            "Service Layer Architecture",
            "Clean Data Separation",
            "AI-powered recommendations",
            "Budget optimization"
        ]
    }

# === DESTINATION ENDPOINTS ===

@app.get("/destinations", response_model=List[dict])
async def get_available_destinations(db: Session = Depends(get_db)):
    """Get all available destinations with basic information."""
    try:
        data_service = TravelDataService(db)
        destinations = data_service.get_all_destinations()
        return destinations
    except Exception as e:
        print(f"Error fetching destinations: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching destinations: {str(e)}")

@app.get("/destinations/{destination_key}")
async def get_destination_details(destination_key: str, db: Session = Depends(get_db)):
    """Get detailed information about a specific destination."""
    try:
        data_service = TravelDataService(db)
        destination = data_service.get_destination_by_key(destination_key)
        
        if not destination:
            raise HTTPException(status_code=404, detail=f"Destination '{destination_key}' not found")
        
        return destination
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error fetching destination {destination_key}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching destination: {str(e)}")

@app.post("/destinations/suggest")
async def suggest_destinations(
    interests: List[str] = Query(...),
    budget_type: BudgetType = Query(BudgetType.MID),
    db: Session = Depends(get_db)
):
    """Get destination suggestions based on interests and budget."""
    try:
        trip_service = TripPlanningService(db)
        suggestions = trip_service.suggest_destinations(interests, budget_type.value)
        return {"suggestions": suggestions}
    except Exception as e:
        print(f"Error suggesting destinations: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error suggesting destinations: {str(e)}")

# === TRIP PLANNING ENDPOINTS ===

@app.post("/trip/plan", response_model=TripRecommendation)
async def plan_trip(request: TripRequest, db: Session = Depends(get_db)):
    """Generate a personalized trip recommendation based on user preferences."""
    try:
        print(f"Planning trip for destination: {request.destination}")
        
        trip_service = TripPlanningService(db)
        recommendation = trip_service.plan_trip(request)
        
        return recommendation
        
    except ValueError as e:
        print(f"Validation error in trip planning: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Error in trip planning: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error planning trip: {str(e)}")

@app.post("/trip/optimize")
async def optimize_trip(request: TripRequest, db: Session = Depends(get_db)):
    """Optimize an existing trip based on new preferences or constraints."""
    try:
        trip_service = TripPlanningService(db)
        optimized_recommendation = trip_service.optimize_trip(request)
        return optimized_recommendation
    except Exception as e:
        print(f"Error optimizing trip: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error optimizing trip: {str(e)}")

@app.get("/trip/templates")
async def get_trip_templates(db: Session = Depends(get_db)):
    """Get pre-defined trip templates for quick planning."""
    try:
        data_service = TravelDataService(db)
        templates = data_service.get_trip_templates()
        return templates
    except Exception as e:
        print(f"Error fetching trip templates: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching templates: {str(e)}")

# === CONTENT ENDPOINTS ===

@app.get("/activities/{destination_key}", response_model=List[EnhancedActivity])
async def get_destination_activities(
    destination_key: str,
    interests: Optional[List[str]] = Query(None),
    budget_type: Optional[BudgetType] = Query(BudgetType.MID),
    db: Session = Depends(get_db)
):
    """Get activities for a specific destination with optional filtering."""
    try:
        data_service = TravelDataService(db)
        activities = data_service.get_activities_for_destination(destination_key, interests)
        
        # Convert to EnhancedActivity format (simplified for now)
        enhanced_activities = []
        for activity in activities:
            enhanced_activities.append(EnhancedActivity(
                name=activity["name"],
                type=activity["type"],
                duration=activity["duration"],
                cost_per_person=activity["cost"][budget_type.value],
                rating=activity["rating"],
                description=activity["description"],
                best_time=activity["best_time"],
                location=activity["location"],
                categories=activity["categories"],
                recommendation_score=4.5  # Default score
            ))
        
        return enhanced_activities
    except Exception as e:
        print(f"Error fetching activities for {destination_key}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching activities: {str(e)}")

@app.get("/hotels/{destination_key}", response_model=List[EnhancedHotel])
async def get_destination_hotels(
    destination_key: str,
    budget_type: Optional[BudgetType] = Query(BudgetType.MID),
    db: Session = Depends(get_db)
):
    """Get hotels for a specific destination with optional budget filtering."""
    try:
        data_service = TravelDataService(db)
        hotels = data_service.get_hotels_for_destination(destination_key, budget_type.value)
        
        # Convert to EnhancedHotel format
        enhanced_hotels = []
        for hotel in hotels:
            enhanced_hotels.append(EnhancedHotel(
                name=hotel["name"],
                category=hotel["category"],
                rating=hotel["rating"],
                price_per_night=hotel["price_per_night"][budget_type.value],
                amenities=hotel["amenities"],
                location=hotel["location"],
                description=hotel["description"],
                recommendation_score=4.3  # Default score
            ))
        
        return enhanced_hotels
    except Exception as e:
        print(f"Error fetching hotels for {destination_key}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching hotels: {str(e)}")

# === ANALYTICS ENDPOINTS ===

@app.get("/analytics/popular-destinations")
async def get_popular_destinations(db: Session = Depends(get_db)):
    """Get analytics data for popular destinations and travel trends."""
    try:
        analytics_service = AnalyticsService(db)
        analytics = analytics_service.get_popular_destinations()
        return analytics
    except Exception as e:
        print(f"Error fetching analytics: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching analytics: {str(e)}")

# === USER PREFERENCES ===

@app.get("/user/preferences/templates")
async def get_preference_templates(db: Session = Depends(get_db)):
    """Get pre-defined user preference templates."""
    try:
        data_service = TravelDataService(db)
        templates = data_service.get_user_preference_templates()
        return templates
    except Exception as e:
        print(f"Error fetching preference templates: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching templates: {str(e)}")

# === BOOKING PROTOTYPE ===

@app.post("/booking/initiate")
async def initiate_booking(booking_request: dict):
    """
    Initiate booking process (Prototype - Not implemented yet).
    This endpoint demonstrates the booking flow for judges.
    """
    return {
        "status": "prototype_mode",
        "message": "🚧 Booking System Under Development",
        "details": {
            "current_stage": "Prototype Phase",
            "next_steps": [
                "Integration with payment gateways (Razorpay/Stripe)",
                "Hotel booking APIs (MakeMyTrip/Booking.com)",
                "Flight booking integration",
                "Real-time availability checking",
                "Confirmation and ticketing system"
            ],
            "estimated_completion": "Phase 2 Development",
            "booking_id": f"PROTO_{hash(str(booking_request)) % 100000:05d}",
            "total_amount": booking_request.get("total_cost", 0),
            "currency": "INR"
        },
        "demo_features": {
            "payment_methods": ["UPI", "Credit Card", "Net Banking", "Wallets"],
            "booking_confirmation": "Email & SMS notifications",
            "cancellation_policy": "Free cancellation up to 24 hours",
            "customer_support": "24/7 multilingual support"
        }
    }

@app.get("/booking/{booking_id}")
async def get_booking_status(booking_id: str):
    """Get booking status (Prototype endpoint)."""
    return {
        "booking_id": booking_id,
        "status": "prototype_mode",
        "message": "This is a prototype booking system",
        "current_status": "Pending Integration",
        "required_apis": [
            "Payment Gateway APIs",
            "Hotel Booking Systems", 
            "Transportation APIs",
            "Activity Booking Platforms"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
