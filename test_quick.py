# test_quick.py
print("Starting tests...")

from src.scraper import scrape_all_job_data
from src.nlp_processor import extract_skills, get_skill_counts

print("Imports successful!")

jobs = scrape_all_job_data(use_test_data=True)
print(f"Found {len(jobs)} jobs")
print(f"First job: {jobs[0]['title']}")

skills = extract_skills(jobs[0]['description'])
print(f"Found {len(skills)} skills: {list(skills.keys())}")