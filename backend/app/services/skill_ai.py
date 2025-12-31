# backend/app/services/skill_ai.py

import re

# A real system would use OpenAI API / HF model.
# For now we simulate an AI extractor.
COMMON_SKILLS = [
    "Python", "SQL", "FastAPI", "Machine Learning", "Deep Learning",
    "Docker", "Kubernetes", "Pandas", "NumPy", "Data Analysis",
    "NLP", "LLMs", "TensorFlow", "PyTorch", "PostgreSQL"
]

def extract_skills_from_text(text: str) -> list[str]:
    """AI-like regex + keyword extractor."""
    extracted = []

    for skill in COMMON_SKILLS:
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text, re.IGNORECASE):
            extracted.append(skill)

    return extracted


def categorize_skill(skill: str) -> str:
    skill = skill.lower()

    if skill in ["python", "sql", "pandas", "numpy"]:
        return "Programming"
    elif skill in ["tensorflow", "pytorch", "machine learning", "deep learning"]:
        return "ML/AI"
    elif skill in ["docker", "kubernetes"]:
        return "DevOps"
    elif skill in ["fastapi", "postgresql"]:
        return "Backend"
    
    return "General"


def suggest_missing_skills(user_skills: list[str], required_skills: list[str]) -> list[str]:
    """Compare and find missing skills."""
    return list(set(required_skills) - set(user_skills))