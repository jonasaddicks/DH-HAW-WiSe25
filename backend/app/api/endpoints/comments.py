from fastapi import APIRouter, status, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import Annotated

from app.db import get_db
from app.dtos import CommentResponseDTO, CommentCreateDTO, CommentRequestDTO
from app.exceptions import CommentConversionException
from app.logging import log_info, Source, log_debug, log_error, log_warning
from app.service import CommentService

router = APIRouter()

@router.get("/at", response_model=list[CommentResponseDTO])
async def get_comments_at(
    dto: Annotated[CommentRequestDTO, Query()],
    db: Session = Depends(get_db),
):
    """
    Collects all available comments around a given point in a given radius.
    """

    log_info(Source.endpoint_comment, '/at: called')
    log_debug(Source.endpoint_comment, f'/at: {dto}')

    try:
        result = CommentService.get_comments_at_service(db, dto)
        log_info(Source.endpoint_comment, '/at: success')
        return result

    except Exception as e:
        log_error(Source.endpoint_comment, f'/at: internal failure: {repr(e)}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error."
        )


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
        CommentService.post_comment_service(db, dto)
        log_info(Source.endpoint_comment, '/post: success')

    except CommentConversionException as e:
        log_warning(Source.endpoint_comment, f'/post: external failure: {repr(e)}')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not create comment"
        )

    except Exception as e:
        log_error(Source.endpoint_comment, f'/post: internal failure: {repr(e)}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error."
        )