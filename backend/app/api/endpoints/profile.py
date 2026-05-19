import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.api import deps
from app.models.user import User, UserProfile
from app.schemas.profile import UserProfileResponse, UserProfileUpdate
from app.services.resume_parser import extract_text_from_file, parse_resume_with_ai

router = APIRouter()

UPLOAD_DIR = "uploads/resumes"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get("/me", response_model=UserProfileResponse)
async def get_profile(
    current_user: User = Depends(deps.get_current_active_user),
    db: AsyncSession = Depends(deps.get_db),
):
    result = await db.execute(select(UserProfile).filter(UserProfile.user_id == current_user.id))
    profile = result.scalars().first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.put("/me", response_model=UserProfileResponse)
async def update_profile(
    profile_update: UserProfileUpdate,
    current_user: User = Depends(deps.get_current_active_user),
    db: AsyncSession = Depends(deps.get_db),
):
    result = await db.execute(select(UserProfile).filter(UserProfile.user_id == current_user.id))
    profile = result.scalars().first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    if profile_update.preferences:
        profile.preferences_json = profile_update.preferences.model_dump()
    if profile_update.parsed_resume:
        profile.parsed_resume_json = profile_update.parsed_resume.model_dump()

    await db.commit()
    await db.refresh(profile)
    return profile

@router.post("/upload-resume", response_model=UserProfileResponse)
async def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(deps.get_current_active_user),
    db: AsyncSession = Depends(deps.get_db),
):
    # Validate file
    if not file.filename.endswith(('.pdf', '.docx', '.doc')):
        raise HTTPException(status_code=400, detail="Only PDF and DOCX files are supported")

    # Save file securely
    file_id = str(uuid.uuid4())
    ext = os.path.splitext(file.filename)[1]
    file_path = os.path.join(UPLOAD_DIR, f"{current_user.id}_{file_id}{ext}")
    
    with open(file_path, "wb") as f:
        f.write(await file.read())
        
    # Extract and parse text
    try:
        raw_text = extract_text_from_file(file_path)
        structured_resume = await parse_resume_with_ai(raw_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse resume: {str(e)}")

    # Update Database
    result = await db.execute(select(UserProfile).filter(UserProfile.user_id == current_user.id))
    profile = result.scalars().first()
    
    profile.master_resume_path = file_path
    profile.parsed_resume_json = structured_resume.model_dump()
    
    await db.commit()
    await db.refresh(profile)
    
    return profile
