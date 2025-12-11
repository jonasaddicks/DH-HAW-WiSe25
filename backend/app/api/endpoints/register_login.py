from fastapi import APIRouter
from backend.app.service import register_login_service

router = APIRouter()
@router.post("/register/")
def register_user(data: dict):
    register_login_service.register_user(data)
    return {"message": "Successfully registered","data": "data"}

@router.post("/login/")
def register_user(data: dict):
    register_login_service.login_user(data)
    return {"message": "Successfully logged in","data": "data"}

