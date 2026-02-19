from fastapi import APIRouter, Query, status, HTTPException, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.dtos import CommentResponseDTO, CommentCreateDTO
from app.logging import log_info, Source, log_debug, log_error, log_warning
from app.service import CommentService

router = APIRouter()

@router.get("/at", response_model=list[CommentResponseDTO])
async def get_comments_at(
    lat: float = Query(..., description="at latitude"),
    lng: float = Query(..., description="at longitude"),
    radius: float = Query(1000.0, description="radius in meters")
):
    """
    Collects all available comments around a given point in a given radius.
    """

    return CommentService.get_comments_at_service(lat, lng, radius)

@router.post("/post")
async def post_comment(
    dto: CommentCreateDTO,
    db: Session = Depends(get_db)
):
    """
    Creates and saves a comment by the specified user at the given location.
    """

    log_info(Source.endpoint_comment, '/post: called')
    log_debug(Source.endpoint_comment, f'/post: {dto}')

    try:
        success: bool = CommentService.post_comment_service(db, dto)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not create comment"
            )
        log_info(Source.endpoint_comment, '/post: success')
        return

    except HTTPException as e:
        log_warning(Source.endpoint_comment, f'/post: external failure: {repr(e)}')
        raise

    except Exception as e:
        log_error(Source.endpoint_comment, f'/post: internal failure: {repr(e)}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Interner Serverfehler."
        )