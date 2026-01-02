from sqlalchemy.orm import Session
from typing import Optional, List
from backend.app.model.comment import Comment
from backend.app.model.point_of_interest import PointOfInterest
from backend.app.model.user import User
from fastapi import HTTPException
from backend.app.repositories.poi_repository import PoiRepository
from backend.app.repositories.user_repository import UserRepository


class CommentService:
    """
        Comment-Service OHNE eigenes Repository
        Greift direkt auf die DB zu
        """

    def __init__(self, db: Session, user_repo: UserRepository, poi_repo: PoiRepository):
        self.db = db
        self.user_repo = user_repo
        self.poi_repo = poi_repo

    def create_comment(
            self,
            user_id,
            osm_id: int,
            text: str,
            geom: str
    ) -> Comment:
        """Erstellt neuen Comment"""

        user = self.user_repo.get_by_id(user_id)
        poi = self.poi_repo.get_by_id(osm_id)
        # Validierung: POI muss existieren
        if not poi:
            raise HTTPException(404, "POI not found")

        if not user:
            raise HTTPException(404, "User not found")

        # Comment erstellen
        comment = Comment(
            user_id=user_id,
            osm_id=osm_id,
            text=text,
            geom=geom
        )

        self.user_repo.update()
        return comment

    def update_comment(
            self,
            comment_id: int,
            user_id,
            new_text: str
    ) -> Comment:
        """Updated Comment (nur eigener)"""

        # Comment laden
        comment = self.db.query(Comment) \
            .filter(Comment.comment_id == comment_id) \
            .first()

        if not comment:
            raise HTTPException(404, "Comment not found")

        # Berechtigung prüfen
        if comment.user_id != user_id:
            raise HTTPException(403, "Not your comment")

        # Update
        comment.text = new_text
        self.db.commit()
        self.db.refresh(comment)
        return comment

    def delete_comment(self, comment_id: int, user_id) -> None:
        """Löscht Comment (nur eigener)"""

        comment = self.db.query(Comment) \
            .filter(Comment.comment_id == comment_id) \
            .first()

        if not comment:
            raise HTTPException(404, "Comment not found")

        if comment.user_id != user_id:
            raise HTTPException(403, "Not your comment")

        self.db.delete(comment)
        self.db.commit()

    def hide_comment(self, comment_id: int) -> None:
        """Versteckt Comment (Moderation)"""

        comment = self.db.query(Comment) \
            .filter(Comment.comment_id == comment_id) \
            .first()

        if not comment:
            raise HTTPException(404, "Comment not found")

        comment.is_hidden = True
        self.db.commit()

    def get_comments_for_poi(
            self,
            osm_id: int,
            include_hidden: bool = False
    ) -> List[Comment]:
        """Holt alle Comments für einen POI"""

        query = self.db.query(Comment) \
            .filter(Comment.osm_id == osm_id)

        if not include_hidden:
            query = query.filter(Comment.is_hidden == False)

        return query.order_by(Comment.created_at.desc()).all()