from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import comments, routing

app = FastAPI(title="Proof-of-Concept API backend")

# CORS aktivieren für Frontend-Zugriff
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In Production einschränken!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(comments.router, prefix="/comments", tags=["Comments"])
app.include_router(routing.router, prefix="/routing", tags=["Routing"])
