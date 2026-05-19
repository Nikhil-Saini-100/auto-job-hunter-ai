import os
import instructor
from openai import AsyncOpenAI
from pdfminer.high_level import extract_text
from docx import Document
from app.schemas.profile import ParsedResumeStructure
from app.core.config import settings

# Initialize instructor client
client = instructor.from_openai(AsyncOpenAI(api_key=settings.OPENAI_API_KEY))

def extract_text_from_file(file_path: str) -> str:
    """Extracts raw text from a PDF or DOCX file."""
    _, ext = os.path.splitext(file_path)
    if ext.lower() == '.pdf':
        return extract_text(file_path)
    elif ext.lower() in ['.docx', '.doc']:
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    else:
        raise ValueError("Unsupported file format. Please upload a PDF or DOCX.")

async def parse_resume_with_ai(raw_text: str) -> ParsedResumeStructure:
    """
    Uses OpenAI GPT to parse raw unstructured resume text into a strict JSON structure.
    """
    if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY == "your_openai_api_key":
        print("Using mock data for Resume Parsing due to placeholder API key.")
        return ParsedResumeStructure(
            name="John Doe",
            email="test@example.com",
            skills=[{"name": "Python"}, {"name": "React"}],
            experience=[{"title": "Software Engineer", "company": "Tech Corp", "description": ["Did stuff"]}],
            education=[{"degree": "B.S. CS", "institution": "State Univ"}],
            projects=[]
        )

    prompt = f"""
    You are an expert technical recruiter and resume parser.
    Extract the following resume text into a highly structured format.
    Ensure that skills are categorized and experience bullets are preserved.
    
    RESUME TEXT:
    {raw_text}
    """

    try:
        # We use instructor to force the output to match our Pydantic schema
        structured_resume = await client.chat.completions.create(
            model="gpt-4o",
            response_model=ParsedResumeStructure,
            messages=[
                {"role": "system", "content": "You are an expert system that extracts structured data from resumes."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.0
        )
        return structured_resume
    except Exception as e:
        # Fallback or error handling
        print(f"Error parsing resume: {e}")
        raise
