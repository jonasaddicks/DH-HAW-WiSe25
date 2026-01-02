from starlette.exceptions import HTTPException
from fastapi import HTTPException, status
from passlib.context import CryptContext
from backend.app.model import User
from backend.app.repositories.user_repository import UserRepository

class RegisterLoginService:
    def __init__(self,user_repo: UserRepository):
        self.user_repo = user_repo
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def register_user(self, data):
        existing_user = self.user_repo.get_by_id(data.user_id)
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Username already registered")
        # TODO: Ich bin lost mit den HTTP-Returns, aber ich glaube hier ist nicht der richtige Ort dafür

        new_user = User(
            email=data.email,
            display_name=data.display_name,
            password_hash=self.hash_password(data.password)
        )

        self.user_repo.create(new_user)
        # TODO: Return ist was??


    def login_user(self, data):
        existing_user = self.user_repo.get_by_id(data.user_id)
        if not existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Username not registered")

        # TODO: Was ändert sich?

    def hash_password(self, password) -> str:
        return self.pwd_context.hash(password)