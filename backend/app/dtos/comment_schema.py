from pydantic import BaseModel, Field


class CommentResponseDTO(BaseModel):
    id: int
    text: str
    lat: float
    lng: float
    user: str
    created_at: str

class CommentRequestDTO(BaseModel):
    lat: float
    lng: float
    radius: float = Field(default=1000, gt=0)

class CommentCreateDTO(BaseModel):
    text: str = Field(..., min_length=1, max_length=511)
    lat: float
    lng: float
    user_id: int