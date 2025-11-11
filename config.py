"""
Configuration settings for LinkedIn scraper
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# LinkedIn credentials
LINKEDIN_EMAIL = os.getenv('LINKEDIN_EMAIL', '')
LINKEDIN_PASSWORD = os.getenv('LINKEDIN_PASSWORD', '')

# Scraping settings
HEADLESS_MODE = os.getenv('HEADLESS_MODE', 'False').lower() == 'true'
IMPLICIT_WAIT = int(os.getenv('IMPLICIT_WAIT', '10'))
PAGE_LOAD_TIMEOUT = int(os.getenv('PAGE_LOAD_TIMEOUT', '30'))

# Export settings
EXPORT_FORMAT = os.getenv('EXPORT_FORMAT', 'csv')
OUTPUT_DIRECTORY = os.getenv('OUTPUT_DIRECTORY', './output')

# HR-related job titles and keywords
HR_KEYWORDS = [
    'Human Resources',
    'HR Manager',
    'HR Director',
    'HR Business Partner',
    'Talent Acquisition',
    'Recruiter',
    'Recruitment',
    'Hiring Manager',
    'People Operations',
    'People Partner',
    'Talent Partner',
    'Head of People',
    'Chief People Officer',
    'HR Specialist',
    'HR Generalist',
    'Staffing',
    'Employee Relations',
    'Talent Management',
    'VP of People',
    'Director of Talent'
]

# LinkedIn URLs
LINKEDIN_LOGIN_URL = 'https://www.linkedin.com/login'
LINKEDIN_PEOPLE_SEARCH_URL = 'https://www.linkedin.com/search/results/people/'

# Rate limiting (seconds)
MIN_SCROLL_DELAY = 2
MAX_SCROLL_DELAY = 4
MIN_PAGE_DELAY = 3
MAX_PAGE_DELAY = 6
