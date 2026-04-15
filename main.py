from fastapi import FastAPI, UploadFile, File, Form
import pdfplumber
import google.generativeai as genai
import json

# 🔑 ADD YOUR GEMINI API KEY HERE (CHANGE AFTER SUBMISSION)
import os
genai.configure(api_key=os.getenv("AIzaSyBMnBqhNWZAHKCeLQTBsikcVieqBbZ0qSM"))

app = FastAPI(title="Smart Resume Analyzer")


# 📄 Extract text from PDF
def extract_text(file):
    with pdfplumber.open(file) as pdf:
        text = " ".join(page.extract_text() or "" for page in pdf.pages)

    if not text.strip():
        return "No content found in resume"

    return text


# 🤖 LLM Extraction
def extract_with_llm(text):
    prompt = f"""
    You are an expert resume parser.

    Extract:
    - Name
    - Skills (list of technical skills)
    - Education
    - Experience (years)

    Return ONLY valid JSON:
    {{
      "name": "",
      "skills": [],
      "education": "",
      "experience": ""
    }}

    Resume:
    {text}
    """

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)

        cleaned = response.text.strip()

        # Fix JSON formatting
        if "```json" in cleaned:
            cleaned = cleaned.split("```json")[1].split("```")[0]
        elif "```" in cleaned:
            cleaned = cleaned.split("```")[1]

        return json.loads(cleaned)

    except Exception as e:
        print("LLM ERROR:", e)
        return {
            "name": "",
            "skills": [],
            "education": "",
            "experience": ""
        }


# ⚙️ Matching Logic
def match_skills(resume_skills, job_desc):
    job_desc = job_desc.lower()

    job_skills = [
        "python", "nlp", "llm", "api", "machine learning"
    ]

    resume_skills_lower = [s.lower() for s in resume_skills]

    matched = [s for s in resume_skills_lower if s in job_desc]
    missing = [s for s in job_skills if s not in resume_skills_lower]

    score = int((len(matched) / max(len(job_skills), 1)) * 100)

    return score, matched, missing


# 🔁 Fallback skill extraction (stronger)
def simple_skill_extract(text):
    common_skills = [
        "python", "java", "sql", "machine learning", "nlp",
        "deep learning", "api", "fastapi", "flask",
        "docker", "aws", "git", "pandas", "numpy",
        "tensorflow", "pytorch", "llm", "prompt engineering",
        "data analysis", "scikit-learn"
    ]

    found = []
    text_lower = text.lower()

    for skill in common_skills:
        if skill in text_lower:
            found.append(skill)

    return found


# 🧠 Smart summary
def generate_summary(matched, missing):
    if not matched:
        return "Candidate lacks key required skills for this role."

    if len(missing) == 0:
        return "Excellent match. Candidate meets all key skill requirements."

    return f"Candidate matches {len(matched)} key skills but is missing {len(missing)} important skills like {', '.join(missing[:3])}."


# 🧠 Name extraction fallback
def extract_name(text):
    lines = text.strip().split("\n")

    for line in lines[:5]:
        if 1 < len(line.split()) <= 4:
            return line.strip()

    return "Unknown"


# 🚀 API
@app.get("/")
def home():
    return {"message": "Resume Analyzer API is live 🚀"}

@app.post("/analyze")
async def analyze(resume: UploadFile = File(...), job_desc: str = Form(...)):
    try:
        # Step 1: Extract text
        text = extract_text(resume.file)
        print("TEXT LENGTH:", len(text))

        # Step 2: LLM extraction
        extracted = extract_with_llm(text)

        # Step 3: Skills
        skills = extracted.get("skills", [])

        # Step 4: fallback if empty
        if not skills:
            skills = simple_skill_extract(text)

        print("SKILLS:", skills)

        # Step 5: Matching
        score, matched, missing = match_skills(skills, job_desc)

        # Step 6: Name fix
        name = extracted.get("name") or extract_name(text)

        return {
            "name": name,
            "match_score": score,
            "matched_skills": matched,
            "missing_skills": missing[:10],
            "summary": generate_summary(matched, missing)
        }

    except Exception as e:
        print("ERROR:", e)
        return {"error": str(e)}
        
