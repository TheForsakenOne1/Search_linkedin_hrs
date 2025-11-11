#!/usr/bin/env python3
"""
Complete LinkedIn HR Outreach Workflow
Combines scraping, message generation, and sending workflow
"""
import sys
import argparse
import os
from linkedin_scraper import LinkedInScraper
from message_generator import MessageGenerator
from linkedin_messenger import LinkedInMessenger, create_messaging_workflow
from data_exporter import DataExporter
import config


def print_workflow_banner():
    """Print workflow banner"""
    banner = """
╔══════════════════════════════════════════════════════════╗
║      LinkedIn HR Complete Outreach Workflow             ║
║                                                          ║
║  1. Scrape HR contacts from company                     ║
║  2. Generate personalized messages                      ║
║  3. Review and send (or export for n8n)                 ║
╚══════════════════════════════════════════════════════════╝
"""
    print(banner)


def run_complete_workflow(
    company_name,
    max_results=50,
    scenario='job_seeker',
    custom_data=None,
    auto_send=False,
    export_only=False
):
    """
    Run the complete workflow: scrape -> generate -> send/export

    Args:
        company_name (str): Company to search
        max_results (int): Maximum profiles to scrape
        scenario (str): Message scenario
        custom_data (dict): Custom personalization data
        auto_send (bool): Auto-send without confirmation
        export_only (bool): Only export, don't send
    """
    scraper = None
    results_summary = {
        'company': company_name,
        'profiles_found': 0,
        'messages_generated': 0,
        'messages_sent': 0,
        'files_created': []
    }

    try:
        print("\n" + "="*60)
        print("STEP 1: SCRAPING HR CONTACTS")
        print("="*60)

        # Initialize scraper
        scraper = LinkedInScraper()
        scraper.setup_driver()

        if not scraper.login():
            print("✗ Failed to login to LinkedIn")
            return results_summary

        # Scrape HR personnel
        profiles = scraper.search_hr_personnel(company_name, max_results)
        results_summary['profiles_found'] = len(profiles)

        if not profiles:
            print("\n⚠ No profiles found. Exiting workflow.")
            return results_summary

        # Export scraped data
        exporter = DataExporter()
        scraped_file = exporter.export_to_json(profiles, company_name)
        results_summary['files_created'].append(scraped_file)

        print("\n" + "="*60)
        print("STEP 2: GENERATING PERSONALIZED MESSAGES")
        print("="*60)

        # Generate messages
        generator = MessageGenerator()
        messages = generator.generate_bulk_messages(profiles, scenario, custom_data)
        results_summary['messages_generated'] = len(messages)

        # Show statistics
        stats = generator.get_message_statistics(messages)
        print(f"\n✓ Generated {len(messages)} messages")
        print(f"  Average length: {stats['avg_char_count']:.0f} characters")
        print(f"  Scenario: {scenario}")

        # Export messages
        messages_file = os.path.join(
            config.OUTPUT_DIRECTORY,
            f"messages_{company_name}_{scenario}.json"
        )
        generator.export_messages(messages, messages_file)
        results_summary['files_created'].append(messages_file)

        # Create messaging workflow file (for n8n or manual sending)
        workflow_file = os.path.join(
            config.OUTPUT_DIRECTORY,
            f"workflow_{company_name}.json"
        )
        create_messaging_workflow(profiles, messages, workflow_file)
        results_summary['files_created'].append(workflow_file)

        if export_only:
            print("\n" + "="*60)
            print("EXPORT COMPLETE - FILES READY FOR N8N")
            print("="*60)
            print("\nGenerated files:")
            for file in results_summary['files_created']:
                print(f"  • {file}")
            print("\nNext steps:")
            print("  1. Import workflow file into n8n")
            print("  2. Configure n8n workflow trigger")
            print("  3. Review and send messages through n8n")
            return results_summary

        print("\n" + "="*60)
        print("STEP 3: REVIEW AND SEND MESSAGES")
        print("="*60)

        # Initialize messenger
        messenger = LinkedInMessenger(scraper.driver)

        # Prepare messages for sending
        messages_to_send = [
            {'profile': profile, 'message': msg['message']}
            for profile, msg in zip(profiles, messages)
        ]

        # Send messages with review
        print(f"\nReady to send {len(messages_to_send)} messages")
        print("You will be prompted to review each message before sending.\n")

        if not auto_send:
            response = input("Continue with sending? (yes/no): ").strip().lower()
            if response != 'yes':
                print("\n✓ Messages saved for later. Check the workflow file.")
                return results_summary

        send_results = messenger.batch_send_messages(
            messages_to_send,
            auto_send=auto_send,
            delay_range=(15, 30)  # 15-30 seconds between messages
        )

        results_summary['messages_sent'] = send_results['sent']

        print("\n" + "="*60)
        print("WORKFLOW COMPLETE")
        print("="*60)
        print(f"\nResults:")
        print(f"  • Profiles found: {results_summary['profiles_found']}")
        print(f"  • Messages generated: {results_summary['messages_generated']}")
        print(f"  • Messages sent: {results_summary['messages_sent']}")
        print(f"  • Messages failed: {send_results['failed']}")
        print(f"  • Messages skipped: {send_results['skipped']}")
        print(f"\nFiles created:")
        for file in results_summary['files_created']:
            print(f"  • {file}")

        return results_summary

    except KeyboardInterrupt:
        print("\n\n⚠ Workflow interrupted by user")
        return results_summary

    except Exception as e:
        print(f"\n✗ Error in workflow: {str(e)}")
        import traceback
        traceback.print_exc()
        return results_summary

    finally:
        if scraper:
            scraper.close()


def interactive_workflow():
    """Run workflow in interactive mode"""
    print_workflow_banner()

    # Get company name
    company_name = input("Enter company name: ").strip()
    if not company_name:
        print("✗ Company name is required!")
        return

    # Get max results
    max_results_input = input("Maximum number of profiles (default: 50): ").strip()
    max_results = int(max_results_input) if max_results_input.isdigit() else 50

    # Get scenario
    print("\nMessage scenarios:")
    print("  1. Job Seeker (looking for opportunities)")
    print("  2. Networking (professional connection)")
    print("  3. Recruiter Outreach (offering candidates)")
    print("  4. Informational Interview (career advice)")

    scenario_choice = input("Choose scenario (1-4, default: 1): ").strip()
    scenario_map = {
        '1': 'job_seeker',
        '2': 'networking',
        '3': 'recruiter_outreach',
        '4': 'informational_interview'
    }
    scenario = scenario_map.get(scenario_choice, 'job_seeker')

    # Get custom data for job seekers
    custom_data = {}
    if scenario == 'job_seeker':
        print("\nPersonalization (press Enter to skip):")
        your_role = input("  Your role/title: ").strip()
        years = input("  Years of experience: ").strip()
        skills = input("  Key skills: ").strip()
        industry = input("  Industry: ").strip()

        if your_role:
            custom_data['your_role'] = your_role
        if years:
            custom_data['years'] = years
        if skills:
            custom_data['skills'] = skills
        if industry:
            custom_data['industry'] = industry

    # Choose workflow mode
    print("\nWorkflow mode:")
    print("  1. Export for n8n (recommended - safer)")
    print("  2. Review and send each message manually")
    print("  3. Auto-send all (NOT recommended - use with caution)")

    mode_choice = input("Choose mode (1-3, default: 1): ").strip()

    export_only = mode_choice == '1' or mode_choice == ''
    auto_send = mode_choice == '3'

    if auto_send:
        confirm = input("\n⚠️  WARNING: Auto-send will send all messages without review. Continue? (yes/no): ").strip().lower()
        if confirm != 'yes':
            export_only = True
            auto_send = False
            print("Switching to export-only mode.")

    # Run workflow
    run_complete_workflow(
        company_name,
        max_results,
        scenario,
        custom_data,
        auto_send,
        export_only
    )


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='LinkedIn HR Complete Outreach Workflow',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode
  python complete_workflow.py

  # Export for n8n
  python complete_workflow.py --company "Google" --export-only

  # Full workflow with manual review
  python complete_workflow.py --company "Microsoft" --scenario job_seeker

  # Specify custom data
  python complete_workflow.py --company "Amazon" \\
    --scenario job_seeker \\
    --role "Software Engineer" \\
    --years "5" \\
    --skills "Python, React, AWS"

Note: Export-only mode is recommended for safety and compliance.
      Review messages before sending to avoid spam or TOS violations.
        """
    )

    parser.add_argument('-c', '--company', type=str, help='Company name')
    parser.add_argument('-m', '--max-results', type=int, default=50, help='Maximum results')
    parser.add_argument('-s', '--scenario', type=str, default='job_seeker',
                        choices=['job_seeker', 'networking', 'recruiter_outreach', 'informational_interview'],
                        help='Message scenario')
    parser.add_argument('--role', type=str, help='Your role/title')
    parser.add_argument('--years', type=str, help='Years of experience')
    parser.add_argument('--skills', type=str, help='Key skills')
    parser.add_argument('--industry', type=str, help='Industry')
    parser.add_argument('--export-only', action='store_true', help='Export only, do not send')
    parser.add_argument('--auto-send', action='store_true', help='Auto-send without review (use with caution)')

    args = parser.parse_args()

    # Check credentials
    if not config.LINKEDIN_EMAIL or not config.LINKEDIN_PASSWORD:
        print("⚠ LinkedIn credentials not configured!")
        print("Please set LINKEDIN_EMAIL and LINKEDIN_PASSWORD in .env file")
        sys.exit(1)

    # Build custom data
    custom_data = {}
    if args.role:
        custom_data['your_role'] = args.role
    if args.years:
        custom_data['years'] = args.years
    if args.skills:
        custom_data['skills'] = args.skills
    if args.industry:
        custom_data['industry'] = args.industry

    # Run workflow
    if args.company:
        print_workflow_banner()
        run_complete_workflow(
            args.company,
            args.max_results,
            args.scenario,
            custom_data if custom_data else None,
            args.auto_send,
            args.export_only
        )
    else:
        interactive_workflow()


if __name__ == "__main__":
    main()
