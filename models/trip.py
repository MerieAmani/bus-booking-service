from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Session
from database import Base
from datetime import datetime
from typing import List

class Trip(Base):
    __tablename__ = 'trips'

    id = Column(Integer, primary_key=True, index=True)
    route_id = Column(Integer, ForeignKey('routes.id'))
    bus_id = Column(Integer, ForeignKey('buses.id'))
    departure_time = Column(DateTime)
    arrival_time = Column(DateTime)
    available_seats = Column(Integer)
    
    route = relationship("Route", back_populates="trips")
    bus = relationship("Bus", back_populates="trips")
    bookings = relationship("Booking", back_populates="trip")

    # CRUD Operations
    @classmethod
    def create(cls, db: Session, route_id: int, bus_id: int, departure_time: datetime, 
               arrival_time: datetime, available_seats: int):
        trip = cls(
            route_id=route_id,
            bus_id=bus_id,
            departure_time=departure_time,
            arrival_time=arrival_time,
            available_seats=available_seats
        )
        db.add(trip)
        db.commit()
        db.refresh(trip)
        return trip

    @classmethod
    def get(cls, db: Session, trip_id: int):
        return db.query(cls).filter(cls.id == trip_id).first()

    @classmethod
    def get_by_route(cls, db: Session, route_id: int):
        return db.query(cls).filter(cls.route_id == route_id).all()

    @classmethod
    def update(cls, db: Session, trip_id: int, **kwargs):
        trip = cls.get(db, trip_id)
        if trip:
            for key, value in kwargs.items():
                setattr(trip, key, value)
            db.commit()
            db.refresh(trip)
        return trip

    @classmethod
    def delete(cls, db: Session, trip_id: int):
        trip = cls.get(db, trip_id)
        if trip:
            db.delete(trip)
            db.commit()
            return True
        return False

@classmethod
def get_available_seats(cls, db: Session, trip_id: int) -> List[int]:
    """Returns list of available seat numbers"""
    trip = db.query(cls).get(trip_id)
    if not trip:
        raise ValueError("Trip not found")
    
    booked_seats = [b.seat_number for b in trip.bookings]
    return [s for s in range(1, trip.bus.capacity + 1) if s not in booked_seats]

@classmethod
def search_available(
    cls, 
    db: Session, 
    origin: str, 
    destination: str, 
    date: datetime
) -> List["Trip"]:
    return db.query(cls).filter(
        cls.route.has(origin=origin),
        cls.route.has(destination=destination),
        cls.departure_time >= date
    ).all()