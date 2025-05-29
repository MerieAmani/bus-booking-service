from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Session
from typing import Optional
from database import Base

class Route(Base):
    __tablename__ = 'routes'

    id = Column(Integer, primary_key=True, index=True)
    origin = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    estimated_duration = Column(String)
    distance_km = Column(Integer)
    
    trips = relationship("Trip", back_populates="route")

    # CRUD Operations
    @classmethod
    def create(
        cls,
        db: Session,
        origin: str,
        destination: str,
        estimated_duration: Optional[str] = None,
        distance_km: Optional[int] = None
    ):
        route = cls(
            origin=origin,
            destination=destination,
            estimated_duration=estimated_duration,
            distance_km=distance_km
        )
        db.add(route)
        db.commit()
        db.refresh(route)
        return route

    @classmethod
    def get(cls, db: Session, route_id: int):
        return db.query(cls).filter(cls.id == route_id).first()

    @classmethod
    def get_by_route(cls, db: Session, origin: str, destination: str):
        return db.query(cls).filter(
            cls.origin == origin,
            cls.destination == destination
        ).first()

    @classmethod
    def update(cls, db: Session, route_id: int, **kwargs):
        route = cls.get(db, route_id)
        if route:
            for key, value in kwargs.items():
                setattr(route, key, value)
            db.commit()
            db.refresh(route)
        return route

    @classmethod
    def delete(cls, db: Session, route_id: int):
        route = cls.get(db, route_id)
        if route:
            db.delete(route)
            db.commit()
            return True
        return False