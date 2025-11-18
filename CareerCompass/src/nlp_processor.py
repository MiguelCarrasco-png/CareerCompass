import re
from collections import Counter
from typing import List, Dict, Set
import PyPDF2
import io

# Comprehensive list of technical skills to search for
# Week 1: Start with this hardcoded list
TECHNICAL_SKILLS = {
    # Programming Languages
    'python', 'java', 'javascript', 'c++', 'c#', 'r', 'matlab', 'sql',
    'typescript', 'go', 'rust', 'kotlin', 'swift', 'scala', 'ruby',
    
    # Web Technologies
    'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask',
    'html', 'css', 'bootstrap', 'tailwind', 'next.js',
    
    # Databases
    'mysql', 'postgresql', 'mongodb', 'redis', 'cassandra', 'dynamodb',
    
    # Cloud & DevOps
    'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'terraform',
    'ci/cd', 'git', 'github', 'gitlab',
    
    # Data Science & ML
    'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy', 'keras',
    'machine learning', 'deep learning', 'nlp', 'computer vision',
    'data analysis', 'statistics', 'tableau', 'power bi',
    
    # Engineering Tools
    'autocad', 'solidworks', 'catia', 'ansys', 'matlab', 'simulink',
    'labview', 'pcb design', 'vhdl', 'verilog', 'spice',
    
    # Methodologies & Concepts
    'agile', 'scrum', 'rest api', 'microservices', 'oop', 'tdd',
    'data structures', 'algorithms', 'system design',
    
    # Other
    'linux', 'excel', 'jira', 'confluence', 'slack'
}


def extract_skills(text: str) -> Counter:
    """
    Extract technical skills from text using keyword matching.
    
    Args:
        text: Job description or resume text
        
    Returns:
        Counter object with skill frequencies
    """
    if not text:
        return Counter()
    
    # Convert to lowercase for matching
    text_lower = text.lower()
    
    # Find all skills present in the text
    found_skills = Counter()
    
    for skill in TECHNICAL_SKILLS:
        # Use word boundaries to avoid partial matches
        # e.g., "java" should not match "javascript"
        pattern = r'\b' + re.escape(skill) + r'\b'
        matches = re.findall(pattern, text_lower)
        if matches:
            found_skills[skill] = len(matches)
    
    return found_skills


def get_skill_counts(job_list: List[Dict]) -> Dict[str, int]:
    """
    Process a list of jobs and count skill occurrences across all jobs.
    
    Args:
        job_list: List of job dictionaries with 'description' key
        
    Returns:
        Dictionary mapping skills to their total count
    """
    total_skills = Counter()
    
    for job in job_list:
        description = job.get('description', '')
        job_skills = extract_skills(description)
        total_skills.update(job_skills)
    
    # Convert Counter to regular dict and sort by count
    skill_dict = dict(total_skills.most_common())
    
    print(f"Processed {len(job_list)} jobs")
    print(f"Found {len(skill_dict)} unique skills")
    
    return skill_dict


def read_pdf_text(uploaded_file) -> str:
    """
    Extract text from an uploaded PDF file.
    Week 3 function - for resume parsing.
    
    Args:
        uploaded_file: Streamlit uploaded file object or file path
        
    Returns:
        Extracted text as string
    """
    try:
        # Handle Streamlit uploaded file
        if hasattr(uploaded_file, 'read'):
            pdf_bytes = uploaded_file.read()
            pdf_file = io.BytesIO(pdf_bytes)
        else:
            # Handle file path
            pdf_file = open(uploaded_file, 'rb')
        
        # Create PDF reader object
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        # Extract text from all pages
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        
        # Close file if we opened it
        if not hasattr(uploaded_file, 'read'):
            pdf_file.close()
            
        return text.strip()
        
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""


def compare_skills(resume_text: str, job_text: str) -> Dict:
    """
    Compare skills in a resume vs. a job description.
    Week 3 function - for resume matching feature.
    
    Args:
        resume_text: Text extracted from resume
        job_text: Job description text
        
    Returns:
        Dictionary with match score and skill lists
    """
    # Extract skills from both
    resume_skills = set(extract_skills(resume_text).keys())
    job_skills = set(extract_skills(job_text).keys())
    
    # Calculate matches
    skills_you_have = resume_skills & job_skills  # Intersection
    skills_you_are_missing = job_skills - resume_skills  # Difference
    
    # Calculate match score
    if len(job_skills) == 0:
        match_score = 0
    else:
        match_score = (len(skills_you_have) / len(job_skills)) * 100
    
    return {
        'score': round(match_score, 1),
        'skills_you_have': sorted(list(skills_you_have)),
        'skills_you_are_missing': sorted(list(skills_you_are_missing)),
        'total_job_skills': len(job_skills),
        'total_resume_skills': len(resume_skills)
    }


if __name__ == "__main__":
    # Test the NLP processor
    test_job = """
    We are seeking a Software Engineer with strong Python and Java skills.
    Experience with React, Docker, and AWS is required.
    Knowledge of machine learning and TensorFlow is a plus.
    """
    
    print("Testing skill extraction...")
    skills = extract_skills(test_job)
    print(f"\nFound skills: {dict(skills)}")
    
    # Test comparison
    test_resume = """
    Experienced software developer proficient in Python, Java, and JavaScript.
    Built web applications using React and Node.js.
    Familiar with Git and Agile methodologies.
    """
    
    print("\n\nTesting skill comparison...")
    comparison = compare_skills(test_resume, test_job)
    print(f"Match Score: {comparison['score']}%")
    print(f"Skills you have: {comparison['skills_you_have']}")
    print(f"Skills you're missing: {comparison['skills_you_are_missing']}")