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
            
            ### Companies
            - **Google**
            - **Lockheed Martin**
            - **Texas Instruments**
            - **Northrop Grumman**
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
        
        # input for resume upload
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
           
        # Match button
            st.markdown("---")
        
            if st.button("🎯 Analyze Resume Against All Jobs", type="primary", use_container_width=True):
                with st.spinner("🔄 Analyzing your resume against all job postings..."):
                    # Get all jobs
                    jobs = scrape_all_job_data(use_test_data=True)
                    
                    # Calculate match for each job
                    job_matches = []
                    for job in jobs:
                        comparison = compare_skills(resume_text, job['description'])
                        job_matches.append({
                            'company': job['company'],
                            'title': job['title'],
                            'description': job['description'],
                            'score': comparison['score'],
                            'skills_you_have': comparison['skills_you_have'],
                            'skills_you_are_missing': comparison['skills_you_are_missing'],
                            'total_job_skills': comparison['total_job_skills'],
                            'total_resume_skills': comparison['total_resume_skills']
                        })
                    
                    # Sort by score (highest first)
                    job_matches.sort(key=lambda x: x['score'], reverse=True)
                    
                    st.session_state['job_matches'] = job_matches
                
                st.success(f"✅ Analyzed {len(job_matches)} jobs!")
        
        # Display ranked results
        if 'job_matches' in st.session_state:
            job_matches = st.session_state['job_matches']
            
            st.markdown("---")
            st.markdown("## 📊 Your Best Job Matches (Ranked)")
            
            # Overall statistics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Jobs Analyzed", len(job_matches))
            with col2:
                avg_score = sum(j['score'] for j in job_matches) / len(job_matches)
                st.metric("Average Match Score", f"{avg_score:.1f}%")
            with col3:
                best_match = job_matches[0]
                st.metric("Best Match Score", f"{best_match['score']}%")
            
            st.markdown("---")
            
            # Display each job match as an expandable card
            for idx, match in enumerate(job_matches, 1):
                # Determine color based on score
                if match['score'] >= 70:
                    score_emoji = "🟢"
                elif match['score'] >= 50:
                    score_emoji = "🟡"
                else:
                    score_emoji = "🔴"
                
                # Create expander for each job
                with st.expander(
                    f"**#{idx}** {score_emoji} **{match['company']} - {match['title']}** (Match: {match['score']}%)",
                    expanded=(idx == 1)  # Auto-expand the top match
                ):
                    # Job details header
                    st.markdown(f"### {match['company']}")
                    st.markdown(f"**Position:** {match['title']}")
                    st.markdown(f"**Match Score:** {match['score']}%")
                    
                    # Match interpretation
                    if match['score'] >= 70:
                        st.success("🎉 Excellent match! You have most of the required skills.")
                    elif match['score'] >= 50:
                        st.info("👍 Good match! Consider learning a few more skills to strengthen your application.")
                    else:
                        st.warning("💪 Room for improvement. Focus on building the missing skills below.")
                    
                    # Skills breakdown
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric(
                            "Skills You Have",
                            len(match['skills_you_have']),
                            f"of {match['total_job_skills']}"
                        )
                    
                    with col2:
                        st.metric(
                            "Skills to Learn",
                            len(match['skills_you_are_missing'])
                        )
                    
                    with col3:
                        st.metric(
                            "Your Total Skills",
                            match['total_resume_skills']
                        )
                    
                    # Detailed skills lists
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("#### ✅ Skills You Have")
                        if match['skills_you_have']:
                            for skill in sorted(match['skills_you_have']):
                                st.markdown(f"- **{skill.title()}**")
                        else:
                            st.write("No matching skills found.")
                    
                    with col2:
                        st.markdown("#### 📚 Skills to Learn")
                        if match['skills_you_are_missing']:
                            for skill in sorted(match['skills_you_are_missing']):
                                st.markdown(f"- {skill.title()}")
                        else:
                            st.write("You have all required skills! 🎉")
                    
                    # Job description
                    st.markdown("---")
                    st.markdown("#### 📋 Full Job Description")
                    st.text_area(
                        "Description",
                        match['description'],
                        height=100,
                        key=f"job_desc_{idx}",
                        label_visibility="collapsed"
                    )
                    
                    # Recommendations
                    if match['skills_you_are_missing']:
                        st.markdown("---")
                        st.markdown("#### 💡 Next Steps")
                        top_skills = match['skills_you_are_missing'][:3]
                        st.markdown(f"""
                        To improve your match for this role:
                        
                        1. **Priority Skills**: Focus on {', '.join(top_skills)}
                        2. **Learn**: Use Coursera, Udemy, or LinkedIn Learning
                        3. **Build**: Create projects showcasing these technologies
                        4. **Update**: Add new skills to your resume
                        """)
        elif not uploaded_file:
            # Show helpful message when no resume uploaded
            st.info("👆 Upload your resume above to get started!")
            
            st.markdown("### How It Works")
            st.markdown("""
            1. **Upload** your resume (PDF or TXT format)
            2. **Click** the analyze button
            3. **View** all jobs ranked by how well you match
            4. **Learn** which skills to develop for each opportunity
            
            Your resume will be compared against all SHPE sponsor company job postings,
            and you'll see exactly where you're the strongest candidate!
            """)

if __name__ == "__main__":
    main()