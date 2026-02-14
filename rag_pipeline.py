from langchain_community.llms import Ollama
from vector_store import load_vector_store
from vector_store import compute_match_score

llm = Ollama(model="mistral")

def match_resume_rag(resume_text, top_k=3):
    """
    Retrieve top_k relevant jobs from vector store, score them dynamically,
    and get explanation from LLM
    """
    db = load_vector_store()
    if db is None:
        return []

    docs_scores = db.similarity_search_with_score(resume_text, k=top_k)
    results = []

    for doc, _ in docs_scores:
        jd_text = doc.page_content

        # Compute dynamic score and extract skills
        score, skills = compute_match_score(resume_text, jd_text)

        # LLM explanation
        explanation_prompt = f"""
        Resume:
        {resume_text}

        Job:
        {jd_text}

        Explain the match in 3 concise bullet points.
        """
        explanation = llm.invoke(explanation_prompt)

        results.append({
            "job_description": jd_text,
            "match_score": score,
            "extracted_skills": skills,
            "explanation": explanation
        })

        # Debug print (optional)
        print(f"Fit Score: {score}%, Extracted Skills: {skills}")

    return results
