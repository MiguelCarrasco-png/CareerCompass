"""
CareerCompass: SHPE Opportunity Analyzer
Fully integrated Streamlit app with backend ML/scraping functionality
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from collections import Counter

# Import your backend functions
from src.scraper import scrape_all_job_data
from src.nlp_processor import get_skill_counts, compare_skills, read_pdf_text, extract_skills

def main():
    """Main function to run the Streamlit app."""
    
    # --- Page Configuration ---
    st.set_page_config(
        page_title="CareerCompass: SHPE Opportunity Analyzer",
        page_icon="🚀",
        layout="wide"
    )

    # --- Sidebar Navigation ---
    st.sidebar.title("🧭 Navigation")
    page_selection = st.sidebar.radio(
        "Go to",
        [
            "🏠 Home",
            "📊 In-Demand Skills Dashboard",
            "📄 Resume Matcher"
        ]
    )
    
    # Add info in sidebar
    st.sidebar.markdown("---")
    st.sidebar.info(
        "**CareerCompass** helps SHPE members understand what skills "
        "are in demand and how their resume matches job opportunities."
    )

    # --- Page Content ---
    
    # HOME PAGE
    if page_selection == "🏠 Home":
        st.title("Welcome to CareerCompass 🚀")
        st.subheader("The SHPE Opportunity & Skill Analyzer")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            ### What is CareerCompass?
            
            CareerCompass is a powerful tool designed specifically for **SHPE UF members** to:
            
            - 📊 **Discover In-Demand Skills**: See what technical skills our sponsor companies are actively seeking
            - 📄 **Match Your Resume**: Upload your resume and see how you stack up against real job postings
            - 🎯 **Identify Skill Gaps**: Know exactly what skills to learn next to boost your career prospects
            
            ### How It Works
            
            1. **We analyze job postings** from SHPE sponsor companies (Google, Lockheed Martin, Texas Instruments, and more)
            2. **Our NLP engine extracts skills** from job descriptions using machine learning
            3. **You get actionable insights** about what to learn and how you compare
            
            ---
            
            ### Get Started
            
            Use the **navigation panel on the left** to:
            - 📊 View the **In-Demand Skills Dashboard** to see trending skills
            - 📄 Try the **Resume Matcher** to analyze your resume against job postings
            """)
        
        with col2:
            st.markdown("### 📈 Quick Stats")
            
            # Show some stats
            if st.button("🔍 Analyze Current Job Market"):
                with st.spinner("Analyzing..."):
                    jobs = scrape_all_job_data(use_test_data=True)
                    skills = get_skill_counts(jobs)
                    
                    st.metric("Total Jobs Analyzed", len(jobs))
                    st.metric("Companies Tracked", len(set(j['company'] for j in jobs)))
                    st.metric("Unique Skills Found", len(skills))
                    
                    top_skill = max(skills.items(), key=lambda x: x[1])
                    st.metric("Most In-Demand Skill", top_skill[0].title(), f"{top_skill[1]} jobs")
    
    # DASHBOARD PAGE
    elif page_selection == "📊 In-Demand Skills Dashboard":
        st.title("📊 In-Demand Skills Dashboard")
        st.markdown("See what skills SHPE sponsor companies are looking for right now!")
        
        # Add controls
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.markdown("### Controls")
            top_n = st.slider("Number of skills to show", 5, 20, 15)
            
            if st.button("🔍 Analyze Jobs", type="primary", use_container_width=True):
                st.session_state['run_analysis'] = True
        
        # Run analysis
        if st.session_state.get('run_analysis', False):
            with st.spinner('🔄 Scraping job postings and analyzing skills...'):
                # Get data from your backend
                jobs = scrape_all_job_data(use_test_data=True)
                skill_counts = get_skill_counts(jobs)
                
                # Store in session state
                st.session_state['jobs'] = jobs
                st.session_state['skill_counts'] = skill_counts
            
            st.success(f"✅ Analyzed {len(jobs)} jobs from {len(set(j['company'] for j in jobs))} companies!")
        
        # Display results if available
        if 'skill_counts' in st.session_state:
            skill_counts = st.session_state['skill_counts']
            jobs = st.session_state['jobs']
            
            # Get top N skills
            top_skills = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:top_n]
            skills = [s[0].title() for s in top_skills]
            counts = [s[1] for s in top_skills]
            
            # Create horizontal bar chart
            fig = go.Figure(data=[
                go.Bar(
                    y=skills[::-1],  # Reverse to show highest at top
                    x=counts[::-1],
                    orientation='h',
                    marker=dict(
                        color=counts[::-1],
                        colorscale='Viridis',
                        showscale=True,
                        colorbar=dict(title="Count")
                    ),
                    text=counts[::-1],
                    textposition='auto',
                )
            ])
            
            fig.update_layout(
                title=f"Top {top_n} In-Demand Skills Across SHPE Sponsor Companies",
                xaxis_title="Number of Job Postings Mentioning Skill",
                yaxis_title="Technical Skill",
                height=600,
                showlegend=False,
                hovermode='y'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Show breakdown by company
            st.markdown("### 📋 Skills by Company")
            
            # Create company breakdown
            company_skills = {}
            for job in jobs:
                company = job['company']
                job_skills = extract_skills(job['description'])
                if company not in company_skills:
                    company_skills[company] = Counter()
                company_skills[company].update(job_skills)
            
            # Display in columns
            cols = st.columns(len(company_skills))
            for idx, (company, skills_counter) in enumerate(company_skills.items()):
                with cols[idx]:
                    st.markdown(f"**{company}**")
                    top_3 = skills_counter.most_common(3)
                    for skill, count in top_3:
                        st.write(f"• {skill.title()}: {count}")
    
    # RESUME MATCHER PAGE
    elif page_selection == "📄 Resume Matcher":
        st.title("📄 Resume Matcher")
        st.markdown("Upload your resume and see how you match against real job postings!")
        
        # Two column layout
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### Step 1: Upload Your Resume")
            uploaded_file = st.file_uploader(
                "Choose your resume (PDF or TXT)",
                type=['pdf', 'txt'],
                help="We'll extract skills from your resume to match against job postings"
            )
            
            if uploaded_file:
                st.success(f"✅ Uploaded: {uploaded_file.name}")
                
                # Extract text from resume
                if uploaded_file.type == "application/pdf":
                    resume_text = read_pdf_text(uploaded_file)
                else:
                    resume_text = uploaded_file.read().decode('utf-8')
                
                st.session_state['resume_text'] = resume_text
                
                # Show preview
                with st.expander("📄 Resume Preview (first 500 characters)"):
                    st.text(resume_text[:500] + "...")
        
        with col2:
            st.markdown("### Step 2: Select a Job")
            
            # Get jobs
            jobs = scrape_all_job_data(use_test_data=True)
            
            # Create job selection dropdown
            job_options = [f"{job['company']} - {job['title']}" for job in jobs]
            selected_job_idx = st.selectbox(
                "Choose a job to match against",
                range(len(job_options)),
                format_func=lambda x: job_options[x]
            )
            
            selected_job = jobs[selected_job_idx]
            
            # Show job description
            with st.expander("📋 View Job Description"):
                st.markdown(f"**Company:** {selected_job['company']}")
                st.markdown(f"**Title:** {selected_job['title']}")
                st.markdown(f"**Description:**")
                st.write(selected_job['description'])
        
        # Match button
        st.markdown("---")
        
        if st.button("🎯 Calculate Match Score", type="primary", use_container_width=True):
            if 'resume_text' not in st.session_state:
                st.error("⚠️ Please upload your resume first!")
            else:
                with st.spinner("🔄 Analyzing your resume..."):
                    resume_text = st.session_state['resume_text']
                    job_text = selected_job['description']
                    
                    # Get comparison
                    comparison = compare_skills(resume_text, job_text)
                    
                    st.session_state['comparison'] = comparison
        
        # Display results
        if 'comparison' in st.session_state:
            comparison = st.session_state['comparison']
            
            st.markdown("---")
            st.markdown("## 📊 Match Results")
            
            # Show match score with color coding
            score = comparison['score']
            if score >= 70:
                score_color = "🟢"
                message = "Excellent match! You have most of the required skills."
            elif score >= 50:
                score_color = "🟡"
                message = "Good match! Consider learning a few more skills to strengthen your application."
            else:
                score_color = "🔴"
                message = "There's room for improvement. Focus on building the missing skills below."
            
            st.markdown(f"### {score_color} Match Score: {score}%")
            st.info(message)
            
            # Create three columns for detailed breakdown
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "Skills You Have",
                    len(comparison['skills_you_have']),
                    f"out of {comparison['total_job_skills']}"
                )
            
            with col2:
                st.metric(
                    "Skills to Learn",
                    len(comparison['skills_you_are_missing'])
                )
            
            with col3:
                st.metric(
                    "Your Total Skills",
                    comparison['total_resume_skills']
                )
            
            # Show detailed lists
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### ✅ Skills You Have")
                if comparison['skills_you_have']:
                    for skill in comparison['skills_you_have']:
                        st.markdown(f"- **{skill.title()}**")
                else:
                    st.write("No matching skills found. Consider adding relevant skills to your resume!")
            
            with col2:
                st.markdown("### 📚 Skills to Learn")
                if comparison['skills_you_are_missing']:
                    for skill in comparison['skills_you_are_missing']:
                        st.markdown(f"- {skill.title()}")
                else:
                    st.write("You have all required skills! 🎉")
            
            # Recommendations
            if comparison['skills_you_are_missing']:
                st.markdown("---")
                st.markdown("### 💡 Recommendations")
                st.markdown(f"""
                To improve your match for this role, consider:
                
                1. **Priority Skills**: Focus on learning {', '.join(comparison['skills_you_are_missing'][:3])}
                2. **Online Resources**: Check out Coursera, Udemy, or LinkedIn Learning for courses
                3. **Build Projects**: Create portfolio projects that use these technologies
                4. **Update Resume**: Make sure your resume clearly lists your technical skills
                """)

if __name__ == "__main__":
    main()