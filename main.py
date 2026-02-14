import os
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from resume_parser import extract_text_from_pdf
from vector_store import add_jobs, match_resume
from utils import convert_numpy

app = FastAPI(title="Resume–Job Match API - Skills + Experience Scoring")

os.makedirs("temp", exist_ok=True)

@app.post("/add_jobs")
async def add_jobs_api(jobs: list[str]):
    """Add job descriptions to the vector store."""
    add_jobs(jobs)
    return {"message": f"{len(jobs)} jobs added successfully."}

@app.post("/match_resume")
async def match_resume_api(resume: UploadFile = File(...), top_k: int = 3):
    """Upload a resume PDF and return top-k job matches with skills & experience scoring."""
    temp_path = os.path.join("temp", resume.filename)
    with open(temp_path, "wb") as f:
        f.write(await resume.read())

    resume_text = extract_text_from_pdf(temp_path)
    results = match_resume(resume_text, top_k=top_k)

    return JSONResponse(content=convert_numpy(results))
