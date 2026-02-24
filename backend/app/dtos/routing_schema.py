from pydantic import BaseModel
from typing import List


class RouteSegment(BaseModel):
    """
    Represents a single point on a route
    """
    lat: float
    lng: float

class Route(BaseModel):
    """
    A route built from a list of route segments
    """
    distance_m: float
    duration_min: int
    start: RouteSegment
    end: RouteSegment
    waypoints: List[RouteSegment]
    
    class Config:
        from_attributes = True

class RoutingResponse(BaseModel):
    score: float
    route: Route

class RoutingRequest(BaseModel):
    user_id: int
    start_lat: float
    start_lng: float
    end_lat: float
    end_lng: float