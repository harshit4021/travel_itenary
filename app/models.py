from typing import List, Optional
from pydantic import BaseModel


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
