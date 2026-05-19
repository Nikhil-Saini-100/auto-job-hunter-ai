import json
import instructor
from openai import AsyncOpenAI
from app.schemas.profile import ParsedResumeStructure
from app.schemas.job import JobResponse
from app.core.config import settings
from pydantic import BaseModel

client = instructor.from_openai(AsyncOpenAI(api_key=settings.OPENAI_API_KEY))

class TailoredContent(BaseModel):
    tailored_summary: str
    optimized_projects: list[dict]
    optimized_experience: list[dict]
    cover_letter_content: str

async def tailor_resume_for_job(job: JobResponse, master_profile: ParsedResumeStructure) -> TailoredContent:
    """
    Uses AI to generate tailored resume sections and a cover letter based on a specific job description.
    """
    if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY == "your_openai_api_key":
        print("Using mock data for Resume Tailor due to placeholder API key.")
        return TailoredContent(
            tailored_summary=f"Dynamic professional ready to excel as {job.title} at {job.company}.",
            optimized_projects=[{"name": "Mock Project", "description": "Did mock things"}],
            optimized_experience=[{"title": "Mock Eng", "company": "Mock Corp", "description": ["Mock bullet"]}],
            cover_letter_content=f"Dear Hiring Manager at {job.company},\n\nI am applying for {job.title}."
        )

    prompt = f"""
    You are an expert career coach and resume writer.
    
    JOB TITLE: {job.title}
    COMPANY: {job.company}
    JOB DESCRIPTION: {job.description}
    
    CANDIDATE MASTER PROFILE:
    {master_profile.model_dump_json()}
    
    TASK:
    1. Write a new, highly-tailored 'tailored_summary' for the candidate that specifically targets this job.
    2. Rewrite the candidate's 'optimized_experience' bullet points to highlight skills mentioned in the job description. Do not invent experience, but emphasize relevant achievements.
    3. Select and optimize the most relevant 'optimized_projects' from the candidate's profile.
    4. Write a professional 'cover_letter_content' addressed to the hiring team at {job.company} for the {job.title} role.
    """

    try:
        tailored = await client.chat.completions.create(
            model="gpt-4o",
            response_model=TailoredContent,
            messages=[
                {"role": "system", "content": "You are a professional resume writer AI."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.4
        )
        return tailored
    except Exception as e:
        print(f"Error tailoring resume: {e}")
        raise
