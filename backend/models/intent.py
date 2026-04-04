from pydantic import BaseModel
from typing import Optional, List, Any

class Intent(BaseModel):
    location: str
    occasion: str
    vibe: str
    budget_min: int
    budget_max: int
    group_size: int
    date_time: str
    city: str
    country: str
    constraints: List[str] = []

class ItineraryStop(BaseModel):
    time: str
    name: str
    type: str
    address: str
    rating: Optional[float] = None
    estimated_cost: Optional[str] = None
    maps_link: Optional[str] = None
    notes: Optional[str] = None

class TransportLeg(BaseModel):
    from_stop: str
    to_stop: str
    mode: str
    duration: str
    instructions: Optional[str] = None
    estimated_cost: Optional[str] = None

class PlanScores(BaseModel):
    vibe_match: int
    coherence: int
    practicality: int

class Itinerary(BaseModel):
    title: str
    date: str
    location: str
    stops: List[ItineraryStop]
    transport_legs: List[TransportLeg]
    scores: PlanScores
    total_estimated_cost: str
    summary: str

class QueryRequest(BaseModel):
    message: str
    user_id: Optional[str] = "default_user"
    session_id: Optional[str] = None

class QueryResponse(BaseModel):
    response: str
    itinerary: Optional[Any] = None
    session_id: str
