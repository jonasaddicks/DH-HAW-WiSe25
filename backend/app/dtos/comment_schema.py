from pydantic import BaseModel
from datetime import datetime


class CommentResponse(BaseModel):
    id: int
    text: str
    lat: float
    lng: float
    user: str
    created_at: str
    
    class Config:
        from_attributes = True