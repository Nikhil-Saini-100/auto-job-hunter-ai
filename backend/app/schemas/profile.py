from typing import List, Optional, Any
from pydantic import BaseModel
from datetime import datetime

class Skill(BaseModel):
    name: str
    level: Optional[str] = "Intermediate"

class Experience(BaseModel):
    title: str
    company: str
    location: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    description: List[str] = []

class Education(BaseModel):
    degree: str
    institution: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None

class Project(BaseModel):
    name: str
    description: str
    technologies: List[str] = []
    url: Optional[str] = None

class ParsedResumeStructure(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    summary: Optional[str] = None
    skills: List[Skill] = []
    experience: List[Experience] = []
    education: List[Education] = []
    projects: List[Project] = []

class UserPreferences(BaseModel):
    preferred_roles: List[str] = []
    preferred_locations: List[str] = []
    remote_preference: str = "Hybrid" # Remote, On-site, Hybrid
    expected_salary_range: Optional[str] = None
    notice_period_days: Optional[int] = 30

class UserProfileUpdate(BaseModel):
    preferences: Optional[UserPreferences] = None
    parsed_resume: Optional[ParsedResumeStructure] = None

class UserProfileResponse(BaseModel):
    id: int
    user_id: int
    master_resume_path: Optional[str] = None
    parsed_resume_json: Optional[ParsedResumeStructure] = None
    preferences_json: Optional[UserPreferences] = None

    model_config = {"from_attributes": True}
