from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))
    resume_version_id = Column(Integer, ForeignKey("resume_versions.id"), nullable=True)
    cover_letter_id = Column(Integer, ForeignKey("cover_letters.id"), nullable=True)
    
    # ready_to_apply, applied, interview, rejected, offer
    status = Column(String, default="ready_to_apply")
    applied_at = Column(DateTime, nullable=True)
    follow_up_date = Column(DateTime, nullable=True)
    notes = Column(String, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
    job = relationship("Job", back_populates="applications")
    resume_version = relationship("ResumeVersion", back_populates="application")
    cover_letter = relationship("CoverLetter", back_populates="application")
    events = relationship("ApplicationEvent", back_populates="application")

class ApplicationEvent(Base):
    __tablename__ = "application_events"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"))
    event_type = Column(String) # e.g., 'status_change', 'note_added', 'email_received'
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    application = relationship("Application", back_populates="events")
