from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class JobBase(BaseModel):
    source: str
    external_job_id: str
    title: str
    company: str
    location: Optional[str] = None
    salary_range: Optional[str] = None
    description: str
    url: str

class JobCreate(JobBase):
    pass

class JobResponse(JobBase):
    id: int
    discovered_at: datetime
    requirements_json: Optional[dict] = None

    model_config = {"from_attributes": True}

class MatchAnalysis(BaseModel):
    match_score: int # 0 to 100
    matched_skills: List[str]
    missing_skills: List[str]
    strengths: List[str]
    match_explanation: str
    recommendation: str # e.g. "apply_now", "skip", "tailor_resume"

class JobMatchResponse(BaseModel):
    id: int
    user_id: int
    job_id: int
    match_score: float
    match_analysis_json: Optional[MatchAnalysis] = None
    status: str
    created_at: datetime
    
    job: JobResponse

    model_config = {"from_attributes": True}
