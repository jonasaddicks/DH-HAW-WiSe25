from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from typing import Optional, List
from uuid import UUID
from backend.app.model.user import User
from backend.app.model.userPrefs import UserPrefs


class UserRepository:
    """
    Repository für User-Entität
    Verantwortlich für alle Datenbank-Operationen mit User
    """

    def __init__(self, db: Session):
        """
        Args:
            db: SQLAlchemy Session (wird über Dependency Injection übergeben)
        """
        self.db = db

    # ═══════════════════════════════════════════════════════════════
    # CREATE
    # ═══════════════════════════════════════════════════════════════

    def create(self, user: User) -> User:
        """
        Erstellt einen neuen User in der Datenbank

        Args:
            user: User-Objekt (noch ohne ID aus DB)

        Returns:
            User: Gespeicherter User mit generierter ID
        """
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)  # Lädt generierte Felder (user_id, created_at)
        return user

    # ═══════════════════════════════════════════════════════════════
    # READ - Single
    # ═══════════════════════════════════════════════════════════════

    def get_by_id(self, user_id: UUID) -> Optional[User]:
        """
        Holt User anhand der ID

        Args:
            user_id: UUID des Users

        Returns:
            User oder None wenn nicht gefunden
        """
        return self.db.query(User).filter(User.user_id == user_id).first()

    def count(self) -> int:
        """
        Zählt alle User

        Returns:
            Anzahl der User
        """
        return self.db.query(User).count()

        # ═══════════════════════════════════════════════════════════════
    # UPDATE
    # ═══════════════════════════════════════════════════════════════

    def update(self, user: User) -> User:
        """
        Updated einen existierenden User
        WICHTIG: User-Objekt muss bereits aus DB geladen sein!

        Args:
            user: User-Objekt mit geänderten Werten

        Returns:
            Updated User

        Example:
            user = repo.get_by_id(user_id)
            user.display_name = "Neuer Name"
            repo.update(user)
        """
        self.db.commit()
        self.db.refresh(user)
        return user

    # ═══════════════════════════════════════════════════════════════
    # DELETE
    # ═══════════════════════════════════════════════════════════════

    def delete(self, user: User) -> None:
        """
        Löscht einen User aus der Datenbank
        CASCADE löscht automatisch:
        - UserPrefs (wegen ON DELETE CASCADE)
        - Comments (wegen ON DELETE CASCADE)
        - Contributions (wegen ON DELETE CASCADE)

        Args:
            user: Zu löschender User
        """
        self.db.delete(user)
        self.db.commit()

        # ═══════════════════════════════════════════════════════════════
    # EXISTS / VALIDATION
    # ═══════════════════════════════════════════════════════════════

    def exists_by_email(self, email: str) -> bool:
        """
        Prüft ob User mit Email existiert (effizienter als get_by_email)

        Args:
            email: Email-Adresse

        Returns:
            True wenn existiert
        """
        return self.db.query(User.user_id) \
            .filter(User.email == email) \
            .first() is not None