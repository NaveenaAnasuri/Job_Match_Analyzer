import re
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from scorer import compute_fit_score

EMBEDDING_DIM = 384
model = SentenceTransformer("all-MiniLM-L6-v2")

job_texts = []
index = faiss.IndexFlatL2(EMBEDDING_DIM)

# -----------------------------
# Skills Extraction
# -----------------------------
def extract_skills_from_text(text: str):
    """
    Extract skills dynamically from text.
    - Assume skills are comma-separated or capitalized words.
    - Simple approach: pick words with 2+ characters starting with uppercase or separated by commas.
    """
    # Comma-separated words
    skills = []
    for part in text.split(","):
        word = part.strip()
        if len(word) > 1:
            skills.append(word.lower())
    
    # Also catch words like Python, SQL, etc. (Capitalized)
    capitalized = re.findall(r'\b[A-Z][a-zA-Z0-9+\-#]+\b', text)
    skills.extend([w.lower() for w in capitalized])
    
    return set(skills)

# -----------------------------
# Robust Experience Extraction
# -----------------------------
def extract_experience(text: str):
    """
    Extract total years of experience from text.
    Supports all numbers (1, 2, 3, 10, 15+) and variations:
    - 1 year, 1+ year, 1 yr, 1+ yrs, 1 year of experience
    - 10 years, 15+ yrs, 20+ years of experience
    """
    # Match numbers followed by optional '+' and 'year', 'years', 'yr', 'yrs'
    exp_pattern = r'(\d+)\s*\+?\s*(?:year|years|yr|yrs)\b'
    matches = re.findall(exp_pattern, text, flags=re.IGNORECASE)

    # Convert all matches to integers and sum if multiple are present
    total_exp = sum([int(x) for x in matches]) if matches else 0
    return total_exp

# -----------------------------
# Job Index Functions
# -----------------------------
def add_jobs(jobs: list[str]):
    """Add job descriptions to FAISS index."""
    global job_texts, index
    embeddings = model.encode(jobs).astype("float32")
    index.add(embeddings)
    job_texts.extend(jobs)

def match_resume(resume_text: str, top_k: int = 3):
    """Match resume with jobs based on dynamic skills from JD and experience."""
    resume_skills = extract_skills_from_text(resume_text)
    resume_exp = extract_experience(resume_text)

    resume_embedding = model.encode([resume_text]).astype("float32")
    distances, indices = index.search(resume_embedding, k=min(top_k, len(job_texts)))

    results = []
    for dist, idx in zip(distances[0], indices[0]):
        jd_text = job_texts[idx]
        jd_skills = extract_skills_from_text(jd_text)
        jd_exp = extract_experience(jd_text)

        # Skills %
        if jd_skills:
            matched_skills = resume_skills & jd_skills
            skills_percent = round(len(matched_skills) / len(jd_skills) * 100, 2)
        else:
            skills_percent = 0.0

        # Experience contribution
        exp_contribution = min(resume_exp, jd_exp)

        # Final match %
        match_percent = compute_fit_score(skills_percent, exp_contribution)

        results.append({
            "job": jd_text,
            "skills_percent": skills_percent,
            "experience_years": resume_exp,
            "experience_required": jd_exp,
            "match_percent": match_percent
        })
    return results
