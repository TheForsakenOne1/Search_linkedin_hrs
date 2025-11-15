#!/usr/bin/env python3
"""
Comprehensive demo script for LinkedIn HR Scraper
Tests all major features and provides usage examples
"""
import os
import sys
from validation import (
    validate_environment,
    validate_credentials,
    validate_company_name,
    validate_scenario,
    ValidationError
)
import config


def print_banner():
    """Print demo banner"""
    print("""
╔══════════════════════════════════════════════════════════╗
║      LinkedIn HR Scraper - Comprehensive Demo          ║
║                                                          ║
║  This demo will guide you through all features          ║
╚══════════════════════════════════════════════════════════╝
""")


def check_environment():
    """Check environment setup"""
    print("\n" + "="*60)
    print("STEP 1: ENVIRONMENT CHECK")
    print("="*60)

    print("\nChecking environment configuration...")

    is_valid, errors = validate_environment()

    if is_valid:
        print("✓ Environment is properly configured!")
    else:
        print("✗ Environment has issues:")
        for error in errors:
            print(f"  - {error}")
        print("\nPlease fix these issues before continuing.")
        return False

    return True


def check_credentials():
    """Check LinkedIn credentials"""
    print("\n" + "="*60)
    print("STEP 2: CREDENTIALS CHECK")
    print("="*60)

    print("\nChecking LinkedIn credentials...")

    is_valid, error = validate_credentials()

    if is_valid:
        print(f"✓ LinkedIn credentials configured!")
        print(f"  Email: {config.LINKEDIN_EMAIL[:3]}***{config.LINKEDIN_EMAIL[-10:]}")
    else:
        print(f"✗ {error}")
        print("\nTo configure credentials:")
        print("  1. Copy .env.example to .env")
        print("  2. Edit .env and add your LinkedIn email/password")
        return False

    return True


def check_ai_setup():
    """Check AI configuration"""
    print("\n" + "="*60)
    print("STEP 3: AI SETUP CHECK (Optional)")
    print("="*60)

    if not config.USE_AI_MESSAGES:
        print("⚠ AI message generation is disabled")
        print("  To enable AI:")
        print("  1. Edit .env and set USE_AI_MESSAGES=True")
        print("  2. Add your OPENAI_API_KEY or ANTHROPIC_API_KEY")
        print("\n  AI generates higher quality, personalized messages.")
        print("  Template-based messages will be used instead.")
        return 'disabled'

    print(f"✓ AI message generation enabled!")
    print(f"  Provider: {config.AI_PROVIDER.upper()}")

    if config.AI_PROVIDER == 'openai':
        if not config.OPENAI_API_KEY or 'your' in config.OPENAI_API_KEY.lower():
            print("✗ OpenAI API key not configured")
            return 'error'
        print(f"  Model: {config.OPENAI_MODEL}")
        print(f"  API Key: {config.OPENAI_API_KEY[:10]}...{config.OPENAI_API_KEY[-4:]}")

    elif config.AI_PROVIDER == 'anthropic':
        if not config.ANTHROPIC_API_KEY or 'your' in config.ANTHROPIC_API_KEY.lower():
            print("✗ Anthropic API key not configured")
            return 'error'
        print(f"  Model: {config.ANTHROPIC_MODEL}")
        print(f"  API Key: {config.ANTHROPIC_API_KEY[:10]}...{config.ANTHROPIC_API_KEY[-4:]}")

    return 'enabled'


def demo_message_generation():
    """Demo message generation"""
    print("\n" + "="*60)
    print("DEMO: MESSAGE GENERATION")
    print("="*60)

    # Example profile
    profile = {
        'name': 'Sarah Johnson',
        'title': 'Senior Talent Acquisition Manager at Google',
        'location': 'San Francisco Bay Area',
        'profile_url': 'https://linkedin.com/in/sarahjohnson'
    }

    custom_data = {
        'your_role': 'Senior Software Engineer',
        'years': '7',
        'skills': 'Python, Kubernetes, React, Machine Learning',
        'industry': 'technology'
    }

    print(f"\nExample Profile:")
    print(f"  Name: {profile['name']}")
    print(f"  Title: {profile['title']}")
    print(f"  Location: {profile['location']}")

    print(f"\nYour Information:")
    print(f"  Role: {custom_data['your_role']}")
    print(f"  Experience: {custom_data['years']} years")
    print(f"  Skills: {custom_data['skills']}")

    # Try AI generation if enabled
    ai_status = check_ai_setup()

    if ai_status == 'enabled':
        print("\n--- AI-Generated Message ---")
        try:
            from ai_message_generator import AIMessageGenerator

            generator = AIMessageGenerator()
            message = generator.generate_message(
                profile,
                scenario='job_seeker',
                custom_data=custom_data,
                message_type='connection'
            )

            print(f"\nTo: {message['recipient_name']}")
            print(f"Characters: {message['char_count']}/300")
            print(f"\n{message['message']}")
            print(f"\n✓ AI message generated successfully!")
            print(f"  Provider: {message['ai_provider'].upper()}")
            print(f"  Model: {message['ai_model']}")

        except Exception as e:
            print(f"\n✗ AI generation failed: {str(e)}")
            print("  Falling back to template-based generation...")
            ai_status = 'disabled'

    if ai_status != 'enabled':
        print("\n--- Template-Based Message ---")
        from message_generator import MessageGenerator

        generator = MessageGenerator(use_ai=False)
        message = generator.generate_message(
            profile,
            scenario='job_seeker',
            custom_data=custom_data
        )

        print(f"\nTo: {message['recipient_name']}")
        print(f"Characters: {message['char_count']}")
        print(f"\n{message['message']}")
        print(f"\n✓ Template message generated successfully!")


def demo_validation():
    """Demo input validation"""
    print("\n" + "="*60)
    print("DEMO: INPUT VALIDATION")
    print("="*60)

    print("\nTesting company name validation:")

    test_cases = [
        ("Google", True, "Valid company name"),
        ("", False, "Empty company name"),
        ("A", False, "Too short"),
        ("Microsoft Corporation", True, "Valid with suffix"),
    ]

    for company, should_pass, description in test_cases:
        is_valid, error = validate_company_name(company)
        status = "✓" if is_valid else "✗"
        print(f"  {status} '{company}': {description}")
        if error:
            print(f"      Error: {error}")

    print("\nTesting scenario validation:")
    for scenario in ['job_seeker', 'networking', 'invalid_scenario']:
        is_valid, error = validate_scenario(scenario)
        status = "✓" if is_valid else "✗"
        print(f"  {status} '{scenario}'")
        if error:
            print(f"      Error: {error}")


def demo_export():
    """Demo export functionality"""
    print("\n" + "="*60)
    print("DEMO: DATA EXPORT")
    print("="*60)

    print("\nSupported export formats:")
    print("  • CSV - Best for spreadsheet analysis")
    print("  • JSON - Best for programming/API integration")
    print("  • Excel - Best for sharing with non-technical users")

    # Create sample data
    sample_profiles = [
        {
            'name': 'John Doe',
            'title': 'HR Manager at Microsoft',
            'location': 'Seattle, WA',
            'profile_url': 'https://linkedin.com/in/johndoe'
        },
        {
            'name': 'Jane Smith',
            'title': 'Talent Acquisition Partner at Amazon',
            'location': 'New York, NY',
            'profile_url': 'https://linkedin.com/in/janesmith'
        }
    ]

    print(f"\nSample data: {len(sample_profiles)} profiles")

    try:
        from data_exporter import DataExporter

        exporter = DataExporter()

        print("\nExporting to different formats...")

        # Export to CSV
        csv_file = exporter.export_to_csv(sample_profiles, "DemoCompany")
        if csv_file:
            print(f"  ✓ CSV: {csv_file}")

        # Export to JSON
        json_file = exporter.export_to_json(sample_profiles, "DemoCompany")
        if json_file:
            print(f"  ✓ JSON: {json_file}")

        # Export to Excel
        excel_file = exporter.export_to_excel(sample_profiles, "DemoCompany")
        if excel_file:
            print(f"  ✓ Excel: {excel_file}")

        print("\n✓ Export demo completed successfully!")

    except Exception as e:
        print(f"\n✗ Export demo failed: {str(e)}")


def show_usage_examples():
    """Show usage examples"""
    print("\n" + "="*60)
    print("USAGE EXAMPLES")
    print("="*60)

    examples = [
        {
            'title': 'Basic Scraping',
            'description': 'Scrape HR contacts from a company',
            'command': 'python main.py --company "Google" --max-results 30'
        },
        {
            'title': 'Complete Workflow (Export Only)',
            'description': 'Scrape, generate messages, and export for review',
            'command': '''python complete_workflow.py \\
  --company "Microsoft" \\
  --scenario job_seeker \\
  --role "Software Engineer" \\
  --years "5" \\
  --skills "Python, React, AWS" \\
  --export-only'''
        },
        {
            'title': 'AI-Powered Campaign',
            'description': 'Run autonomous AI agent (requires API key)',
            'command': '''python ai_agent.py \\
  --company "Amazon" \\
  --scenario job_seeker \\
  --role "Data Scientist" \\
  --years "4" \\
  --skills "Python, ML, TensorFlow"'''
        },
        {
            'title': 'Multi-Company Campaign',
            'description': 'Target multiple companies at once',
            'command': 'python ai_agent.py --companies "Google,Microsoft,Amazon,Meta,Apple"'
        },
        {
            'title': 'Test Message Generation',
            'description': 'Test message generator only',
            'command': 'python message_generator.py'
        },
        {
            'title': 'Start Message Service API',
            'description': 'Run Flask API for n8n integration',
            'command': 'python message_service.py'
        }
    ]

    for idx, example in enumerate(examples, 1):
        print(f"\n{idx}. {example['title']}")
        print(f"   {example['description']}")
        print(f"\n   {example['command']}\n")


def show_next_steps():
    """Show next steps"""
    print("\n" + "="*60)
    print("NEXT STEPS")
    print("="*60)

    print("""
Ready to use the LinkedIn HR Scraper! Here's what to do next:

1. Configure Credentials (if not done):
   - Copy .env.example to .env
   - Add your LinkedIn email and password

2. Optional: Enable AI Messages
   - Get OpenAI or Anthropic API key
   - Set USE_AI_MESSAGES=True in .env
   - Add your API key

3. Run Your First Search:
   - Basic: python main.py --company "Google"
   - Full workflow: python complete_workflow.py --company "Google" --export-only

4. Review Generated Files:
   - Check output/ directory for results
   - CSV, JSON, or Excel formats available

5. For Automation:
   - Set up n8n workflows
   - Use message service API
   - See N8N_INTEGRATION_GUIDE.md

6. Documentation:
   - README.md - Main documentation
   - QUICKSTART.md - 5-minute quick start
   - AI_AGENT_GUIDE.md - AI features guide
   - N8N_INTEGRATION_GUIDE.md - n8n setup

Need Help?
   - Run: python utils.py --check
   - Check documentation
   - Review example_usage.py

Happy networking! 🚀
""")


def interactive_demo():
    """Run interactive demo"""
    print_banner()

    # Check environment
    if not check_environment():
        print("\n⚠ Please fix environment issues before continuing.")
        return

    # Check credentials
    creds_ok = check_credentials()

    # Check AI setup
    ai_status = check_ai_setup()

    # Run demos
    demo_validation()
    demo_message_generation()
    demo_export()

    # Show examples
    show_usage_examples()

    # Show next steps
    show_next_steps()


def main():
    """Main entry point"""
    if len(sys.argv) > 1 and sys.argv[1] == '--quick':
        # Quick check mode
        print("Running quick environment check...")
        env_ok = check_environment()
        creds_ok = check_credentials()
        ai_status = check_ai_setup()

        if env_ok and creds_ok:
            print("\n✓ All systems ready!")
        else:
            print("\n⚠ Some issues found. Run 'python demo.py' for full details.")

    else:
        # Full interactive demo
        interactive_demo()


if __name__ == "__main__":
    main()
