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

# AI Message Generation settings
USE_AI_MESSAGES = os.getenv('USE_AI_MESSAGES', 'False').lower() == 'true'
AI_PROVIDER = os.getenv('AI_PROVIDER', 'openai')  # openai or anthropic

# OpenAI settings
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4')
OPENAI_MAX_TOKENS = int(os.getenv('OPENAI_MAX_TOKENS', '500'))
OPENAI_TEMPERATURE = float(os.getenv('OPENAI_TEMPERATURE', '0.7'))

# Anthropic settings
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '')
ANTHROPIC_MODEL = os.getenv('ANTHROPIC_MODEL', 'claude-3-5-sonnet-20241022')
ANTHROPIC_MAX_TOKENS = int(os.getenv('ANTHROPIC_MAX_TOKENS', '1000'))

# Message scenarios
MESSAGE_SCENARIOS = [
    'job_seeker',
    'networking',
    'recruiter_outreach',
    'informational_interview'
]

# Validation settings
MAX_COMPANY_NAME_LENGTH = 100
MIN_COMPANY_NAME_LENGTH = 2
MAX_RESULTS_LIMIT = 500
MIN_RESULTS_LIMIT = 1
