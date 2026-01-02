from fastapi import FastAPI
from app.api.endpoints import comment, contribution, diary, register_login, routing

app = FastAPI()

app.include_router(comment.router,prefix="/api/comment",tags=["comments"])
app.include_router(contribution.router,prefix="/api/contribution",tags=["contribution"])
app.include_router(diary.router,prefix="/api/diary",tags=["diary"])
app.include_router(register_login.router,prefix="/api/register-login",tags=["register-login"])
app.include_router(routing.router,prefix="/api/routing",tags=["routing"])
