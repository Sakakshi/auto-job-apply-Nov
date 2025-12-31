from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime

from backend.app.db import get_db
from backend.app.models.models import JobApplication, UserSkill
from backend.app.schemas import (
    JobMatchRequest,
    JobApplicationSchema,
    JobStatusUpdateSchema,
)
from backend.app.services.job_matcher import calculate_match

router = APIRouter(prefix="/jobs", tags=["Jobs"])


# ---------------------------------------------------------
# 1️⃣ Match job + save application
# ---------------------------------------------------------
@router.post("/match/{user_id}", response_model=JobApplicationSchema)
def match_and_save_job(
    user_id: int,
    payload: JobMatchRequest,
    db: Session = Depends(get_db),
):
    user_skills = (
        db.query(UserSkill)
        .filter(UserSkill.user_id == user_id)
        .all()
    )

    if not user_skills:
        raise HTTPException(400, "User has no skills")

    skill_names = [us.skill.skill_name for us in user_skills]

    result = calculate_match(skill_names, payload.job_description)

    job = JobApplication(
        user_id=user_id,
        job_title=payload.job_title,
        company_name=payload.company_name,
        job_description=payload.job_description,
        match_percentage=result["match_percentage"],
        matched_skills=result["matched_skills"],
        missing_skills=result["missing_skills"],
        status="recommended"
        if result["match_percentage"] >= 60
        else "needs_upskilling",
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return job


# ---------------------------------------------------------
# 2️⃣ Apply to job
# ---------------------------------------------------------
@router.post("/apply/{job_id}")
def apply_to_job(
    job_id: int,
    db: Session = Depends(get_db),
):
    job = db.query(JobApplication).filter(
        JobApplication.id == job_id
    ).first()

    if not job:
        raise HTTPException(404, "Job not found")

    if job.status == "applied":
        raise HTTPException(400, "Already applied")

    job.status = "applied"
    job.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(job)

    return {
        "message": "Job applied successfully",
        "job_id": job.id,
        "status": job.status,
    }


# ---------------------------------------------------------
# 3️⃣ Update job status (interview / offer / rejected)
# ---------------------------------------------------------
@router.patch("/{job_id}/status")
def update_job_status(
    job_id: int,
    payload: JobStatusUpdateSchema,
    db: Session = Depends(get_db),
):
    job = db.query(JobApplication).filter(
        JobApplication.id == job_id
    ).first()

    if not job:
        raise HTTPException(404, "Job not found")

    job.status = payload.status
    job.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(job)

    return {"message": "Status updated"}


# ---------------------------------------------------------
# 4️⃣ List all jobs for a user (dashboard)
# ---------------------------------------------------------
@router.get(
    "/user/{user_id}",
    response_model=List[JobApplicationSchema],
)
def get_user_jobs(
    user_id: int,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(JobApplication).filter(
        JobApplication.user_id == user_id
    )

    if status:
        query = query.filter(JobApplication.status == status)

    return (
        query.order_by(JobApplication.created_at.desc())
        .all()
    )
