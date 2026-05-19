from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.api import deps
from app.models.user import User, UserProfile
from app.models.job import Job, JobMatch
from app.schemas.job import JobCreate, JobResponse, JobMatchResponse
from app.services.job_analyzer import analyze_job_match
from app.schemas.profile import ParsedResumeStructure

router = APIRouter()

@router.get("/", response_model=List[JobMatchResponse])
async def list_job_matches(
    current_user: User = Depends(deps.get_current_active_user),
    db: AsyncSession = Depends(deps.get_db),
):
    """
    List all jobs matched for the current user.
    """
    # Fetch job matches eagerly loading the Job
    from sqlalchemy.orm import selectinload
    result = await db.execute(
        select(JobMatch)
        .options(selectinload(JobMatch.job))
        .filter(JobMatch.user_id == current_user.id)
        .order_by(JobMatch.match_score.desc())
    )
    matches = result.scalars().all()
    return matches

@router.post("/analyze/{job_id}", response_model=JobMatchResponse)
async def trigger_job_analysis(
    job_id: int,
    current_user: User = Depends(deps.get_current_active_user),
    db: AsyncSession = Depends(deps.get_db),
):
    """
    Trigger AI analysis to match a specific job against the user's parsed resume.
    """
    # Get user profile
    result = await db.execute(select(UserProfile).filter(UserProfile.user_id == current_user.id))
    profile = result.scalars().first()
    
    if not profile or not profile.parsed_resume_json:
        raise HTTPException(status_code=400, detail="Please upload and parse a master resume first.")
        
    parsed_profile = ParsedResumeStructure(**profile.parsed_resume_json)

    # Get Job
    result = await db.execute(select(Job).filter(Job.id == job_id))
    job = result.scalars().first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Analyze
    try:
        analysis = await analyze_job_match(job.description, parsed_profile)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Analysis failed: {str(e)}")

    # Create or update match
    result = await db.execute(
        select(JobMatch).filter(JobMatch.user_id == current_user.id, JobMatch.job_id == job_id)
    )
    job_match = result.scalars().first()

    if not job_match:
        job_match = JobMatch(
            user_id=current_user.id,
            job_id=job.id,
            match_score=analysis.match_score,
            match_analysis_json=analysis.model_dump(),
            status="shortlisted" if analysis.recommendation in ["apply_now", "tailor_resume"] else "discovered"
        )
        db.add(job_match)
    else:
        job_match.match_score = analysis.match_score
        job_match.match_analysis_json = analysis.model_dump()
        job_match.status = "shortlisted" if analysis.recommendation in ["apply_now", "tailor_resume"] else "discovered"

    await db.commit()
    await db.refresh(job_match)
    
    # Reload with relation
    from sqlalchemy.orm import selectinload
    result = await db.execute(
        select(JobMatch).options(selectinload(JobMatch.job)).filter(JobMatch.id == job_match.id)
    )
    return result.scalars().first()
