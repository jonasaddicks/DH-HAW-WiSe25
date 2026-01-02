from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.repositories.user_repository import UserRepository
from backend.app.service.register_login_service import RegisterLoginService

router = APIRouter()

def get_register_login_service(db: Session = Depends(get_db)) -> RegisterLoginService:
    """Dependency Injection für Register/LoginService"""
    user_repo = UserRepository(db)
    return RegisterLoginService(user_repo)

@router.post("/register/")
def register_user(data: dict, register_login_service: RegisterLoginService = Depends(get_register_login_service)):
    register_login_service.register_user(data)
    return {"message": "Successfully registered"}

@router.post("/login/")
def register_user(data: dict, register_login_service: RegisterLoginService = Depends(get_register_login_service)):
    register_login_service.login_user(data)
    return {"message": "Successfully logged in"}

