"""
Input validation utilities for LinkedIn scraper
Ensures data quality and prevents errors
"""
import re
import os
from urllib.parse import urlparse


class ValidationError(Exception):
    """Custom validation error"""
    pass


def validate_company_name(company_name):
    """
    Validate company name input

    Args:
        company_name (str): Company name to validate

    Returns:
        tuple: (is_valid, error_message)
    """
    if not company_name:
        return False, "Company name cannot be empty"

    if not isinstance(company_name, str):
        return False, "Company name must be a string"

    company_name = company_name.strip()

    if len(company_name) < 2:
        return False, "Company name is too short (minimum 2 characters)"

    if len(company_name) > 100:
        return False, "Company name is too long (maximum 100 characters)"

    # Check for valid characters (allow letters, numbers, spaces, hyphens, ampersands)
    if not re.match(r'^[a-zA-Z0-9\s\-&.,()]+$', company_name):
        return False, "Company name contains invalid characters"

    return True, None


def validate_email(email):
    """
    Validate email address

    Args:
        email (str): Email to validate

    Returns:
        tuple: (is_valid, error_message)
    """
    if not email:
        return False, "Email cannot be empty"

    if not isinstance(email, str):
        return False, "Email must be a string"

    # Basic email regex
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False, "Invalid email format"

    return True, None


def validate_linkedin_url(url):
    """
    Validate LinkedIn profile URL

    Args:
        url (str): LinkedIn URL to validate

    Returns:
        tuple: (is_valid, error_message)
    """
    if not url:
        return False, "URL cannot be empty"

    if not isinstance(url, str):
        return False, "URL must be a string"

    try:
        parsed = urlparse(url)

        # Check domain
        if 'linkedin.com' not in parsed.netloc:
            return False, "URL must be from linkedin.com"

        # Check scheme
        if parsed.scheme not in ['http', 'https']:
            return False, "URL must use http or https"

        return True, None

    except Exception as e:
        return False, f"Invalid URL format: {str(e)}"


def validate_scenario(scenario):
    """
    Validate message scenario

    Args:
        scenario (str): Scenario to validate

    Returns:
        tuple: (is_valid, error_message)
    """
    valid_scenarios = ['job_seeker', 'networking', 'recruiter_outreach', 'informational_interview']

    if not scenario:
        return False, "Scenario cannot be empty"

    if scenario not in valid_scenarios:
        return False, f"Invalid scenario. Must be one of: {', '.join(valid_scenarios)}"

    return True, None


def validate_max_results(max_results):
    """
    Validate max results parameter

    Args:
        max_results (int): Maximum results to validate

    Returns:
        tuple: (is_valid, error_message)
    """
    if not isinstance(max_results, int):
        try:
            max_results = int(max_results)
        except (ValueError, TypeError):
            return False, "Max results must be a number"

    if max_results < 1:
        return False, "Max results must be at least 1"

    if max_results > 500:
        return False, "Max results cannot exceed 500 (LinkedIn and performance limitations)"

    return True, None


def validate_api_key(api_key, provider='openai'):
    """
    Validate API key format

    Args:
        api_key (str): API key to validate
        provider (str): API provider (openai, anthropic)

    Returns:
        tuple: (is_valid, error_message)
    """
    if not api_key:
        return False, "API key cannot be empty"

    if not isinstance(api_key, str):
        return False, "API key must be a string"

    api_key = api_key.strip()

    if provider == 'openai':
        if not api_key.startswith('sk-'):
            return False, "OpenAI API key must start with 'sk-'"
        if len(api_key) < 20:
            return False, "OpenAI API key is too short"

    elif provider == 'anthropic':
        if not api_key.startswith('sk-ant-'):
            return False, "Anthropic API key must start with 'sk-ant-'"
        if len(api_key) < 20:
            return False, "Anthropic API key is too short"

    # Check if it's a placeholder
    if 'your' in api_key.lower() or 'example' in api_key.lower():
        return False, "API key appears to be a placeholder, not a real key"

    return True, None


def validate_file_path(file_path, must_exist=False):
    """
    Validate file path

    Args:
        file_path (str): File path to validate
        must_exist (bool): Whether file must already exist

    Returns:
        tuple: (is_valid, error_message)
    """
    if not file_path:
        return False, "File path cannot be empty"

    if not isinstance(file_path, str):
        return False, "File path must be a string"

    # Check if path is absolute
    if not os.path.isabs(file_path):
        return False, "File path must be absolute"

    if must_exist and not os.path.exists(file_path):
        return False, f"File does not exist: {file_path}"

    # Check parent directory exists (for new files)
    if not must_exist:
        parent_dir = os.path.dirname(file_path)
        if parent_dir and not os.path.exists(parent_dir):
            return False, f"Parent directory does not exist: {parent_dir}"

    return True, None


def validate_custom_data(custom_data):
    """
    Validate custom personalization data

    Args:
        custom_data (dict): Custom data to validate

    Returns:
        tuple: (is_valid, error_message)
    """
    if custom_data is None:
        return True, None  # Optional parameter

    if not isinstance(custom_data, dict):
        return False, "Custom data must be a dictionary"

    # Validate common fields if present
    if 'years' in custom_data:
        years = custom_data['years']
        try:
            years_int = int(years)
            if years_int < 0 or years_int > 50:
                return False, "Years of experience must be between 0 and 50"
        except (ValueError, TypeError):
            return False, "Years must be a number"

    if 'skills' in custom_data:
        skills = custom_data['skills']
        if not isinstance(skills, str):
            return False, "Skills must be a string"
        if len(skills) > 200:
            return False, "Skills description is too long (max 200 characters)"

    return True, None


def validate_profile(profile):
    """
    Validate profile data structure

    Args:
        profile (dict): Profile data to validate

    Returns:
        tuple: (is_valid, error_message)
    """
    if not isinstance(profile, dict):
        return False, "Profile must be a dictionary"

    required_fields = ['name', 'title']

    for field in required_fields:
        if field not in profile:
            return False, f"Profile missing required field: {field}"

        if not profile[field]:
            return False, f"Profile field '{field}' cannot be empty"

    # Validate name
    name = profile.get('name', '')
    if len(name) < 2:
        return False, "Profile name is too short"
    if name.lower() == 'linkedin member':
        return False, "Invalid profile name (LinkedIn Member)"

    # Validate URL if present
    if 'profile_url' in profile and profile['profile_url']:
        is_valid, error = validate_linkedin_url(profile['profile_url'])
        if not is_valid:
            return False, f"Invalid profile URL: {error}"

    return True, None


def sanitize_filename(filename):
    """
    Sanitize filename to be safe for file system

    Args:
        filename (str): Filename to sanitize

    Returns:
        str: Sanitized filename
    """
    # Remove or replace invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)

    # Remove leading/trailing spaces and dots
    filename = filename.strip(' .')

    # Limit length
    if len(filename) > 200:
        filename = filename[:200]

    return filename


def validate_environment():
    """
    Validate environment setup

    Returns:
        tuple: (is_valid, list_of_errors)
    """
    errors = []

    # Check Python version
    import sys
    if sys.version_info < (3, 8):
        errors.append(f"Python 3.8+ required, found {sys.version_info.major}.{sys.version_info.minor}")

    # Check required packages
    required_packages = [
        'selenium',
        'dotenv',
        'pandas',
        'beautifulsoup4',
        'flask'
    ]

    for package in required_packages:
        try:
            __import__(package.replace('-', '_').replace('python_', ''))
        except ImportError:
            errors.append(f"Required package not installed: {package}")

    # Check .env file exists
    if not os.path.exists('.env'):
        errors.append(".env file not found (copy from .env.example)")

    # Check output directory
    try:
        os.makedirs('./output', exist_ok=True)
    except Exception as e:
        errors.append(f"Cannot create output directory: {str(e)}")

    is_valid = len(errors) == 0
    return is_valid, errors


def validate_credentials():
    """
    Validate LinkedIn credentials are configured

    Returns:
        tuple: (is_valid, error_message)
    """
    import config

    if not config.LINKEDIN_EMAIL or config.LINKEDIN_EMAIL == 'your_email@example.com':
        return False, "LinkedIn email not configured in .env"

    if not config.LINKEDIN_PASSWORD or config.LINKEDIN_PASSWORD == 'your_password':
        return False, "LinkedIn password not configured in .env"

    # Validate email format
    is_valid, error = validate_email(config.LINKEDIN_EMAIL)
    if not is_valid:
        return False, f"LinkedIn email invalid: {error}"

    return True, None


# Convenience functions for raising exceptions
def validate_or_raise(validator_func, *args, **kwargs):
    """
    Run validator and raise ValidationError if invalid

    Args:
        validator_func: Validation function to run
        *args, **kwargs: Arguments to pass to validator

    Raises:
        ValidationError: If validation fails
    """
    is_valid, error = validator_func(*args, **kwargs)
    if not is_valid:
        raise ValidationError(error)
    return True


if __name__ == "__main__":
    """Run validation tests"""
    print("Running validation tests...\n")

    # Test company name validation
    test_cases = [
        ("Google", True),
        ("Microsoft Inc.", True),
        ("A", False),
        ("", False),
        ("Company123", True),
        ("@#$%", False),
    ]

    print("Company name validation:")
    for company, should_be_valid in test_cases:
        is_valid, error = validate_company_name(company)
        status = "✓" if is_valid == should_be_valid else "✗"
        print(f"  {status} '{company}': {is_valid} {'- ' + error if error else ''}")

    # Test email validation
    print("\nEmail validation:")
    emails = [
        ("test@example.com", True),
        ("invalid.email", False),
        ("user@domain.co.uk", True),
        ("", False),
    ]

    for email, should_be_valid in emails:
        is_valid, error = validate_email(email)
        status = "✓" if is_valid == should_be_valid else "✗"
        print(f"  {status} '{email}': {is_valid} {'- ' + error if error else ''}")

    # Test environment
    print("\nEnvironment validation:")
    is_valid, errors = validate_environment()
    if is_valid:
        print("  ✓ Environment is properly configured")
    else:
        print("  ✗ Environment has issues:")
        for error in errors:
            print(f"    - {error}")
