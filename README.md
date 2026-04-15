<img width="1917" height="973" alt="image" src="https://github.com/user-attachments/assets/1f1ff857-e359-4cba-90f1-e66b12c25ebc" />\# Smart Resume Analyzer



\## 📌 Overview

This project is an AI-powered system that analyzes resumes and matches them with job descriptions.



\---



\## 🚀 Features

\- Resume parsing (PDF)

\- AI-based information extraction (Gemini LLM)

\- Skill matching

\- Match score generation

\- Smart summary output

\- Simple UI using Streamlit



\---



\## ⚙️ Tech Stack

\- Python

\- FastAPI (Backend API)

\- Streamlit (Frontend UI)

\- Google Gemini API (LLM)

\- pdfplumber (PDF parsing)



\---



\## 🧠 Approach \& Design

1\. Extract text from resume using pdfplumber  

2\. Use Gemini LLM to extract structured data  

3\. Apply rule-based fallback for skills  

4\. Match resume skills with job description  

5\. Generate score and summary  

6\. Display results via API + UI  



\---



\## 📌 Assumptions

\- Resume is in readable PDF format  

\- Job description contains relevant keywords  

\- LLM output may need fallback handling  



\---



\## ▶️ Setup Instructions



\### 1. Install dependencies

pip install -r requirements.txt



\### 2. Add your Gemini API key in main.py



\### 3. Run backend

python -m uvicorn main:app --reload



\### 4. Run frontend

streamlit run app.py



\---



\## 📥 Sample Input

Job Description:

"We are looking for a prompt engineer with skills in Python, NLP, LLMs, API development"



\---



\## 📤 Sample Output

{

"name": "Aryan Singh",

"match\_score": 40,

"matched\_skills": \["python", "llm"],

"missing\_skills": \["nlp", "api"],

"summary": "Candidate matches 2 key skills but is missing important skills."

}



\---


\## 📌 Future Improvements

\- Semantic similarity using embeddings

\- Resume suggestions

\- ATS scoring system


## 📸 LIVE Demo

https://resume-analyzer-mslcu6cdnasmlr6tvacgxe.streamlit.app/#ai-resume-analyzer


