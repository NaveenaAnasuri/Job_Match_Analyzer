# scorer.py
import re

def extract_skills(text):
    """
    Extract skills from text using a simple regex pattern.
    You can expand this with NLP or a predefined list if needed.
    """
    # Assume skills are capitalized words or common tech keywords
    # Simple split by comma, newline, or semicolon
    skills = re.split(r"[,;\n]", text)
    skills = [s.strip().lower() for s in skills if s.strip()]
    return set(skills)

def extract_experience_years(text):
    """
    Extract experience in years from text.
    Looks for patterns like 'X years' or 'X yrs'
    """
    pattern = r"(\d+)\s*(?:years|yrs)"
    matches = re.findall(pattern, text.lower())
    years = [int(m) for m in matches]
    if years:
        return max(years)  # take the maximum mentioned
    return 0

def compute_skills_percent(resume_skills, jd_skills):
    """
    Compute skills percentage as intersection over JD skills.
    """
    if not jd_skills:
        return 0
    matched_skills = resume_skills.intersection(jd_skills)
    return round(len(matched_skills) / len(jd_skills) * 100, 2)

def compute_experience_percent(resume_years, jd_years):
    """
    Compute experience percentage as ratio of resume experience to JD requirement.
    Capped at 100%.
    """
    if jd_years == 0:
        return 100.0
    percent = (resume_years / jd_years) * 100
    return min(round(percent, 2), 100.0)

def score_resume_vs_jd(resume_text, jd_text):
    """
    Returns a dict:
    - skills_percent
    - experience_years
    - experience_percent
    - match_percent (skills + experience)
    """
    # Extract skills
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)

    # Extract experience
    resume_years = extract_experience_years(resume_text)
    jd_years = extract_experience_years(jd_text)

    # Compute scores
    skills_percent = compute_skills_percent(resume_skills, jd_skills)
    experience_percent = compute_experience_percent(resume_years, jd_years)
    match_percent = round(skills_percent + experience_percent, 2)

    return {
        "skills_percent": skills_percent,
        "experience_years": resume_years,
        "experience_percent": experience_percent,
        "match_percent": match_percent
    }
