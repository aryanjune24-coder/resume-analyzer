import streamlit as st
import requests

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🚀",
    layout="wide"
)

# 🎨 Premium Styling
st.markdown("""
<style>
body {
    background-color: #0f172a;
}
h1, h2, h3, p {
    color: white;
}
.block-container {
    padding-top: 2rem;
}
.stButton>button {
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    color: white;
    border-radius: 12px;
    height: 50px;
    font-size: 18px;
    width: 100%;
}
.card {
    padding: 20px;
    border-radius: 15px;
    background: #1e293b;
    margin: 10px 0;
}
</style>
""", unsafe_allow_html=True)

# 🔥 Header
st.title("🚀 AI Resume Analyzer")
st.caption("Automating Resume Screening with AI")

st.divider()

# 🎯 Input Section
col1, col2 = st.columns(2)

with col1:
    st.subheader("📄 Upload Resume")
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

with col2:
    st.subheader("🧠 Job Description")
    job_desc = st.text_area("Paste job description", height=180)

# 🚀 Analyze Button
if st.button("⚡ Analyze Resume"):
    if uploaded_file and job_desc:

        progress = st.progress(0)
        status = st.empty()

        # Fake smooth progress animation
        for i in range(100):
            progress.progress(i + 1)
            status.text(f"Processing... {i+1}%")

        try:
            files = {"resume": uploaded_file}
            data = {"job_desc": job_desc}

            response = requests.post(
                "https://resume-backend.onrender.com/analyze",
                files=files,
                data=data
            )

            result = response.json()

            progress.empty()
            status.empty()

            st.success("✅ Analysis Complete")

            # 🔥 Score Section
            st.subheader("📊 Match Score")

            score = result["match_score"]

            st.progress(score / 100)

            if score > 70:
                st.success(f"🔥 Excellent Match: {score}%")
            elif score > 40:
                st.warning(f"⚡ Moderate Match: {score}%")
            else:
                st.error(f"❌ Low Match: {score}%")

            # 🔥 Metrics
            col1, col2, col3 = st.columns(3)

            col1.metric("Matched Skills", len(result["matched_skills"]))
            col2.metric("Missing Skills", len(result["missing_skills"]))
            col3.metric("Score", f"{score}%")

            st.divider()

            # 🔥 Skills Section
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("✅ Matched Skills")
                for skill in result["matched_skills"]:
                    st.success(skill)

            with col2:
                st.subheader("❌ Missing Skills")
                for skill in result["missing_skills"]:
                    st.error(skill)

            st.divider()

            # 🔥 Summary Section
            st.subheader("📌 AI Summary")
            st.info(result["summary"])

        except Exception as e:
            st.error("Backend not running or error occurred.")
            st.text(str(e))

    else:
        st.warning("Please upload resume and enter job description")