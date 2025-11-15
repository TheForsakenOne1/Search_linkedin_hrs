# Contributing to LinkedIn HR Scraper

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Code Quality Standards

### 1. Input Validation

All user inputs MUST be validated:

```python
from validation import validate_company_name, validate_or_raise

# Validate and raise exception if invalid
validate_or_raise(validate_company_name, company_name)

# Or handle errors manually
is_valid, error = validate_company_name(company_name)
if not is_valid:
    print(f"Error: {error}")
    return
```

### 2. Error Handling

Use try-except blocks with specific exceptions:

```python
try:
    result = risky_operation()
except ValidationError as e:
    logger.error(f"Validation failed: {e}")
except Exception as e:
    logger.error(f"Unexpected error: {e}", exc_info=True)
```

### 3. Logging

Use the logging system instead of print statements:

```python
from logger import get_logger

logger = get_logger(__name__)
logger.info("Starting operation")
logger.error("Operation failed", exc_info=True)
```

### 4. Documentation

All functions must have docstrings:

```python
def my_function(param1, param2):
    """
    Brief description of function

    Args:
        param1 (type): Description of param1
        param2 (type): Description of param2

    Returns:
        type: Description of return value

    Raises:
        ExceptionType: When this exception is raised
    """
    pass
```

### 5. Type Hints (Encouraged)

Add type hints for better code clarity:

```python
def process_profiles(profiles: list, max_count: int = 50) -> dict:
    """Process profiles and return summary"""
    pass
```

### 6. Testing

Add tests for new functionality:

```python
# tests.py
class TestNewFeature(unittest.TestCase):
    def test_basic_functionality(self):
        result = my_new_function("test")
        self.assertEqual(result, expected_value)
```

## Development Workflow

### 1. Setup Development Environment

```bash
# Clone the repository
git clone <repo-url>
cd Search_linkedin_hrs

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
# Edit .env with your test credentials
```

### 2. Run Tests Before Committing

```bash
# Run full test suite
python tests.py

# Run demo to verify functionality
python demo.py --quick

# Validate environment
python utils.py --check
```

### 3. Code Style

Follow PEP 8 guidelines:

- Use 4 spaces for indentation
- Maximum line length: 100 characters
- Use descriptive variable names
- Add blank lines between logical sections

```python
# Good
def get_hr_profiles(company_name, max_results=50):
    """Get HR profiles from company"""
    validate_or_raise(validate_company_name, company_name)

    profiles = []
    # ... implementation
    return profiles

# Bad
def f(c,m=50):
    p=[]
    return p
```

### 4. Git Commit Messages

Use clear, descriptive commit messages:

```
Add feature: AI-powered message generation

- Implemented OpenAI integration
- Added fallback to templates
- Updated documentation

Fixes #123
```

Format:
- First line: Brief summary (50 chars max)
- Blank line
- Detailed description if needed
- Reference issues with #number

### 5. Pull Request Process

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Run tests: `python tests.py`
5. Commit with clear messages
6. Push to your fork
7. Create pull request with description

## Project Structure Guidelines

### Where to Add Code

**New Validation:**
- Add to `validation.py`
- Add test to `tests.py` (TestValidation class)

**New Message Scenario:**
- Add to `message_generator.py` templates
- Add to `ai_message_generator.py` prompts
- Update `config.MESSAGE_SCENARIOS`

**New Export Format:**
- Add method to `data_exporter.py`
- Add test to `tests.py` (TestDataExport class)

**New Utility:**
- Add to `utils.py` or create new file
- Document in README.md

**New Configuration:**
- Add to `config.py`
- Add to `.env.example`
- Document in README.md

## Common Contribution Areas

### 1. Adding New HR Keywords

Edit `config.py`:

```python
HR_KEYWORDS = [
    'Human Resources',
    # ... existing keywords
    'Your New Keyword',  # Add here
]
```

### 2. Adding New Message Scenario

Add to `message_generator.py`:

```python
'your_scenario': {
    'greeting': ['Hi {name}', ...],
    'introduction': [...],
    'value_proposition': [...],
    'call_to_action': [...],
    'closing': [...]
}
```

Update `config.py`:

```python
MESSAGE_SCENARIOS = [
    'job_seeker',
    # ... existing scenarios
    'your_scenario',  # Add here
]
```

### 3. Improving AI Prompts

Edit `ai_message_generator.py` `_build_prompt()` method:

```python
def _build_prompt(self, profile, scenario, custom_data, message_type):
    # Modify prompt construction
    prompt = f"""
    Your improved prompt here...
    """
    return prompt
```

### 4. Adding New Validators

Add to `validation.py`:

```python
def validate_your_input(value):
    """
    Validate your input type

    Args:
        value: Value to validate

    Returns:
        tuple: (is_valid, error_message)
    """
    if not value:
        return False, "Value cannot be empty"

    # Your validation logic

    return True, None
```

Add test to `tests.py`:

```python
def test_your_input_validation(self):
    """Test your input validation"""
    self.assertTrue(validate_your_input("valid")[0])
    self.assertFalse(validate_your_input("")[0])
```

## Testing Guidelines

### Unit Tests

- Test one thing per test
- Use descriptive test names
- Include positive and negative cases
- Don't require LinkedIn credentials

```python
def test_company_name_validation_accepts_valid_names(self):
    """Test that valid company names are accepted"""
    valid_names = ["Google", "Microsoft Inc.", "Company & Co."]
    for name in valid_names:
        is_valid, _ = validate_company_name(name)
        self.assertTrue(is_valid, f"{name} should be valid")
```

### Integration Tests

For features that require LinkedIn:
- Mark as integration tests
- Document setup requirements
- Make optional/skippable

## Documentation Guidelines

### Update README.md When:

- Adding new features
- Changing usage patterns
- Adding new dependencies
- Changing configuration

### Update Docstrings When:

- Changing function parameters
- Changing return values
- Adding exceptions
- Modifying behavior

### Add Examples When:

- Adding complex features
- Creating new workflows
- Introducing new APIs

## Security Guidelines

### Never Commit:

- API keys
- Passwords
- .env files
- Personal LinkedIn credentials
- Session tokens

### Always:

- Use environment variables for secrets
- Validate all user inputs
- Sanitize file paths
- Check URL schemes
- Escape special characters

## Performance Guidelines

### Do:

- Add delays between LinkedIn requests
- Respect rate limits
- Cache when appropriate
- Use bulk operations

### Don't:

- Make unnecessary API calls
- Scrape excessively
- Ignore rate limit errors
- Skip error handling for speed

## Questions?

- Check existing issues on GitHub
- Read documentation thoroughly
- Run demo.py to understand features
- Look at example_usage.py for patterns

## Code of Conduct

- Be respectful and professional
- Help others learn
- Provide constructive feedback
- Follow ethical scraping practices
- Respect LinkedIn's Terms of Service

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to make LinkedIn HR Scraper better! 🚀
