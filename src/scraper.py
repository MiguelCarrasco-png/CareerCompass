"""
Web scraper for job postings from SHPE sponsor companies.
Week 1: Basic scraper for one company
"""

import requests
from bs4 import BeautifulSoup
import time
from typing import List, Dict

def scrape_google_jobs(max_jobs=10):
    """
    Scrapes job postings from Google Careers.
    This is a SIMPLIFIED example - real implementation will vary by site.
    
    Args:
        max_jobs: Maximum number of jobs to scrape
        
    Returns:
        List of dictionaries with job data
    """
    jobs = []
    
    # NOTE: This is a placeholder URL - you'll need to find the actual careers page
    # Example: "https://careers.google.com/jobs/results/"
    url = "https://careers.google.com/jobs/results/"
    
    try:
        # Make request with headers to avoid being blocked
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # TODO: Inspect the actual website and update these selectors
        # This is a TEMPLATE - you need to find the correct CSS selectors
        job_cards = soup.find_all('div', class_='job-card', limit=max_jobs)
        
        for card in job_cards:
            try:
                # Extract job details (UPDATE THESE SELECTORS)
                title = card.find('h3', class_='job-title')
                description = card.find('div', class_='job-description')
                link = card.find('a', class_='job-link')
                
                if title and description:
                    jobs.append({
                        'company': 'Google',
                        'title': title.text.strip(),
                        'description': description.text.strip(),
                        'url': link['href'] if link else 'N/A'
                    })
            except Exception as e:
                print(f"Error parsing job card: {e}")
                continue
                
        print(f"Successfully scraped {len(jobs)} jobs from Google")
        
    except Exception as e:
        print(f"Error scraping Google jobs: {e}")
    
    return jobs


def scrape_test_data():
    """
    Returns fake job data for testing when real scraping isn't ready.
    Use this while you're building the actual scraper!
    """
    return [
        {
            'company': 'Google',
            'title': 'Software Engineer Intern',
            'description': 'We are looking for a software engineer intern with experience in Python, Java, and React. Must have strong problem-solving skills and knowledge of data structures and algorithms. Experience with cloud platforms like GCP is a plus.',
            'url': 'https://careers.google.com/jobs/test1'
        },
        {
            'company': 'Google',
            'title': 'Data Scientist',
            'description': 'Seeking a data scientist with expertise in machine learning, Python, TensorFlow, and SQL. Should have experience with data visualization tools like Tableau and strong statistical analysis skills.',
            'url': 'https://careers.google.com/jobs/test2'
        },
        {
            'company': 'Lockheed Martin',
            'title': 'Mechanical Engineer',
            'description': 'Looking for mechanical engineers with CAD experience, particularly SolidWorks and AutoCAD. Knowledge of MATLAB, finite element analysis, and thermodynamics required. Security clearance preferred.',
            'url': 'https://lockheedmartin.com/jobs/test1'
        },
        {
            'company': 'Texas Instruments',
            'title': 'Electrical Engineer Intern',
            'description': 'Internship opportunity for electrical engineering students. Must know circuit design, VHDL, SPICE simulation, and PCB layout. Experience with oscilloscopes and signal analysis tools required.',
            'url': 'https://ti.com/jobs/test1'
        },
        {
            'company': 'Northrop Grumman',
            'title': 'Systems Engineer',
            'description': 'Systems engineer position requiring knowledge of systems integration, requirements analysis, and technical documentation. Programming skills in Python, C++, and experience with Agile methodology needed.',
            'url': 'https://northropgrumman.com/jobs/test1'
        }
    ]


def scrape_all_job_data(use_test_data=True):
    """
    Master function to scrape from all target companies.
    
    Args:
        use_test_data: If True, returns fake data. Set to False when scraper is ready.
        
    Returns:
        List of all job postings from all companies
    """
    if use_test_data:
        print("Using test data...")
        return scrape_test_data()
    
    all_jobs = []
    
    # Week 2: Add more companies here
    companies = [
        scrape_google_jobs,
        # scrape_lockheed_jobs,
        # scrape_ti_jobs,
    ]
    
    for scraper_func in companies:
        try:
            jobs = scraper_func()
            all_jobs.extend(jobs)
            time.sleep(2)  # Be polite - don't hammer servers
        except Exception as e:
            print(f"Error with {scraper_func.__name__}: {e}")
    
    return all_jobs


if __name__ == "__main__":
    # Test the scraper
    print("Testing scraper...")
    jobs = scrape_all_job_data(use_test_data=True)
    print(f"\nFound {len(jobs)} total jobs")
    print("\nFirst job:")
    print(jobs[0])