from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship, Session
from datetime import datetime
from database import Base

class Bus(Base):
    __tablename__ = 'buses'

    id = Column(Integer, primary_key=True, index=True)
    number_plate = Column(String, unique=True, nullable=False)
    model = Column(String, nullable=False)
    capacity = Column(Integer, nullable=False)
    
    trips = relationship("Trip", back_populates="bus")

    # CRUD Operations
    @classmethod
    def create(cls, db: Session, number_plate: str, model: str, capacity: int):
        bus = cls(
            number_plate=number_plate,
            model=model,
            capacity=capacity
        )
        db.add(bus)
        db.commit()
        db.refresh(bus)
        return bus

    @classmethod
    def get(cls, db: Session, bus_id: int):
        return db.query(cls).filter(cls.id == bus_id).first()

    @classmethod
    def get_by_plate(cls, db: Session, number_plate: str):
        return db.query(cls).filter(cls.number_plate == number_plate).first()

    @classmethod
    def update(cls, db: Session, bus_id: int, **kwargs):
        bus = cls.get(db, bus_id)
        if bus:
            for key, value in kwargs.items():
                setattr(bus, key, value)
            db.commit()
            db.refresh(bus)
        return bus

    @classmethod
    def delete(cls, db: Session, bus_id: int):
        bus = cls.get(db, bus_id)
        if bus:
            db.delete(bus)
            db.commit()
            return True
        return False