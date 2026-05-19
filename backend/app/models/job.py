from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, index=True) # e.g., 'indeed', 'internshala'
    external_job_id = Column(String, unique=True, index=True)
    title = Column(String, nullable=False)
    company = Column(String, nullable=False)
    location = Column(String)
    salary_range = Column(String)
    description = Column(String)
    requirements_json = Column(JSON) # Extracted skills, etc.
    url = Column(String, nullable=False)
    discovered_at = Column(DateTime, default=datetime.utcnow)

    matches = relationship("JobMatch", back_populates="job")
    applications = relationship("Application", back_populates="job")

class JobMatch(Base):
    __tablename__ = "job_matches"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))
    match_score = Column(Float)
    match_analysis_json = Column(JSON) # matched skills, missing skills, etc.
    status = Column(String, default="discovered") # discovered, shortlisted, rejected
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="jobs")
    job = relationship("Job", back_populates="matches")
