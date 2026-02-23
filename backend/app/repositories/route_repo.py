from sqlalchemy.orm import Session

from app.model import UserPrefsModel

class RoutingRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_prefs(self, user_id: int) -> dict | None:
        user_prefs = (
            self.db.query(UserPrefsModel.user_id, UserPrefsModel.prefs)
            .filter(UserPrefsModel.user_id == user_id)
            .one_or_none()
        )

        if user_prefs:
            return user_prefs.prefs
        return None