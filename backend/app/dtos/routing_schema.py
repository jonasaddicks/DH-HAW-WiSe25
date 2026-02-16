from pydantic import BaseModel
from typing import List, Tuple


class RouteSegment(BaseModel):
    """Ein einzelner Punkt auf der Route"""
    lat: float
    lng: float


class RoutingResponse(BaseModel):
    """Eine berechnete Route"""
    route_id: int
    name: str
    distance_m: float
    duration_min: int
    difficulty: str  # 'easy', 'medium', 'hard'
    waypoints: List[RouteSegment]
    
    class Config:
        from_attributes = True