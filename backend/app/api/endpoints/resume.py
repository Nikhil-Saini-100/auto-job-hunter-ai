from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.api import deps
from app.models.user import User, UserProfile
from app.models.job import Job
from app.models.resume import ResumeVersion, CoverLetter
from app.schemas.profile import ParsedResumeStructure
from app.services.resume_tailor import tailor_resume_for_job

router = APIRouter()

@router.post("/tailor/{job_id}")
async def generate_tailored_resume(
    job_id: int,
    current_user: User = Depends(deps.get_current_active_user),
    db: AsyncSession = Depends(deps.get_db),
):
    """
    Generate a tailored resume and cover letter for a specific job.
    """
    # Fetch job
    result = await db.execute(select(Job).filter(Job.id == job_id))
    job = result.scalars().first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Fetch master profile
    result = await db.execute(select(UserProfile).filter(UserProfile.user_id == current_user.id))
    profile = result.scalars().first()
    if not profile or not profile.parsed_resume_json:
        raise HTTPException(status_code=400, detail="Master profile not set up")

    parsed_profile = ParsedResumeStructure(**profile.parsed_resume_json)

    try:
        # Generate Tailored Content via AI
        tailored_data = await tailor_resume_for_job(job, parsed_profile)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to tailor resume: {str(e)}")

    # Construct the final tailored resume JSON structure
    final_resume_json = parsed_profile.model_dump()
    final_resume_json["summary"] = tailored_data.tailored_summary
    final_resume_json["experience"] = tailored_data.optimized_experience
    final_resume_json["projects"] = tailored_data.optimized_projects

    # Save Tailored Resume Version to DB
    resume_version = ResumeVersion(
        user_id=current_user.id,
        job_id=job.id,
        content_json=final_resume_json
    )
    db.add(resume_version)

    # Save Cover Letter to DB
    cover_letter = CoverLetter(
        user_id=current_user.id,
        job_id=job.id,
        content=tailored_data.cover_letter_content
    )
    db.add(cover_letter)

    await db.commit()
    await db.refresh(resume_version)
    await db.refresh(cover_letter)

    return {
        "status": "success",
        "resume_version_id": resume_version.id,
        "cover_letter_id": cover_letter.id,
        "message": "Resume and Cover Letter tailored successfully"
    }
