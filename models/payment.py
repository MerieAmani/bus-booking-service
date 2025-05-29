from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, Session
from typing import Optional
from database import Base

class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey('bookings.id'), unique=True)
    amount = Column(Float)
    status = Column(String, default='pending')
    method = Column(String)
    
    booking = relationship("Booking", back_populates="payment")

    @classmethod
    def create(cls, db: Session, booking_id: int, amount: float, status: str = 'pending', method: Optional[str] = None):
        payment = cls(
            booking_id=booking_id,
            amount=amount,
            status=status,
            method=method
        )
        db.add(payment)
        db.commit()
        db.refresh(payment)
        return payment

    @classmethod
    def get(cls, db: Session, payment_id: int):
        return db.query(cls).filter(cls.id == payment_id).first()

    @classmethod
    def get_by_booking(cls, db: Session, booking_id: int):
        return db.query(cls).filter(cls.booking_id == booking_id).first()

    @classmethod
    def get_by_status(cls, db: Session, status: str):
        return db.query(cls).filter(cls.status == status).all()

    @classmethod
    def update(cls, db: Session, payment_id: int, **kwargs):
        payment = cls.get(db, payment_id)
        if payment:
            for key, value in kwargs.items():
                setattr(payment, key, value)
            db.commit()
            db.refresh(payment)
        return payment

    @classmethod
    def delete(cls, db: Session, payment_id: int):
        payment = cls.get(db, payment_id)
        if payment:
            db.delete(payment)
            db.commit()
            return True
        return False