from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    profile = relationship("UserProfile", back_populates="user", uselist=False)
    jobs = relationship("JobMatch", back_populates="user")
    resumes = relationship("ResumeVersion", back_populates="user")

class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, sqlalchemy.ForeignKey("users.id"))
    master_resume_path = Column(String, nullable=True)
    parsed_resume_json = Column(JSON, nullable=True)
    preferences_json = Column(JSON, nullable=True)

    user = relationship("User", back_populates="profile")
