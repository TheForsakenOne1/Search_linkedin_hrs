"""
Utility functions for LinkedIn scraper
"""
import os
import sys


def check_environment():
    """Check if the environment is properly configured"""
    print("Checking environment configuration...\n")

    issues = []

    # Check Python version
    python_version = sys.version_info
    if python_version < (3, 8):
        issues.append(f"⚠ Python version {python_version.major}.{python_version.minor} is too old. Please use Python 3.8+")
    else:
        print(f"✓ Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")

    # Check if .env exists
    if os.path.exists('.env'):
        print("✓ .env file exists")

        # Check if credentials are set
        from dotenv import load_dotenv
        load_dotenv()

        email = os.getenv('LINKEDIN_EMAIL', '')
        password = os.getenv('LINKEDIN_PASSWORD', '')

        if not email or email == 'your_email@example.com':
            issues.append("⚠ LINKEDIN_EMAIL not configured in .env")
        else:
            print(f"✓ LinkedIn email configured: {email[:3]}***{email[-10:]}")

        if not password or password == 'your_password':
            issues.append("⚠ LINKEDIN_PASSWORD not configured in .env")
        else:
            print("✓ LinkedIn password configured")

    else:
        issues.append("⚠ .env file not found. Please copy .env.example to .env and configure it")

    # Check if output directory can be created
    try:
        os.makedirs('./output', exist_ok=True)
        print("✓ Output directory is accessible")
    except Exception as e:
        issues.append(f"⚠ Cannot create output directory: {str(e)}")

    # Check required packages
    required_packages = [
        'selenium',
        'beautifulsoup4',
        'pandas',
        'webdriver_manager',
        'dotenv'
    ]

    print("\nChecking required packages:")
    for package in required_packages:
        try:
            __import__(package.replace('-', '_').replace('python_', ''))
            print(f"  ✓ {package}")
        except ImportError:
            issues.append(f"⚠ Package '{package}' not installed")
            print(f"  ✗ {package}")

    # Print summary
    print("\n" + "="*60)
    if issues:
        print("❌ Configuration Issues Found:\n")
        for issue in issues:
            print(f"  {issue}")
        print("\nPlease fix these issues before running the scraper.")
        print("See README.md or QUICKSTART.md for setup instructions.")
        return False
    else:
        print("✅ All checks passed! You're ready to run the scraper.")
        return True


def validate_company_name(company_name):
    """Validate company name input"""
    if not company_name or not company_name.strip():
        return False, "Company name cannot be empty"

    if len(company_name.strip()) < 2:
        return False, "Company name is too short"

    return True, "Valid company name"


def print_hr_keywords():
    """Print all configured HR keywords"""
    import config

    print("Configured HR Keywords:")
    print("="*60)
    for idx, keyword in enumerate(config.HR_KEYWORDS, 1):
        print(f"{idx:2d}. {keyword}")
    print(f"\nTotal keywords: {len(config.HR_KEYWORDS)}")


if __name__ == "__main__":
    """Run environment check when executed directly"""
    import argparse

    parser = argparse.ArgumentParser(description='LinkedIn Scraper Utilities')
    parser.add_argument('--check', action='store_true', help='Check environment configuration')
    parser.add_argument('--keywords', action='store_true', help='Print HR keywords')

    args = parser.parse_args()

    if args.keywords:
        print_hr_keywords()
    elif args.check:
        check_environment()
    else:
        # Default: run environment check
        check_environment()
