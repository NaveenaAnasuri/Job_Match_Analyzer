# Job_Match_Analyzer
AI-powered Resume–Job Match Analyzer using Semantic Similarity, Embeddings, and Vector Search (FAISS) with Flask API backend.  Alternative shorter version:  Semantic Resume–JD Matcher using SentenceTransformers + FAISS + Flask.

🚀 HR – Resume to Job Match Analyzer

An AI-powered system that matches resumes to job descriptions using semantic similarity, dynamic skill extraction, and experience-based scoring.
Instead of simple keyword filtering, this project uses vector embeddings + FAISS search to evaluate real candidate-job fit.

📌 Problem Statement
Recruiters spend significant time manually screening resumes. Traditional keyword search fails to capture contextual meaning.
This system solves that by:
Extracting skills and experience from resumes
Comparing them with job descriptions semantically
Generating explainable match percentages

🧠 How It Works
1️⃣ Resume Parsing:
Extracts multi-word skills
Extracts years of experience (1 year, 3+ yrs, 15+ years)
Converts unstructured text into structured signals

2️⃣ Embedding Generation:
Uses SentenceTransformers
Converts resume & JD into vector embeddings

3️⃣ Vector Search:
FAISS indexes job descriptions
Finds most relevant jobs using nearest neighbor search

4️⃣ Scoring Logic:
Skills %
(Matched JD skills / Total JD skills) × 100
Experience (Years)
Extracted numerically from text
Match %
Skills % + Experience contribution
This ensures scoring is transparent and explainable.

🛠 Tech Stack:
Python
Flask (REST API)
SentenceTransformers
FAISS (Vector Database)
Regex-based Text Extraction
NumPy

📂 Project Structure:
├── main.py              # Flask API
├── vector_store.py      # Embedding + FAISS + Matching Logic
├── scorer.py            # Match scoring logic
├── resume_parser.py     # Resume text extraction
├── requirements.txt

🎯 Learning Outcomes:
✔ Semantic similarity implementation
✔ Embedding-based vector search
✔ Resume/JD text extraction
✔ Scoring logic design
✔ Modular AI system architecture

🚀 Future Improvements:
Dockerization
Cloud deployment
LLM-powered interview insights
Scalable vector DB (Milvus / Pinecone)
Integration with ATS platforms

📈 Impact:
This project demonstrates how AI can streamline hiring workflows by:
Reducing manual screening effort
Improving candidate-job alignment
Providing structured, explainable scoring
