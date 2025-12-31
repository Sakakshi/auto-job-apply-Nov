#backend/app/models/models.py
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, Date, DateTime,
    Text, ForeignKey, Numeric, JSON, ARRAY
)
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.app.db import Base  


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(15))
    default_location = Column(String(100))
    years_of_experience = Column(Numeric(3, 1))
    current_salary = Column(Numeric(10, 2))
    expected_salary = Column(Numeric(10, 2))
    notice_period_days = Column(Integer)
    resume_master_path = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    emails = relationship("UserEmail", back_populates="user")
    preferences = relationship("UserPreference", back_populates="user")
    skills = relationship("UserSkill", back_populates="user")
    work_history = relationship("WorkHistory", back_populates="user")


class UserEmail(Base):
    __tablename__ = "user_emails"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    email = Column(String(255), nullable=False)
    is_primary = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="emails")


class UserPreference(Base):
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    work_mode = Column(String(20))
    preferred_locations = Column(ARRAY(Text))
    target_titles = Column(ARRAY(Text))
    min_salary = Column(Numeric(10, 2))
    max_notice_period = Column(Integer)
    willing_to_relocate = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="preferences")


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True)
    skill_name = Column(String(100), unique=True, nullable=False)
    category = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)


class UserSkill(Base):
    __tablename__ = "user_skills"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    skill_id = Column(Integer, ForeignKey("skills.id", ondelete="CASCADE"))
    proficiency_level = Column(String(20))
    years_of_experience = Column(Numeric(3, 1))
    last_used_year = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="skills")
    skill = relationship("Skill")


class WorkHistory(Base):
    __tablename__ = "work_history"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    company_name = Column(String(200))
    job_title = Column(String(200))
    location = Column(String(100))
    start_date = Column(Date)
    end_date = Column(Date)
    is_current = Column(Boolean, default=False)
    responsibilities = Column(Text)
    achievements = Column(Text)
    technologies_used = Column(ARRAY(Text))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="work_history")

class JobApplication(Base):
    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    job_title = Column(String(200), nullable=False)
    company_name = Column(String(200))
    job_description = Column(Text)

    match_percentage = Column(Integer)
    matched_skills = Column(ARRAY(Text))
    missing_skills = Column(ARRAY(Text))

    status = Column(
        String(50),
        default="recommended"
        # recommended | applied | rejected | interview | offer | needs_upskilling
    )

    applied_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    user = relationship("User", backref="job_applications")

class GmailToken(Base):
    __tablename__ = "gmail_tokens"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    access_token = Column(Text, nullable=False)
    refresh_token = Column(Text, nullable=True)
    token_expiry = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
