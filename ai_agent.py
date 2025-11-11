#!/usr/bin/env python3
"""
Autonomous AI Agent for LinkedIn HR Outreach
Automatically scrapes, generates AI-powered messages, and manages workflow
"""
import sys
import os
import argparse
import json
from datetime import datetime
from linkedin_scraper import LinkedInScraper
from ai_message_generator import AIMessageGenerator
from message_generator import MessageGenerator
from data_exporter import DataExporter
from linkedin_messenger import create_messaging_workflow
import config


class LinkedInAIAgent:
    """Autonomous AI agent for LinkedIn outreach"""

    def __init__(self, use_ai=True):
        """
        Initialize AI agent

        Args:
            use_ai (bool): Use AI for message generation (requires API keys)
        """
        self.use_ai = use_ai and os.getenv('USE_AI_MESSAGES', 'False').lower() == 'true'

        if self.use_ai:
            try:
                self.message_generator = AIMessageGenerator()
                print(f"✓ AI Agent initialized with {self.message_generator.provider.upper()}")
            except Exception as e:
                print(f"⚠ AI initialization failed: {str(e)}")
                print("  Falling back to template-based generation")
                self.message_generator = MessageGenerator()
                self.use_ai = False
        else:
            self.message_generator = MessageGenerator()
            print("✓ Agent initialized with template-based generation")

    def run_campaign(self, company_name, scenario='job_seeker', custom_data=None, max_results=50, message_type='connection'):
        """
        Run complete AI-powered outreach campaign

        Args:
            company_name (str): Target company
            scenario (str): Message scenario
            custom_data (dict): Personalization data
            max_results (int): Max profiles to scrape
            message_type (str): 'connection' or 'direct'

        Returns:
            dict: Campaign results and statistics
        """
        campaign_id = f"{company_name.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        print(f"""
╔══════════════════════════════════════════════════════════╗
║          LinkedIn AI Agent - Campaign Launch            ║
╚══════════════════════════════════════════════════════════╝

Campaign ID: {campaign_id}
Company: {company_name}
Scenario: {scenario}
AI-Powered: {self.use_ai}
Message Type: {message_type}
Max Results: {max_results}

""")

        campaign_results = {
            'campaign_id': campaign_id,
            'company': company_name,
            'scenario': scenario,
            'started_at': datetime.now().isoformat(),
            'ai_powered': self.use_ai,
            'profiles_scraped': 0,
            'messages_generated': 0,
            'avg_message_length': 0,
            'files_created': [],
            'errors': []
        }

        scraper = None

        try:
            # Phase 1: Scraping
            print("="*60)
            print("PHASE 1: SCRAPING HR CONTACTS")
            print("="*60)

            scraper = LinkedInScraper()
            scraper.setup_driver()

            if not scraper.login():
                raise Exception("LinkedIn login failed")

            profiles = scraper.search_hr_personnel(company_name, max_results)
            campaign_results['profiles_scraped'] = len(profiles)

            if not profiles:
                print("\n⚠ No profiles found. Campaign stopped.")
                return campaign_results

            # Export scraped data
            exporter = DataExporter()
            scraped_file = exporter.export_to_json(profiles, company_name)
            campaign_results['files_created'].append(scraped_file)

            # Phase 2: AI Message Generation
            print("\n" + "="*60)
            print(f"PHASE 2: {'AI-POWERED' if self.use_ai else 'TEMPLATE-BASED'} MESSAGE GENERATION")
            print("="*60)

            if self.use_ai:
                messages = self.message_generator.generate_bulk_messages(
                    profiles,
                    scenario=scenario,
                    custom_data=custom_data,
                    message_type=message_type
                )
            else:
                messages = self.message_generator.generate_bulk_messages(
                    profiles,
                    scenario=scenario,
                    custom_data=custom_data
                )

            campaign_results['messages_generated'] = len(messages)

            if messages:
                avg_length = sum(m['char_count'] for m in messages) / len(messages)
                campaign_results['avg_message_length'] = round(avg_length, 1)

            # Phase 3: Export and Analysis
            print("\n" + "="*60)
            print("PHASE 3: EXPORT & ANALYSIS")
            print("="*60)

            # Export messages
            messages_file = os.path.join(
                config.OUTPUT_DIRECTORY,
                f"ai_messages_{campaign_id}.json"
            )

            self._export_messages(messages, messages_file, campaign_results)
            campaign_results['files_created'].append(messages_file)

            # Create workflow file for n8n or manual sending
            workflow_file = os.path.join(
                config.OUTPUT_DIRECTORY,
                f"workflow_{campaign_id}.json"
            )

            create_messaging_workflow(profiles, messages, workflow_file)
            campaign_results['files_created'].append(workflow_file)

            # Generate campaign report
            report_file = self._generate_campaign_report(campaign_results, profiles, messages)
            campaign_results['files_created'].append(report_file)

            # Phase 4: Summary
            self._print_campaign_summary(campaign_results, messages)

            return campaign_results

        except KeyboardInterrupt:
            print("\n\n⚠ Campaign interrupted by user")
            campaign_results['status'] = 'interrupted'
            return campaign_results

        except Exception as e:
            print(f"\n✗ Campaign failed: {str(e)}")
            campaign_results['errors'].append(str(e))
            campaign_results['status'] = 'failed'
            import traceback
            traceback.print_exc()
            return campaign_results

        finally:
            if scraper:
                scraper.close()

            campaign_results['completed_at'] = datetime.now().isoformat()

    def _export_messages(self, messages, output_file, campaign_results):
        """Export messages with campaign metadata"""
        export_data = {
            'campaign_id': campaign_results['campaign_id'],
            'company': campaign_results['company'],
            'scenario': campaign_results['scenario'],
            'ai_powered': campaign_results['ai_powered'],
            'generated_at': datetime.now().isoformat(),
            'total_messages': len(messages),
            'messages': messages
        }

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)

        print(f"✓ Messages exported to: {output_file}")

    def _generate_campaign_report(self, campaign_results, profiles, messages):
        """Generate detailed campaign report"""
        report_file = os.path.join(
            config.OUTPUT_DIRECTORY,
            f"report_{campaign_results['campaign_id']}.md"
        )

        report = f"""# LinkedIn AI Agent Campaign Report

## Campaign Overview

- **Campaign ID**: {campaign_results['campaign_id']}
- **Company**: {campaign_results['company']}
- **Scenario**: {campaign_results['scenario']}
- **Started**: {campaign_results['started_at']}
- **AI-Powered**: {campaign_results['ai_powered']}

## Results

- **Profiles Scraped**: {campaign_results['profiles_scraped']}
- **Messages Generated**: {campaign_results['messages_generated']}
- **Average Message Length**: {campaign_results['avg_message_length']} characters

## Generated Files

"""
        for file in campaign_results['files_created']:
            report += f"- `{file}`\n"

        report += "\n## Sample Messages\n\n"

        # Include first 3 messages as samples
        for i, msg in enumerate(messages[:3], 1):
            report += f"""### Message {i}

**To**: {msg['recipient_name']}
**Title**: {msg['recipient_title']}
**Length**: {msg['char_count']} characters

```
{msg['message']}
```

---

"""

        report += f"""
## Message Statistics

- **Shortest Message**: {min(m['char_count'] for m in messages)} characters
- **Longest Message**: {max(m['char_count'] for m in messages)} characters
- **Average Length**: {sum(m['char_count'] for m in messages) / len(messages):.1f} characters

## Next Steps

1. **Review Messages**: Check the generated messages in `{campaign_results['files_created'][1]}`
2. **Import to n8n**: Use workflow file `{campaign_results['files_created'][2]}`
3. **Send Messages**: Use manual review or automated sending
4. **Track Results**: Monitor response rates and engagement

## AI Details

"""
        if self.use_ai:
            sample_msg = messages[0]
            report += f"""
- **Provider**: {sample_msg.get('ai_provider', 'N/A').upper()}
- **Model**: {sample_msg.get('ai_model', 'N/A')}
- **Message Type**: {sample_msg.get('message_type', 'N/A')}

The messages were generated using AI to ensure maximum personalization and authenticity.
"""
        else:
            report += """
Messages were generated using template-based personalization.
For AI-powered messages, enable AI in your .env file.
"""

        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"✓ Campaign report generated: {report_file}")

        return report_file

    def _print_campaign_summary(self, campaign_results, messages):
        """Print campaign summary"""
        print("\n" + "="*60)
        print("CAMPAIGN COMPLETE")
        print("="*60)

        print(f"""
📊 Campaign Statistics:
   • Profiles found: {campaign_results['profiles_scraped']}
   • Messages generated: {campaign_results['messages_generated']}
   • Average length: {campaign_results['avg_message_length']} chars
   • AI-powered: {'Yes' if campaign_results['ai_powered'] else 'No'}

📁 Files Created:
""")
        for file in campaign_results['files_created']:
            print(f"   • {file}")

        print(f"""
🎯 Quality Metrics:
   • Shortest message: {min(m['char_count'] for m in messages)} chars
   • Longest message: {max(m['char_count'] for m in messages)} chars
   • Within LinkedIn limits: {'✓ Yes' if all(m['char_count'] <= 300 for m in messages if m.get('message_type') == 'connection') else '⚠ Some messages exceed limits'}

📝 Next Steps:
   1. Review the campaign report
   2. Check generated messages
   3. Import workflow to n8n or send manually
   4. Track response rates

{"🤖 Messages generated with " + messages[0].get('ai_provider', 'template').upper() + " AI" if campaign_results['ai_powered'] else ""}
""")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='LinkedIn AI Agent - Autonomous Outreach Campaign',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run AI-powered campaign (requires API keys)
  python ai_agent.py --company "Google" --scenario job_seeker

  # With full personalization
  python ai_agent.py \\
    --company "Microsoft" \\
    --scenario job_seeker \\
    --role "Data Scientist" \\
    --years "4" \\
    --skills "Python, Machine Learning, TensorFlow" \\
    --message-type connection

  # Multiple companies campaign
  python ai_agent.py --companies "Google,Microsoft,Amazon"

  # Disable AI (use templates)
  python ai_agent.py --company "Apple" --no-ai

Note: Ensure USE_AI_MESSAGES=True and API keys are configured in .env
        """
    )

    parser.add_argument('-c', '--company', type=str, help='Target company')
    parser.add_argument('--companies', type=str, help='Multiple companies (comma-separated)')
    parser.add_argument('-s', '--scenario', type=str, default='job_seeker',
                        choices=['job_seeker', 'networking', 'recruiter_outreach', 'informational_interview'])
    parser.add_argument('-m', '--max-results', type=int, default=50)
    parser.add_argument('--message-type', type=str, default='connection',
                        choices=['connection', 'direct'],
                        help='Connection request (300 chars) or direct message')
    parser.add_argument('--role', type=str, help='Your role/title')
    parser.add_argument('--years', type=str, help='Years of experience')
    parser.add_argument('--skills', type=str, help='Key skills')
    parser.add_argument('--industry', type=str, help='Industry')
    parser.add_argument('--no-ai', action='store_true', help='Disable AI, use templates')

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

    # Initialize agent
    agent = LinkedInAIAgent(use_ai=not args.no_ai)

    # Run campaigns
    if args.companies:
        companies = [c.strip() for c in args.companies.split(',')]
        print(f"\n🚀 Running multi-company campaign for {len(companies)} companies\n")

        all_results = []
        for company in companies:
            print(f"\n{'='*60}")
            print(f"Starting campaign for {company}")
            print(f"{'='*60}\n")

            results = agent.run_campaign(
                company,
                args.scenario,
                custom_data if custom_data else None,
                args.max_results,
                args.message_type
            )
            all_results.append(results)

        # Print overall summary
        print("\n" + "="*60)
        print("MULTI-COMPANY CAMPAIGN SUMMARY")
        print("="*60)
        for result in all_results:
            print(f"\n{result['company']}:")
            print(f"  Profiles: {result['profiles_scraped']}")
            print(f"  Messages: {result['messages_generated']}")

    elif args.company:
        agent.run_campaign(
            args.company,
            args.scenario,
            custom_data if custom_data else None,
            args.max_results,
            args.message_type
        )
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
