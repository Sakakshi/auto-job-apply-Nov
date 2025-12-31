from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4
import shutil
import os

from backend.app.db import get_db
from backend.app.models.models import Skill, UserSkill
from backend.app.schemas import ResumeUploadResponse
from backend.app.services.skill_ai import extract_skills_from_text, categorize_skill
from backend.app.services.resume_parser import extract_text_from_resume

router = APIRouter()

UPLOAD_DIR = "uploaded_resumes"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload/{user_id}", response_model=ResumeUploadResponse)
def upload_resume(
    user_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # ----------------------------
    # Save file
    # ----------------------------
    unique_name = f"{uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, unique_name)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # ----------------------------
    # Extract text
    # ----------------------------
    text = extract_text_from_resume(file_path)

    if not text:
        raise HTTPException(400, "Could not extract text from resume")

    # ----------------------------
    # Extract skills (AI)
    # ----------------------------
    extracted_skills = extract_skills_from_text(text)

    # ----------------------------
    # Save skills to DB
    # ----------------------------
    for skill_name in extracted_skills:
        skill = db.query(Skill).filter(
            Skill.skill_name.ilike(skill_name)
        ).first()

        if not skill:
            skill = Skill(
                skill_name=skill_name,
                category=categorize_skill(skill_name)
            )
            db.add(skill)
            db.commit()
            db.refresh(skill)

        # Check mapping
        existing_mapping = db.query(UserSkill).filter(
            UserSkill.user_id == user_id,
            UserSkill.skill_id == skill.id
        ).first()

        if not existing_mapping:
            mapping = UserSkill(
                user_id=user_id,
                skill_id=skill.id,
                proficiency_level="intermediate"
            )
            db.add(mapping)
            db.commit()

    return {
        "filename": file.filename,
        "saved_as": unique_name,
        "extracted_skills": extracted_skills,
        "skill_count": len(extracted_skills)
    }
