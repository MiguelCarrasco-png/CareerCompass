import streamlit as st

# --- Resume Matcher Page ---

#elif page_selection == "📄 Resume Matcher":
st.title("📄 Resume Matcher")
st.write("Upload your resume to see which jobs best match your skills!")

st.markdown("---")

    # === 1. Upload Resume ===
uploaded_resume = st.file_uploader(
        "Upload your resume (PDF or TXT)",
        type=["pdf", "txt"]
    )

    # === 2. Load Job Postings (Temporary Placeholder) ===
job_postings = {
        "Software Engineering Intern – Google": "Python, C++, Machine Learning, Git, API Development",
        "Mechanical Engineering Intern – Tesla": "CAD, SolidWorks, FEA, Manufacturing, MATLAB",
        "Data Analyst Intern – Meta": "SQL, Python, Data Visualization, Dashboards, Excel",
        "Cybersecurity Intern – Lockheed Martin": "Linux, Networking, Python, Security Tools, Risk Analysis",
        "Cloud Engineering Intern – Amazon": "AWS, Python, Docker, Kubernetes, CI/CD"
    }

st.markdown("---")

    # === 3. Run Matcher ===
if st.button("🔍 Find Matching Jobs!", type="primary"):

        if not uploaded_resume:
            st.error("Please upload your resume first.")
            st.stop()

        st.info("Extracting skills and matching your resume...")

        # =====================================
        # 🔗 BACKEND PLACEHOLDERS – REPLACE LATER
        # =====================================
        # Example skills extracted from resume
        extracted_resume_skills = ["Python", "Git", "SQL"]

        # Ranking jobs by match %
        results = []
        for job_title, jd_text in job_postings.items():

            jd_skills = [skill.strip() for skill in jd_text.split(",")]

            matched = list(set(extracted_resume_skills) & set(jd_skills))
            missing = list(set(jd_skills) - set(extracted_resume_skills))

            match_score = int((len(matched) / len(jd_skills)) * 100)

            results.append({
                "title": job_title,
                "jd_skills": jd_skills,
                "matched": matched,
                "missing": missing,
                "score": match_score
            })

        # Sort jobs by match score (descending)
        results = sorted(results, key=lambda x: x["score"], reverse=True)
        # =====================================

        st.markdown("## 🔥 Best Matching Job Postings for You")

        # Show results
        for job in results:

            st.markdown(f"### **{job['title']}**")
            st.metric("Match Score", f"{job['score']}%")

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("✔️ Matched Skills")
                if job["matched"]:
                    for s in job["matched"]:
                        st.success(s)
                else:
                    st.write("No matching skills.")

            with col2:
                st.subheader("❌ Missing Skills")
                if job["missing"]:
                    for s in job["missing"]:
                        st.error(s)
                else:
                    st.write("You meet all required skills!")

            st.markdown("---")
