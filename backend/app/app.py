from fastapi import FastAPI

from app.api import comments, routing

app = FastAPI(title="Proof-of-Concept API backend")

app.include_router(comments.router, prefix="/comments", tags=["Comments"])
app.include_router(routing.router, prefix="/routing", tags=["Routing"])
