from sqlalchemy.orm import Session
from sqlalchemy import cast, func
from geoalchemy2 import Geography

from app.model import CommentModel, UserModel


class CommentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, comment: CommentModel) -> CommentModel:
        """
        Creates a new comment in the database
        """
        self.db.add(comment)
        self.db.flush()
        return comment

    def get_comments_in_radius(self, lng: float, lat: float, radius_m: float):
        """
        Returns rows with fields: id, text, lat, lng, user (display_name), created_at
        radius_m is in meters.
        """
        point = func.ST_SetSRID(func.ST_MakePoint(lng, lat), 4326)

        q = (
            self.db.query(
                CommentModel.comment_id.label("id"),
                CommentModel.text.label("text"),
                func.ST_Y(CommentModel.geom).label("lat"), # ST_Y -> latitude
                func.ST_X(CommentModel.geom).label("lng"), # ST_X -> longitude
                UserModel.display_name.label("user"),
                CommentModel.created_at.label("created_at"),
            )
            .join(UserModel, CommentModel.user)
            .filter(
                func.ST_DWithin( # cast to use meter instead of degree
                    cast(CommentModel.geom, Geography),
                    cast(point, Geography),
                    radius_m
                )
            )
            .order_by(CommentModel.created_at.desc())
        )

        return q.all()