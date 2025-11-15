"""
AI-powered message generator for LinkedIn HR outreach
Creates personalized, human-like messages for different scenarios
"""
import random
import json
from datetime import datetime


class MessageGenerator:
    """Generate personalized LinkedIn messages for HR outreach"""

    def __init__(self, use_ai=False, api_key=None):
        """
        Initialize message generator

        Args:
            use_ai (bool): Use AI API for message generation (OpenAI/Anthropic)
            api_key (str): API key for AI service
        """
        self.use_ai = use_ai
        self.api_key = api_key
        self.templates = self._load_templates()

    def _load_templates(self):
        """Load message templates for different scenarios"""
        return {
            'job_seeker': {
                'greeting': [
                    "Hi {name}",
                    "Hello {name}",
                    "Hi there {name}",
                ],
                'introduction': [
                    "I came across your profile while researching {company} and was impressed by your work in talent acquisition.",
                    "I noticed you're leading talent acquisition at {company}, and I wanted to reach out.",
                    "Your experience in HR at {company} caught my attention.",
                    "I've been following {company}'s growth and noticed your role in building the team.",
                ],
                'value_proposition': [
                    "I'm a {your_role} with {years} years of experience in {skills}, and I'm actively exploring new opportunities.",
                    "As a {your_role} specializing in {skills}, I'm interested in learning more about opportunities at {company}.",
                    "I bring {years} years of experience in {skills} and am particularly drawn to {company}'s mission.",
                    "With my background in {skills} and passion for {industry}, I believe I could contribute meaningfully to {company}.",
                ],
                'call_to_action': [
                    "Would you be open to a brief conversation about current or future opportunities?",
                    "I'd love to connect and learn more about your team's needs.",
                    "Would you have 15 minutes for a quick chat about potential openings?",
                    "I'd appreciate the opportunity to discuss how my skills might align with your team's goals.",
                ],
                'closing': [
                    "Thanks for your time, and I look forward to connecting!",
                    "Looking forward to hearing from you!",
                    "Thank you for considering my request!",
                    "I appreciate your time and consideration!",
                ]
            },
            'networking': {
                'greeting': [
                    "Hi {name}",
                    "Hello {name}",
                ],
                'introduction': [
                    "I noticed we both work in the {industry} space and wanted to connect.",
                    "Your work at {company} has been really impressive, especially in talent development.",
                    "I've been following {company}'s innovative approach to hiring and wanted to reach out.",
                    "As someone passionate about {industry}, I wanted to connect with fellow professionals.",
                ],
                'value_proposition': [
                    "I'm always looking to expand my network with talented HR professionals.",
                    "I'd love to exchange insights about current trends in talent acquisition.",
                    "I think we could have some interesting conversations about the evolving HR landscape.",
                    "I'm keen to learn from your experience in building high-performing teams.",
                ],
                'call_to_action': [
                    "Would you be open to connecting?",
                    "I'd love to add you to my professional network.",
                    "Let's connect and stay in touch!",
                    "Would be great to have you in my network!",
                ],
                'closing': [
                    "Best regards!",
                    "Thanks for connecting!",
                    "Looking forward to staying in touch!",
                    "Cheers!",
                ]
            },
            'recruiter_outreach': {
                'greeting': [
                    "Hi {name}",
                    "Hello {name}",
                ],
                'introduction': [
                    "I'm reaching out because we're helping companies in the {industry} space find exceptional talent.",
                    "Your work in talent acquisition at {company} is impressive, and I wanted to connect.",
                    "I specialize in connecting top-tier {industry} talent with innovative companies.",
                ],
                'value_proposition': [
                    "I regularly work with {your_role} professionals who might be a great fit for {company}.",
                    "I have several candidates with strong backgrounds in {skills} who are exploring new opportunities.",
                    "I'd love to learn more about your hiring needs and see if I can help.",
                ],
                'call_to_action': [
                    "Would you be open to a brief conversation about your current hiring needs?",
                    "Could we schedule a quick call to discuss potential collaboration?",
                    "I'd love to explore how we might work together.",
                ],
                'closing': [
                    "Looking forward to connecting!",
                    "Thanks for your time!",
                    "Excited to potentially collaborate!",
                ]
            },
            'informational_interview': {
                'greeting': [
                    "Hi {name}",
                    "Hello {name}",
                ],
                'introduction': [
                    "I'm exploring a career transition into {industry} and noticed your impressive background at {company}.",
                    "Your career path from {previous_company} to {company} really caught my attention.",
                    "I'm researching companies in the {industry} space, and {company} stands out.",
                ],
                'value_proposition': [
                    "I'd love to learn about your experience in talent acquisition and hear any advice you might have.",
                    "Your insights on building teams at {company} would be incredibly valuable to me.",
                    "I'd appreciate learning from your perspective on the industry and {company}'s culture.",
                ],
                'call_to_action': [
                    "Would you have 15-20 minutes for an informational chat?",
                    "Could I treat you to a virtual coffee and pick your brain?",
                    "Would you be open to a brief informational interview?",
                ],
                'closing': [
                    "Thank you for considering my request!",
                    "I really appreciate your time!",
                    "Thanks in advance for any guidance you can share!",
                ]
            }
        }

    def generate_message(self, profile, scenario='job_seeker', custom_data=None):
        """
        Generate a personalized message for a profile

        Args:
            profile (dict): HR profile data from scraper
            scenario (str): Type of message (job_seeker, networking, recruiter_outreach, informational_interview)
            custom_data (dict): Additional data for personalization

        Returns:
            dict: Generated message with metadata
        """
        if self.use_ai and self.api_key:
            return self._generate_ai_message(profile, scenario, custom_data)
        else:
            return self._generate_template_message(profile, scenario, custom_data)

    def _generate_template_message(self, profile, scenario, custom_data):
        """Generate message using templates"""
        templates = self.templates.get(scenario, self.templates['job_seeker'])
        custom_data = custom_data or {}

        # Extract profile data
        name = profile.get('name', 'there').split()[0]  # Use first name
        company = self._extract_company(profile.get('title', ''))
        title = profile.get('title', 'HR Professional')

        # Build message sections
        greeting = random.choice(templates['greeting']).format(name=name)
        introduction = random.choice(templates['introduction']).format(
            name=name,
            company=company,
            **custom_data
        )
        value_prop = random.choice(templates['value_proposition']).format(
            company=company,
            **custom_data
        )
        cta = random.choice(templates['call_to_action']).format(
            company=company,
            **custom_data
        )
        closing = random.choice(templates['closing'])

        # Assemble message
        message = f"{greeting},\n\n{introduction}\n\n{value_prop}\n\n{cta}\n\n{closing}"

        return {
            'recipient_name': profile.get('name'),
            'recipient_title': title,
            'recipient_url': profile.get('profile_url'),
            'message': message,
            'scenario': scenario,
            'generated_at': datetime.now().isoformat(),
            'char_count': len(message),
            'word_count': len(message.split())
        }

    def _generate_ai_message(self, profile, scenario, custom_data):
        """Generate message using AI (OpenAI/Anthropic)"""
        try:
            # Import AI generator (only if needed)
            from ai_message_generator import AIMessageGenerator

            ai_generator = AIMessageGenerator()
            message_data = ai_generator.generate_message(
                profile,
                scenario=scenario,
                custom_data=custom_data,
                message_type='connection'
            )
            return message_data

        except ImportError:
            print("⚠ AI message generator not available, using templates")
            return self._generate_template_message(profile, scenario, custom_data)
        except Exception as e:
            print(f"⚠ AI generation failed ({str(e)}), falling back to templates")
            return self._generate_template_message(profile, scenario, custom_data)

    def _build_ai_prompt(self, profile, scenario, custom_data):
        """Build prompt for AI message generation"""
        name = profile.get('name', 'there')
        title = profile.get('title', 'HR Professional')
        company = self._extract_company(title)

        prompt = f"""Generate a personalized, professional LinkedIn message for the following scenario:

Scenario: {scenario}
Recipient: {name}
Their Role: {title}
Company: {company}

Requirements:
- Keep it under 300 characters (LinkedIn connection note limit) or 1000 characters for InMail
- Make it natural and conversational
- Personalize based on their role and company
- Include a clear call to action
- Be respectful of their time
- Avoid being overly salesy or pushy

Custom Context: {json.dumps(custom_data, indent=2)}

Generate the message:"""

        return prompt

    def _extract_company(self, title_or_text):
        """Extract company name from title or text"""
        # Simple extraction - look for "at Company" pattern
        if ' at ' in title_or_text:
            parts = title_or_text.split(' at ')
            if len(parts) > 1:
                company = parts[1].split(',')[0].strip()
                return company
        return "your company"

    def generate_bulk_messages(self, profiles, scenario='job_seeker', custom_data=None):
        """
        Generate messages for multiple profiles

        Args:
            profiles (list): List of HR profile dictionaries
            scenario (str): Message scenario
            custom_data (dict): Additional personalization data

        Returns:
            list: List of generated message dictionaries
        """
        messages = []

        for profile in profiles:
            try:
                message_data = self.generate_message(profile, scenario, custom_data)
                messages.append(message_data)
            except Exception as e:
                print(f"Warning: Failed to generate message for {profile.get('name', 'unknown')}: {str(e)}")
                continue

        return messages

    def export_messages(self, messages, output_file='messages.json'):
        """
        Export generated messages to file

        Args:
            messages (list): List of generated messages
            output_file (str): Output file path
        """
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                'generated_at': datetime.now().isoformat(),
                'total_messages': len(messages),
                'messages': messages
            }, f, indent=2, ensure_ascii=False)

        print(f"✓ Exported {len(messages)} messages to {output_file}")

    def get_message_statistics(self, messages):
        """Get statistics about generated messages"""
        if not messages:
            return {}

        char_counts = [m['char_count'] for m in messages]
        word_counts = [m['word_count'] for m in messages]

        return {
            'total_messages': len(messages),
            'avg_char_count': sum(char_counts) / len(char_counts),
            'avg_word_count': sum(word_counts) / len(word_counts),
            'min_char_count': min(char_counts),
            'max_char_count': max(char_counts),
            'scenarios': list(set(m['scenario'] for m in messages))
        }


def main():
    """Example usage"""
    # Example profile
    example_profile = {
        'name': 'Jane Smith',
        'title': 'Senior Talent Acquisition Manager at Google',
        'location': 'San Francisco Bay Area',
        'profile_url': 'https://linkedin.com/in/janesmith'
    }

    # Initialize generator
    generator = MessageGenerator()

    # Generate messages for different scenarios
    scenarios = ['job_seeker', 'networking', 'informational_interview']

    print("Message Generator Examples\n" + "="*60 + "\n")

    for scenario in scenarios:
        custom_data = {
            'your_role': 'Software Engineer',
            'years': '5',
            'skills': 'Python, React, Cloud Architecture',
            'industry': 'technology'
        }

        message_data = generator.generate_message(example_profile, scenario, custom_data)

        print(f"Scenario: {scenario.upper()}")
        print(f"To: {message_data['recipient_name']} ({message_data['recipient_title']})")
        print(f"Characters: {message_data['char_count']}")
        print(f"\nMessage:\n{message_data['message']}")
        print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    main()
