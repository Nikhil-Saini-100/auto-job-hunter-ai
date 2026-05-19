import instructor
from openai import AsyncOpenAI
from app.schemas.job import MatchAnalysis
from app.schemas.profile import ParsedResumeStructure
from app.core.config import settings

client = instructor.from_openai(AsyncOpenAI(api_key=settings.OPENAI_API_KEY))

async def analyze_job_match(job_description: str, profile: ParsedResumeStructure) -> MatchAnalysis:
    """
    Uses OpenAI to analyze a job description against a structured resume profile.
    Returns a structured analysis including a match score and missing skills.
    """
    if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY == "your_openai_api_key":
        print("Using mock data for Job Match due to placeholder API key.")
        return MatchAnalysis(
            match_score=85,
            matched_skills=["React", "Python"],
            missing_skills=["AWS"],
            strengths=["Frontend Development"],
            match_explanation="Candidate has strong frontend skills but lacks deep AWS experience.",
            recommendation="apply_now"
        )

    prompt = f"""
    You are an expert technical recruiter AI.
    Analyze the following Job Description against the Candidate's Resume Profile.
    
    JOB DESCRIPTION:
    {job_description}
    
    CANDIDATE PROFILE:
    {profile.model_dump_json()}
    
    Provide a realistic match score from 0 to 100 based on how well the candidate's skills and experience align with the job requirements.
    List the matched skills, missing skills, and strengths.
    Determine the recommendation: "apply_now", "tailor_resume", or "skip".
    """

    try:
        analysis = await client.chat.completions.create(
            model="gpt-4o",
            response_model=MatchAnalysis,
            messages=[
                {"role": "system", "content": "You are an AI job matcher that outputs precise JSON."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.1
        )
        return analysis
    except Exception as e:
        print(f"Error matching job: {e}")
        raise
