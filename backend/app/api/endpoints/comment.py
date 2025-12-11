from fastapi import APIRouter

from backend.app.service import map_service

router = APIRouter()

@router.get("/comment/{comment_id}")
def get_comment(comment_id: str):
    comment = map_service.get_comment(comment_id)
    return {comment}

@router.post("/comment/{comment_id}")
def get_comment(comment_id: str):
    comment = map_service.add_comment(comment_id)
    return {comment}