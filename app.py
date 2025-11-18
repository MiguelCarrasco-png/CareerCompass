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
    
    # Custom CSS for better styling
    st.markdown("""
        <style>
        /* Main container styling */
        .main > div {
            padding-top: 2rem;
        }
        
        /* Skill badge styling */
        .skill-badge {
            display: inline-block;
            padding: 0.4rem 0.8rem;
            margin: 0.3rem;
            border-radius: 20px;
            font-weight: 500;
            font-size: 0.9rem;
        }
        
        .skill-have {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        
        .skill-missing {
            background-color: #fff3cd;
            color: #856404;
            border: 1px solid #ffeeba;
        }
        
        .skill-all {
            background-color: #e3f2fd;
            color: #0d47a1;
            border: 1px solid #90caf9;
        }
        
        /* Metric styling */
        [data-testid="stMetricValue"] {
            font-size: 2rem;
        }
        
        /* Button styling */
        .stButton > button {
            width: 100%;
            border-radius: 10px;
            height: 3rem;
            font-weight: 600;
        }
        
        /* Info box styling */
        .info-box {
            padding: 1.5rem;
            border-radius: 10px;
            background-color: #f8f9fa;
            border-left: 4px solid #0066cc;
            margin: 1rem 0;
        }
        </style>
    """, unsafe_allow_html=True)

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
            
            # Create horizontal bar chart with CLEAN HOVER
            fig = go.Figure(data=[
                go.Bar(
                    y=skills[::-1],  # Reverse to show highest at top
                    x=counts[::-1],
                    orientation='h',
                    marker=dict(
                        color=counts[::-1],
                        colorscale='Viridis',
                        showscale=False,
                    ),
                    text=counts[::-1],
                    textposition='auto',
                    textfont=dict(size=12, color='white', family='Arial'),
                    # CLEAN HOVER - No extra info
                    hoverinfo='none',  # Disable default hover
                    customdata=counts[::-1],
                )
            ])
            
            # Add custom hover using annotations
            fig.update_traces(
                hovertemplate='<b>%{y}</b><br>Mentioned in %{x} job postings<extra></extra>'
            )
            
            fig.update_layout(
                title={
                    'text': f"Top {top_n} In-Demand Skills Across SHPE Sponsor Companies",
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 20, 'color': '#1f1f1f', 'family': 'Arial'}
                },
                xaxis_title="Number of Job Postings",
                yaxis_title="",
                height=600,
                showlegend=False,
                plot_bgcolor='rgba(250,250,250,0.5)',
                paper_bgcolor='white',
                font=dict(size=12, family='Arial'),
                margin=dict(l=150, r=50, t=80, b=50),
                xaxis=dict(
                    showgrid=True,
                    gridcolor='rgba(200,200,200,0.3)',
                    zeroline=False,
                ),
                yaxis=dict(
                    showgrid=False,
                ),
                hoverlabel=dict(
                    bgcolor="white",
                    font_size=14,
                    font_family="Arial"
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Show breakdown by company
            st.markdown("---")
            st.markdown("### 📋 Skills by Company")
            
            # Create company breakdown
            company_skills = {}
            for job in jobs:
                company = job['company']
                job_skills = extract_skills(job['description'])
                if company not in company_skills:
                    company_skills[company] = Counter()
                company_skills[company].update(job_skills)
            
            # Display in columns with better formatting
            cols = st.columns(len(company_skills))
            for idx, (company, skills_counter) in enumerate(company_skills.items()):
                with cols[idx]:
                    st.markdown(f"#### {company}")
                    top_3 = skills_counter.most_common(3)
                    for rank, (skill, count) in enumerate(top_3, 1):
                        st.markdown(f"`{rank}.` **{skill.title()}** - {count} jobs")
    
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
                
                # Extract and display ALL skills from resume
                resume_skills = extract_skills(resume_text)
                st.session_state['all_resume_skills'] = list(resume_skills.keys())
                
                # Show skills found in resume
                if resume_skills:
                    st.markdown("#### 🔍 Skills Detected in Your Resume:")
                    skills_html = ""
                    for skill in sorted(resume_skills.keys()):
                        skills_html += f'<span class="skill-badge skill-all">{skill.title()}</span>'
                    st.markdown(skills_html, unsafe_allow_html=True)
                else:
                    st.warning("⚠️ No technical skills detected. Make sure your resume lists your technical skills clearly.")
                
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
                progress_color = "green"
            elif score >= 50:
                score_color = "🟡"
                message = "Good match! Consider learning a few more skills to strengthen your application."
                progress_color = "orange"
            else:
                score_color = "🔴"
                message = "There's room for improvement. Focus on building the missing skills below."
                progress_color = "red"
            
            # Big score display
            st.markdown(f"### {score_color} Match Score: {score}%")
            st.progress(score / 100)
            st.info(message)
            
            # Create three columns for detailed breakdown
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "Matching Skills",
                    len(comparison['skills_you_have']),
                    f"out of {comparison['total_job_skills']} required"
                )
            
            with col2:
                st.metric(
                    "Skills Gap",
                    len(comparison['skills_you_are_missing'])
                )
            
            with col3:
                st.metric(
                    "Total Resume Skills",
                    comparison['total_resume_skills']
                )
            
            st.markdown("---")
            
            # THREE COLUMN SKILL DISPLAY
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("### ✅ Skills You Have")
                st.caption("Skills that match this job")
                if comparison['skills_you_have']:
                    skills_html = ""
                    for skill in sorted(comparison['skills_you_have']):
                        skills_html += f'<span class="skill-badge skill-have">{skill.title()}</span>'
                    st.markdown(skills_html, unsafe_allow_html=True)
                else:
                    st.warning("No matching skills found.")
            
            with col2:
                st.markdown("### 📚 Skills to Learn")
                st.caption("Required by job but not in your resume")
                if comparison['skills_you_are_missing']:
                    skills_html = ""
                    for skill in sorted(comparison['skills_you_are_missing']):
                        skills_html += f'<span class="skill-badge skill-missing">{skill.title()}</span>'
                    st.markdown(skills_html, unsafe_allow_html=True)
                else:
                    st.success("You have all required skills! 🎉")
            
            with col3:
                st.markdown("### 💼 All Your Skills")
                st.caption("All technical skills found in your resume")
                if 'all_resume_skills' in st.session_state and st.session_state['all_resume_skills']:
                    skills_html = ""
                    for skill in sorted(st.session_state['all_resume_skills']):
                        skills_html += f'<span class="skill-badge skill-all">{skill.title()}</span>'
                    st.markdown(skills_html, unsafe_allow_html=True)
                else:
                    st.info("Upload a resume to see your skills")
            
            # Recommendations
            if comparison['skills_you_are_missing']:
                st.markdown("---")
                st.markdown("### 💡 Recommendations")
                
                # Get top 3 priority skills
                priority_skills = ', '.join([s.title() for s in comparison['skills_you_are_missing'][:3]])
                
                st.markdown(f"""
                <div class="info-box">
                <strong>To improve your match for this role:</strong><br><br>
                
                🎯 <strong>Priority Skills:</strong> Focus on learning {priority_skills}<br>
                📚 <strong>Online Resources:</strong> Check out Coursera, Udemy, or LinkedIn Learning<br>
                💻 <strong>Build Projects:</strong> Create portfolio projects using these technologies<br>
                📝 <strong>Update Resume:</strong> Make sure your resume clearly lists your technical skills
                </div>
                """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()