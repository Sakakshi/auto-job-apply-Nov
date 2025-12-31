from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

# -------------------------------
# User Create Schema
# -------------------------------
class UserCreateSchema(BaseModel):
    name: str
    phone: str | None = None
    default_location: str | None = None
    years_of_experience: float | None = None


# -------------------------------
# User Response Schema
# -------------------------------
class UserSchema(BaseModel):
    id: int
    name: str
    phone: str | None
    default_location: str | None
    years_of_experience: float | None
    current_salary: float | None = None
    expected_salary: float | None = None
    notice_period_days: int | None = None
    resume_master_path: str | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# -------------------------------
# User Update Schema
# -------------------------------
class UserUpdateSchema(BaseModel):
    name: str | None = None
    phone: str | None = None
    default_location: str | None = None
    years_of_experience: float | None = None



# ------------------------------------------------------
# Skill Master Table Schemas
# ------------------------------------------------------
class SkillCreateSchema(BaseModel):
    skill_name: str
    category: str | None = None


class SkillSchema(BaseModel):
    id: int
    skill_name: str
    category: str | None
    created_at: datetime

    class Config:
        from_attributes = True


# ------------------------------------------------------
# User-Skill Mapping Schemas
# ------------------------------------------------------
class UserSkillCreateSchema(BaseModel):
    skill_id: int
    proficiency_level: str
    years_of_experience: float
    last_used_year: int | None = None


class UserSkillSchema(BaseModel):
    id: int
    user_id: int
    skill_id: int
    proficiency_level: str
    years_of_experience: float
    last_used_year: int | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
class SkillExtractRequest(BaseModel):
    text: str

class SkillSuggestResponse(BaseModel):
    missing_skills: list[str]
    suggested_for_role: str

    class Config:
        from_attributes = True    

class SkillExtractResponse(BaseModel):
    extracted_skills: list[str]
    count: int

# ------------------------------------------------------
# Resume Upload Response
# ------------------------------------------------------
class ResumeUploadResponse(BaseModel):
    filename: str
    saved_as: str
    extracted_skills: list[str]
    skill_count: int


# ------------------------------------------------------
# Job Matching Schemas
# ------------------------------------------------------

class JobMatchResponse(BaseModel):
    match_percentage: int
    matched_skills: list[str]
    missing_skills: list[str]
    recommendation: str

class JobMatchRequest(BaseModel):
    job_title: str
    job_description: str
    company_name: str | None = None


class JobApplicationSchema(BaseModel):
    id: int
    job_title: str
    company_name: str | None
    match_percentage: int
    matched_skills: list[str]
    missing_skills: list[str]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class JobApplicationResponse(BaseModel):
    id: int
    job_title: str
    company_name: Optional[str]
    match_percentage: int
    matched_skills: List[str]
    missing_skills: List[str]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class JobStatusUpdateSchema(BaseModel):
    status: str
