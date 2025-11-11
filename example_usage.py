#!/usr/bin/env python3
"""
Example usage of LinkedIn HR Scraper
This script demonstrates various ways to use the scraper programmatically
"""

from linkedin_scraper import LinkedInScraper
from data_exporter import DataExporter
import config


def example_basic_search():
    """Example: Basic search for HR personnel"""
    print("Example 1: Basic Search\n" + "="*60)

    scraper = None
    try:
        # Initialize scraper with credentials from config
        scraper = LinkedInScraper()

        # Setup browser
        scraper.setup_driver()

        # Login to LinkedIn
        if not scraper.login():
            print("Failed to login")
            return

        # Search for HR at Google
        company = "Google"
        results = scraper.search_hr_personnel(company, max_results=20)

        # Print results
        print(f"\nFound {len(results)} HR personnel at {company}")
        for profile in results[:5]:  # Show first 5
            print(f"- {profile['name']}: {profile['title']}")

        # Export to CSV
        exporter = DataExporter()
        exporter.export_to_csv(results, company)

    finally:
        if scraper:
            scraper.close()


def example_multiple_companies():
    """Example: Search multiple companies"""
    print("\n\nExample 2: Multiple Companies\n" + "="*60)

    companies = ["Microsoft", "Amazon", "Apple"]
    scraper = None

    try:
        scraper = LinkedInScraper()
        scraper.setup_driver()

        if not scraper.login():
            print("Failed to login")
            return

        exporter = DataExporter()

        for company in companies:
            print(f"\nSearching {company}...")
            results = scraper.search_hr_personnel(company, max_results=10)
            print(f"  Found {len(results)} profiles")

            # Export each company to separate file
            exporter.export_to_csv(results, company)

    finally:
        if scraper:
            scraper.close()


def example_custom_export():
    """Example: Custom export to multiple formats"""
    print("\n\nExample 3: Multi-Format Export\n" + "="*60)

    scraper = None
    try:
        scraper = LinkedInScraper()
        scraper.setup_driver()

        if not scraper.login():
            print("Failed to login")
            return

        company = "Netflix"
        results = scraper.search_hr_personnel(company, max_results=15)

        # Export to all formats
        exporter = DataExporter()
        files = exporter.export_all_formats(results, company)

        print("\nExported to:")
        for format_type, filepath in files.items():
            print(f"  {format_type.upper()}: {filepath}")

    finally:
        if scraper:
            scraper.close()


def example_with_custom_credentials():
    """Example: Using custom credentials"""
    print("\n\nExample 4: Custom Credentials\n" + "="*60)

    # You can override config credentials
    custom_email = "your_custom_email@example.com"
    custom_password = "your_custom_password"

    scraper = None
    try:
        # Initialize with custom credentials
        scraper = LinkedInScraper(
            email=custom_email,
            password=custom_password,
            headless=False  # Override headless mode
        )

        scraper.setup_driver()
        # ... rest of the code

        print("Note: This is just a demonstration. Use actual credentials.")

    except ValueError as e:
        print(f"Expected error: {e}")
    finally:
        if scraper:
            scraper.close()


def main():
    """Run all examples"""
    print("""
╔══════════════════════════════════════════════════════════╗
║      LinkedIn HR Scraper - Example Usage Scripts        ║
╚══════════════════════════════════════════════════════════╝

This script demonstrates various ways to use the scraper.

⚠️  WARNING: These examples will actually run if you have
    configured your LinkedIn credentials in .env file.

    Each example will open a browser and perform searches.
    Make sure you're ready before running!

""")

    response = input("Do you want to run the examples? (yes/no): ").strip().lower()

    if response != 'yes':
        print("\nExamples cancelled. You can review the code in example_usage.py")
        return

    # Check if credentials are configured
    if not config.LINKEDIN_EMAIL or not config.LINKEDIN_PASSWORD:
        print("\n❌ LinkedIn credentials not configured!")
        print("Please set LINKEDIN_EMAIL and LINKEDIN_PASSWORD in .env file")
        return

    print("\n" + "="*60)
    print("Starting examples...")
    print("="*60)

    # Run examples (comment out the ones you don't want to run)
    # example_basic_search()
    # example_multiple_companies()
    # example_custom_export()
    example_with_custom_credentials()

    print("\n" + "="*60)
    print("Examples completed!")
    print("="*60)


if __name__ == "__main__":
    main()
