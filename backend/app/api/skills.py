from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.db import get_db
from backend.app.models.models import Skill
from backend.app.schemas import (
    SkillCreateSchema,
    SkillSchema,
    SkillExtractRequest,
    SkillExtractResponse,
    SkillSuggestResponse,
)
from backend.app.services.skill_ai import (
    extract_skills_from_text,
    categorize_skill,
    suggest_missing_skills,
)

router = APIRouter()


# 1️⃣ Add Skill
@router.post("/", response_model=SkillSchema)
def add_skill(payload: SkillCreateSchema, db: Session = Depends(get_db)):

    category = payload.category or categorize_skill(payload.skill_name)

    existing = db.query(Skill).filter(
        Skill.skill_name.ilike(payload.skill_name)
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Skill already exists")

    skill = Skill(skill_name=payload.skill_name, category=category)
    db.add(skill)
    db.commit()
    db.refresh(skill)
    return skill


# 2️⃣ List Skills
@router.get("/", response_model=list[SkillSchema])
def list_skills(db: Session = Depends(get_db)):
    return db.query(Skill).all()


# 3️⃣ Extract Skills (AI)
@router.post("/extract", response_model=SkillExtractResponse)
def extract_skills(payload: SkillExtractRequest):

    extracted = extract_skills_from_text(payload.text)

    return {
        "extracted_skills": extracted,
        "count": len(extracted),
    }


# 4️⃣ Skill Gap Analysis
@router.post("/suggest", response_model=SkillSuggestResponse)
def suggest_skills(payload: dict):

    user_skills = payload.get("user_skills", [])
    required_skills = payload.get("required_skills", [])

    missing = suggest_missing_skills(user_skills, required_skills)

    return {
        "required_skills": required_skills,
        "missing_skills": missing,
    }
