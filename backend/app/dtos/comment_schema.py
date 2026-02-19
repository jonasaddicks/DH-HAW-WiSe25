from pydantic import BaseModel, Field


class CommentResponseDTO(BaseModel):
    id: int
    text: str
    lat: float
    lng: float
    user: str
    created_at: str
    
    class Config:
        from_attributes = True

class CommentCreateDTO(BaseModel):
    text: str = Field(..., min_length=1, max_length=511)
    lat: float
    lng: float
    user_id: int