from sqlalchemy import BigInteger
from sqlalchemy.orm import Session
from typing import Optional
from backend.app.model.point_of_interest import PointOfInterest

class PoiRepository:

    def __init__(self, db: Session):
        self.db = db


    def create(self, poi: PointOfInterest) -> PointOfInterest:
        self.db.add(poi)
        self.db.commit()
        self.db.refresh(poi)
        return poi

    def get_by_id(self, osm_id: BigInteger) -> Optional[PointOfInterest]:
        return self.db.query(PointOfInterest).filter(PointOfInterest.osm_id == osm_id).first()

    def count(self) -> int:
        return self.db.query(PointOfInterest).count()

    def update(self, poi: PointOfInterest) -> PointOfInterest:
        self.db.commit()
        self.db.refresh(poi)
        return poi

    def delete(self,poi:  PointOfInterest) -> None:
        self.db.delete(poi)
        self.db.commit()