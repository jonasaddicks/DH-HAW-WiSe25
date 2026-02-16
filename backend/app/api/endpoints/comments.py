from fastapi import APIRouter, Query

from app.dtos import CommentResponse
from app.service.comment_service import get_comments_at as get_comments_service

router = APIRouter()

@router.get("/at", response_model=list[CommentResponse])
async def get_comments_at(
    lat: float = Query(..., description="at latitude"),
    lng: float = Query(..., description="at longitude"),
    radius: float = Query(1000.0, description="radius in meters")
):
    """
    Collects all available comments around a given point in a given radius.
    """

    return get_comments_service(lat, lng, radius)
