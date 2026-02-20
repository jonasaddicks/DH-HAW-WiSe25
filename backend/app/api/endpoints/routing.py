from fastapi import APIRouter, Query

from app.dtos import RoutingResponse
from app.service import RoutingService

router = APIRouter()

@router.get("/route", response_model=list[RoutingResponse])
async def calculate_routes(
    start_lat: float = Query(..., description="start latitude"),
    start_lng: float = Query(..., description="start longitude"),
    end_lat: float = Query(..., description="end latitude"),
    end_lng: float = Query(..., description="end longitude")
):
    """
    Calculates possible routes from given start to given end coordinates.
    """

    start = (start_lat, start_lng)
    end = (end_lat, end_lng)
    return await RoutingService.calculate_routes_service(start, end)
