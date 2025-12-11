from fastapi import APIRouter

from backend.app.service import routing_service

router = APIRouter()

router.get("/routing/start_navigation/{route_id}")
def start_navigation(route_id):
    routing_service.start_navigation(route_id)
    return {}

router.post("/routing/route")
def make_route(start, end):
    routing_service.get_route(start, end)
    return {}