"""
AI-powered message generator using OpenAI GPT-4 or Anthropic Claude
Generates highly personalized LinkedIn messages
"""
import os
from dotenv import load_dotenv

load_dotenv()


class AIMessageGenerator:
    """Generate personalized messages using AI (OpenAI or Anthropic)"""

    def __init__(self, provider=None, api_key=None, model=None):
        """
        Initialize AI message generator

        Args:
            provider (str): 'openai' or 'anthropic'
            api_key (str): API key for the provider
            model (str): Model name to use
        """
        self.provider = provider or os.getenv('AI_PROVIDER', 'openai')
        self.api_key = api_key or self._get_api_key()
        self.model = model or self._get_model()

        if self.provider == 'openai':
            self._init_openai()
        elif self.provider == 'anthropic':
            self._init_anthropic()
        else:
            raise ValueError(f"Unsupported AI provider: {self.provider}")

    def _get_api_key(self):
        """Get API key from environment"""
        if self.provider == 'openai':
            key = os.getenv('OPENAI_API_KEY')
            if not key or key == 'your_openai_api_key_here':
                raise ValueError("OPENAI_API_KEY not configured in .env file")
            return key
        elif self.provider == 'anthropic':
            key = os.getenv('ANTHROPIC_API_KEY')
            if not key or key == 'your_anthropic_api_key_here':
                raise ValueError("ANTHROPIC_API_KEY not configured in .env file")
            return key

    def _get_model(self):
        """Get model name from environment"""
        if self.provider == 'openai':
            return os.getenv('OPENAI_MODEL', 'gpt-4')
        elif self.provider == 'anthropic':
            return os.getenv('ANTHROPIC_MODEL', 'claude-3-5-sonnet-20241022')

    def _init_openai(self):
        """Initialize OpenAI client"""
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=self.api_key)
            print(f"✓ OpenAI initialized with model: {self.model}")
        except ImportError:
            raise ImportError("OpenAI library not installed. Run: pip install openai")

    def _init_anthropic(self):
        """Initialize Anthropic client"""
        try:
            import anthropic
            self.client = anthropic.Anthropic(api_key=self.api_key)
            print(f"✓ Anthropic initialized with model: {self.model}")
        except ImportError:
            raise ImportError("Anthropic library not installed. Run: pip install anthropic")

    def generate_message(self, profile, scenario='job_seeker', custom_data=None, message_type='connection'):
        """
        Generate personalized message using AI

        Args:
            profile (dict): HR profile data with name, title, location, company
            scenario (str): Message scenario
            custom_data (dict): Additional personalization data
            message_type (str): 'connection' (300 chars) or 'direct' (longer)

        Returns:
            dict: Generated message with metadata
        """
        prompt = self._build_prompt(profile, scenario, custom_data, message_type)

        try:
            if self.provider == 'openai':
                message = self._generate_with_openai(prompt, message_type)
            elif self.provider == 'anthropic':
                message = self._generate_with_anthropic(prompt, message_type)

            return {
                'recipient_name': profile.get('name'),
                'recipient_title': profile.get('title'),
                'recipient_url': profile.get('profile_url'),
                'message': message,
                'scenario': scenario,
                'ai_provider': self.provider,
                'ai_model': self.model,
                'message_type': message_type,
                'char_count': len(message),
                'word_count': len(message.split())
            }

        except Exception as e:
            raise Exception(f"AI generation failed: {str(e)}")

    def _generate_with_openai(self, prompt, message_type):
        """Generate message using OpenAI"""
        max_tokens = 150 if message_type == 'connection' else 500
        temperature = float(os.getenv('OPENAI_TEMPERATURE', '0.7'))

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional LinkedIn message writer who creates personalized, authentic, and engaging connection requests and messages. Your messages are warm, concise, and respectful of the recipient's time."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=max_tokens,
            temperature=temperature
        )

        return response.choices[0].message.content.strip()

    def _generate_with_anthropic(self, prompt, message_type):
        """Generate message using Anthropic Claude"""
        max_tokens = int(os.getenv('ANTHROPIC_MAX_TOKENS', '1000'))

        message = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return message.content[0].text.strip()

    def _build_prompt(self, profile, scenario, custom_data, message_type):
        """Build AI prompt for message generation"""
        custom_data = custom_data or {}

        # Extract profile info
        name = profile.get('name', 'there')
        first_name = name.split()[0] if name else 'there'
        title = profile.get('title', 'Professional')
        location = profile.get('location', '')

        # Extract company from title
        company = self._extract_company(title)

        # Character limit based on message type
        char_limit = 300 if message_type == 'connection' else 1500

        # Build scenario-specific context
        scenario_context = self._get_scenario_context(scenario, custom_data)

        prompt = f"""Write a personalized LinkedIn message to {first_name} ({title}) at {company}.

MESSAGE TYPE: {"LinkedIn connection request (must be under 300 characters)" if message_type == 'connection' else "LinkedIn direct message (can be up to 1500 characters)"}

SCENARIO: {scenario}
{scenario_context}

RECIPIENT DETAILS:
- Name: {name}
- Title: {title}
- Company: {company}
- Location: {location}

REQUIREMENTS:
1. Must be under {char_limit} characters
2. Sound natural and conversational (not salesy or robotic)
3. Be specific about why you're reaching out to THEM specifically
4. Reference their role or company authentically
5. Include a clear but gentle call-to-action
6. Be respectful and professional
7. Don't use overly formal language or clichés
8. Make it feel like a human wrote it, not AI

WHAT TO AVOID:
- Generic "I came across your profile" openings
- Excessive flattery or buzzwords
- Being too pushy or aggressive
- Making it all about yourself
- Long-winded explanations

Generate ONLY the message text (no subject line, no "Dear X", just the message body starting with a natural greeting).
"""

        return prompt

    def _get_scenario_context(self, scenario, custom_data):
        """Get context for different scenarios"""
        contexts = {
            'job_seeker': f"""
You are looking for job opportunities. Your background:
- Role: {custom_data.get('your_role', 'Professional')}
- Experience: {custom_data.get('years', 'several')} years
- Key skills: {custom_data.get('skills', 'various technologies')}
- Industry: {custom_data.get('industry', 'technology')}

Express genuine interest in their company and inquire about potential opportunities in a humble, non-demanding way.
""",
            'networking': f"""
You want to expand your professional network. Your background:
- Industry: {custom_data.get('industry', 'technology')}
- Interests: {custom_data.get('interests', 'professional growth and learning')}

Focus on mutual professional interests and the value of connecting with other professionals in your field.
""",
            'recruiter_outreach': f"""
You are a recruiter with quality candidates. Your focus:
- Specialization: {custom_data.get('specialization', 'technical recruiting')}
- Candidate types: {custom_data.get('candidate_types', 'experienced professionals')}

Offer value by mentioning you work with quality candidates that might fit their hiring needs. Don't oversell.
""",
            'informational_interview': f"""
You're seeking career advice and insights. Your situation:
- Current stage: {custom_data.get('career_stage', 'mid-career professional')}
- Interests: {custom_data.get('interests', 'career growth and development')}

Be respectful of their time and show genuine interest in learning from their experience.
"""
        }

        return contexts.get(scenario, contexts['job_seeker'])

    def _extract_company(self, title_or_text):
        """Extract company name from title"""
        if ' at ' in title_or_text:
            parts = title_or_text.split(' at ')
            if len(parts) > 1:
                company = parts[1].split(',')[0].split('|')[0].strip()
                return company
        return "their company"

    def generate_bulk_messages(self, profiles, scenario='job_seeker', custom_data=None, message_type='connection'):
        """
        Generate messages for multiple profiles

        Args:
            profiles (list): List of profile dictionaries
            scenario (str): Message scenario
            custom_data (dict): Personalization data
            message_type (str): 'connection' or 'direct'

        Returns:
            list: List of generated message dictionaries
        """
        messages = []
        total = len(profiles)

        print(f"\nGenerating {total} AI-powered messages...")
        print(f"Provider: {self.provider} | Model: {self.model}")
        print("="*60)

        for idx, profile in enumerate(profiles, 1):
            try:
                print(f"[{idx}/{total}] Generating for {profile.get('name', 'Unknown')}...", end=' ')
                message_data = self.generate_message(profile, scenario, custom_data, message_type)
                messages.append(message_data)
                print(f"✓ ({message_data['char_count']} chars)")

            except Exception as e:
                print(f"✗ Failed: {str(e)}")
                continue

        print("="*60)
        print(f"✓ Generated {len(messages)}/{total} messages successfully")

        return messages


def main():
    """Example usage"""
    import sys

    print("""
╔══════════════════════════════════════════════════════════╗
║        AI-Powered LinkedIn Message Generator            ║
╚══════════════════════════════════════════════════════════╝
""")

    # Check if AI is configured
    use_ai = os.getenv('USE_AI_MESSAGES', 'False').lower() == 'true'

    if not use_ai:
        print("⚠ AI message generation is disabled.")
        print("\nTo enable:")
        print("1. Edit .env file")
        print("2. Set USE_AI_MESSAGES=True")
        print("3. Add your OPENAI_API_KEY or ANTHROPIC_API_KEY")
        sys.exit(1)

    # Example profile
    example_profile = {
        'name': 'Sarah Johnson',
        'title': 'Senior Talent Acquisition Manager at Google',
        'location': 'San Francisco Bay Area',
        'profile_url': 'https://linkedin.com/in/sarahjohnson'
    }

    # Custom data
    custom_data = {
        'your_role': 'Senior Software Engineer',
        'years': '7',
        'skills': 'Python, Kubernetes, React, Machine Learning',
        'industry': 'technology'
    }

    try:
        # Initialize AI generator
        provider = os.getenv('AI_PROVIDER', 'openai')
        print(f"Initializing {provider.upper()} AI generator...\n")

        generator = AIMessageGenerator()

        # Generate connection request message
        print("="*60)
        print("CONNECTION REQUEST MESSAGE (300 char limit):")
        print("="*60)

        connection_msg = generator.generate_message(
            example_profile,
            scenario='job_seeker',
            custom_data=custom_data,
            message_type='connection'
        )

        print(f"\nTo: {connection_msg['recipient_name']}")
        print(f"Title: {connection_msg['recipient_title']}")
        print(f"Characters: {connection_msg['char_count']}/300")
        print(f"\n{connection_msg['message']}\n")

        # Generate direct message
        print("="*60)
        print("DIRECT MESSAGE (longer format):")
        print("="*60)

        direct_msg = generator.generate_message(
            example_profile,
            scenario='job_seeker',
            custom_data=custom_data,
            message_type='direct'
        )

        print(f"\nTo: {direct_msg['recipient_name']}")
        print(f"Characters: {direct_msg['char_count']}")
        print(f"\n{direct_msg['message']}\n")

        print("="*60)
        print("✓ AI message generation working!")
        print("="*60)

    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
