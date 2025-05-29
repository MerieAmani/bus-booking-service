from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Session
from database import Base
from models.trip import Trip
from models.payment import Payment

class Booking(Base):
    __tablename__ = 'bookings'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    trip_id = Column(Integer, ForeignKey('trips.id'))
    seat_number = Column(Integer)
    status = Column(String, default='confirmed')
    
    user = relationship("User", back_populates="bookings")
    trip = relationship("Trip", back_populates="bookings")
    payment = relationship("Payment", back_populates="booking")

    # CRUD Operations
    @classmethod
    def create(cls, db: Session, user_id: int, trip_id: int, seat_number: int, status: str = 'confirmed'):
        booking = cls(
            user_id=user_id,
            trip_id=trip_id,
            seat_number=seat_number,
            status=status
        )
        db.add(booking)
        db.commit()
        db.refresh(booking)
        return booking

    @classmethod
    def get(cls, db: Session, booking_id: int):
        return db.query(cls).filter(cls.id == booking_id).first()

    @classmethod
    def get_by_user(cls, db: Session, user_id: int):
        return db.query(cls).filter(cls.user_id == user_id).all()

    @classmethod
    def get_by_trip(cls, db: Session, trip_id: int):
        return db.query(cls).filter(cls.trip_id == trip_id).all()

    @classmethod
    def update(cls, db: Session, booking_id: int, **kwargs):
        booking = cls.get(db, booking_id)
        if booking:
            for key, value in kwargs.items():
                setattr(booking, key, value)
            db.commit()
            db.refresh(booking)
        return booking

    @classmethod
    def delete(cls, db: Session, booking_id: int):
        booking = cls.get(db, booking_id)
        if booking:
            db.delete(booking)
            db.commit()
            return True
        return False
    
@classmethod
def create_booking(
    cls,
    db: Session,
    user_id: int,
    trip_id: int,
    seat_number: int
) -> "Booking":
    available_seats = Trip.get_available_seats(db, trip_id)
    if seat_number not in available_seats:
        raise ValueError(f"Seat {seat_number} not available")
    
    booking = cls(
        user_id=user_id,
        trip_id=trip_id,
        seat_number=seat_number,
        status="confirmed"
    )
    db.add(booking)
    
    trip = Trip.get(db, trip_id)
    if not trip or not hasattr(trip, "route") or not hasattr(trip.route, "distance_km"):
        raise ValueError("Trip or route information is missing")
    payment = Payment(
        booking=booking,
        amount=trip.route.distance_km * 2.5,
        status="pending"
    )
    db.add(payment)
    
    db.commit()
    return booking