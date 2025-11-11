#!/usr/bin/env python3
"""
LinkedIn HR Scraper - Main Script
Search for HR and hiring personnel from any company on LinkedIn
"""
import sys
import argparse
from linkedin_scraper import LinkedInScraper
from data_exporter import DataExporter
import config


def print_banner():
    """Print application banner"""
    banner = """
╔══════════════════════════════════════════════════════════╗
║         LinkedIn HR & Hiring Personnel Scraper          ║
║                                                          ║
║  Search for recruiters, HR managers, and hiring         ║
║  personnel from any company on LinkedIn                 ║
╚══════════════════════════════════════════════════════════╝
"""
    print(banner)


def print_results_summary(results):
    """Print summary of scraped results"""
    if not results:
        print("\n⚠ No results found")
        return

    print("\n" + "="*60)
    print(f"Found {len(results)} HR/Hiring personnel:\n")

    for idx, profile in enumerate(results, 1):
        print(f"{idx}. {profile['name']}")
        print(f"   Title: {profile['title']}")
        print(f"   Location: {profile['location']}")
        print(f"   Profile: {profile['profile_url']}")
        print()


def interactive_mode():
    """Run in interactive mode"""
    print_banner()

    # Get company name
    company_name = input("Enter company name: ").strip()

    if not company_name:
        print("✗ Company name is required!")
        return

    # Get max results
    max_results_input = input("Maximum number of results (default: 50): ").strip()
    max_results = int(max_results_input) if max_results_input.isdigit() else 50

    # Get export format
    print("\nExport format options:")
    print("  1. CSV")
    print("  2. JSON")
    print("  3. Excel")
    print("  4. All formats")

    format_choice = input("Choose format (1-4, default: 1): ").strip()

    format_map = {
        '1': 'csv',
        '2': 'json',
        '3': 'excel',
        '4': 'all'
    }
    export_format = format_map.get(format_choice, 'csv')

    # Run scraper
    run_scraper(company_name, max_results, export_format)


def run_scraper(company_name, max_results=50, export_format='csv'):
    """
    Run the LinkedIn scraper

    Args:
        company_name (str): Name of the company to search
        max_results (int): Maximum number of results
        export_format (str): Export format (csv, json, excel, all)
    """
    scraper = None

    try:
        # Initialize scraper
        print("\n[1/5] Initializing scraper...")
        scraper = LinkedInScraper()

        # Setup driver
        print("[2/5] Setting up browser...")
        scraper.setup_driver()

        # Login
        print("[3/5] Logging into LinkedIn...")
        if not scraper.login():
            print("✗ Failed to login. Please check your credentials.")
            return

        # Search for HR personnel
        print(f"[4/5] Searching for HR personnel at {company_name}...")
        results = scraper.search_hr_personnel(company_name, max_results)

        if not results:
            print("\n⚠ No results found. Try:")
            print("  - Checking the company name spelling")
            print("  - Ensuring you have an active LinkedIn Premium account for better search results")
            print("  - Verifying your LinkedIn account is not restricted")
            return

        # Display results
        print_results_summary(results)

        # Export results
        print(f"[5/5] Exporting results...")
        exporter = DataExporter()

        if export_format == 'all':
            exported_files = exporter.export_all_formats(results, company_name)
            print("\n✓ Data exported to all formats:")
            for format_type, filepath in exported_files.items():
                if filepath:
                    print(f"  {format_type.upper()}: {filepath}")
        else:
            filepath = exporter.export(results, company_name, export_format)
            if filepath:
                print(f"\n✓ Results saved to: {filepath}")

        print("\n✓ Scraping completed successfully!")

    except KeyboardInterrupt:
        print("\n\n⚠ Scraping interrupted by user")

    except Exception as e:
        print(f"\n✗ An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()

    finally:
        if scraper:
            scraper.close()


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='LinkedIn HR & Hiring Personnel Scraper',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode
  python main.py

  # Direct search
  python main.py --company "Google" --max-results 100

  # Export to specific format
  python main.py --company "Microsoft" --format json

  # Export to all formats
  python main.py --company "Amazon" --format all

Note:
  Make sure to configure your LinkedIn credentials in the .env file first!
        """
    )

    parser.add_argument(
        '-c', '--company',
        type=str,
        help='Company name to search'
    )

    parser.add_argument(
        '-m', '--max-results',
        type=int,
        default=50,
        help='Maximum number of results (default: 50)'
    )

    parser.add_argument(
        '-f', '--format',
        type=str,
        choices=['csv', 'json', 'excel', 'all'],
        default='csv',
        help='Export format (default: csv)'
    )

    parser.add_argument(
        '--headless',
        action='store_true',
        help='Run browser in headless mode'
    )

    args = parser.parse_args()

    # Check if credentials are configured
    if not config.LINKEDIN_EMAIL or not config.LINKEDIN_PASSWORD:
        print("⚠ LinkedIn credentials not configured!")
        print("\nPlease follow these steps:")
        print("1. Copy .env.example to .env")
        print("2. Edit .env and add your LinkedIn email and password")
        print("3. Run the script again")
        sys.exit(1)

    # Run in appropriate mode
    if args.company:
        print_banner()
        run_scraper(args.company, args.max_results, args.format)
    else:
        interactive_mode()


if __name__ == "__main__":
    main()
