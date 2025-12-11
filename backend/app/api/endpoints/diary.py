from fastapi import APIRouter

from backend.app.service import diary_service

router = APIRouter()

@router.get("/diary/{entry_id}")
def get_entry(entry_id: str):
    entry = diary_service.get_entry(entry_id)
    return {entry}

@router.post("/diary/{entry_id}")
def add_entry(entry_id: str):
    entry = diary_service.add_entry(entry_id)
    return {entry}