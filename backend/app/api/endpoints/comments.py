from fastapi import APIRouter, Query

from app.dtos import CommentResponse
from app.service import CommentService

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

    return CommentService.get_comments_at_service(lat, lng, radius)
