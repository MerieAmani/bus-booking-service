from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship, Session
from datetime import datetime, timezone
from typing import Optional
from database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    full_name = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    bookings = relationship("Booking", back_populates="user")

    @classmethod
    def create(cls, db: Session, username: str, email: str, password: str, full_name: Optional[str] = None):
        user = cls(
            username=username,
            email=email,
            password_hash=password,
            full_name=full_name
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
        return user

    @classmethod
    def get(cls, db: Session, user_id: int):
        return db.query(cls).filter(cls.id == user_id).first()

    @classmethod
    def get_by_email(cls, db: Session, email: str):
        return db.query(cls).filter(cls.email == email).first()

    @classmethod
    def get_by_username(cls, db: Session, username: str):
        return db.query(cls).filter(cls.username == username).first()

    @classmethod
    def update(cls, db: Session, user_id: int, **kwargs):
        user = cls.get(db, user_id)
        if user:
            for key, value in kwargs.items():
                setattr(user, key, value)
            db.commit()
            db.refresh(user)
        return user

    @classmethod
    def delete(cls, db: Session, user_id: int):
        user = cls.get(db, user_id)
        if user:
            db.delete(user)
            db.commit()
            return True
        return False