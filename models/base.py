from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer
from sqlalchemy.orm import Session
from typing import Any

Base = declarative_base()

class BaseMixin:
    """Base model class that provides common columns and methods"""
    
    id = Column(Integer, primary_key=True, index=True)
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(id={self.id})>"
    @classmethod
    def create(cls, db: Session, **kwargs) -> Any:
        """Create and save a new instance"""
        obj = cls(**kwargs)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj
        
    @classmethod
    def get(cls, db: Session, id: int) -> Any:
        """Get instance by ID"""
        return db.query(cls).get(id)
        
    @classmethod
    def get_all(cls, db: Session, skip: int = 0, limit: int = 100) -> "list[Any]":
        """Get all instances with pagination"""
        return db.query(cls).offset(skip).limit(limit).all()
        
    def update(self, db: Session, **kwargs) -> None:
        """Update instance attributes"""
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.commit()
        db.refresh(self)
        
    def delete(self, db: Session) -> None:
        """Delete instance"""
        db.delete(self)
        db.commit()
        db.commit()

# Import all SQLAlchemy types for convenience
from sqlalchemy import (
    String, 
    DateTime, 
    Float, 
    Boolean, 
    ForeignKey,
    Text,
    Date,
    Time,
    Numeric,
    LargeBinary
)

__all__ = ['Base', 'BaseMixin', 'Column', 'Integer', 'String', 'DateTime', 
           'Float', 'Boolean', 'ForeignKey', 'Text', 'Date', 'Time', 
           'Numeric', 'LargeBinary']