from fastapi import APIRouter
from backend.app.service import map_service

router = APIRouter()

router.post("/contribution/{location}")
def add_contribution(location: str):
    map_service.add_contribution(location)
    return {}