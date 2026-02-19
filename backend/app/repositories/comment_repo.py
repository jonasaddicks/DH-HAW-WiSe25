from sqlalchemy.orm import Session

from app.model import CommentModel

class CommentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, comment: CommentModel) -> CommentModel:
        self.db.add(comment)
        self.db.flush()
        return comment