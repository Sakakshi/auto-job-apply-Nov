from backend.app.services.skill_ai import extract_skills_from_text


def calculate_match(user_skills: list[str], job_description: str):
    job_skills = extract_skills_from_text(job_description)

    user_set = set(s.lower() for s in user_skills)
    job_set = set(s.lower() for s in job_skills)

    matched = list(user_set & job_set)
    missing = list(job_set - user_set)

    match_percentage = int((len(matched) / max(len(job_set), 1)) * 100)

    recommendation = (
        "Excellent match! Auto-apply recommended."
        if match_percentage >= 80
        else "Good match. Consider applying."
        if match_percentage >= 60
        else "Skill gap detected. Upskill before applying."
    )

    return {
        "match_percentage": match_percentage,
        "matched_skills": matched,
        "missing_skills": missing,
        "recommendation": recommendation,
    }
