# n8n Integration Guide

Complete guide for integrating the LinkedIn HR scraper with n8n for automated message generation and workflow management.

## Table of Contents
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Workflow Options](#workflow-options)
- [Usage](#usage)
- [Advanced Configuration](#advanced-configuration)
- [Troubleshooting](#troubleshooting)

## Overview

This integration provides two workflow options:

1. **Python-first Workflow** (Recommended)
   - Scrape → Generate → Export workflow file
   - Import into n8n for review and sending
   - Maximum control and safety

2. **n8n-native Workflow**
   - Trigger n8n from scraper
   - Generate messages in n8n
   - Auto-send or manual review

## Prerequisites

- Python 3.8+ with all dependencies installed
- n8n installed (Docker or self-hosted)
- LinkedIn account configured in `.env`
- (Optional) OpenAI/Anthropic API key for AI-enhanced messages

### Installing n8n

**Option 1: Docker (Recommended)**
```bash
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

**Option 2: npm**
```bash
npm install n8n -g
n8n start
```

Access n8n at: `http://localhost:5678`

## Setup

### Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Start the Message Service API

The message service provides an HTTP API for n8n to generate messages:

```bash
python message_service.py
```

The API will run on `http://localhost:5000`

**Test the API:**
```bash
curl http://localhost:5000/health
```

### Step 3: Import n8n Workflow

1. Open n8n at `http://localhost:5678`
2. Click "Add workflow" or "Import from file"
3. Select `n8n_workflows/linkedin_hr_messaging_workflow.json`
4. Click "Import"

The workflow will be ready to use!

## Workflow Options

### Option 1: Python-First Workflow (Recommended)

**Best for:** Safety, control, compliance

This workflow generates all messages locally, then imports them into n8n for review.

**Steps:**

1. **Run the complete workflow in export mode:**
   ```bash
   python complete_workflow.py --company "Google" --export-only
   ```

2. **Files generated:**
   - `output/linkedin_hr_Google_<timestamp>.json` - Scraped profiles
   - `output/messages_Google_job_seeker.json` - Generated messages
   - `output/workflow_Google.json` - Complete workflow file

3. **Import into n8n:**
   - Open your n8n workflow
   - Update the "Read Scraper Output" node with the workflow file path
   - Execute the workflow to review messages
   - Manually send approved messages

**Example:**
```bash
# Scrape Google, generate job seeker messages, export only
python complete_workflow.py \
  --company "Google" \
  --scenario job_seeker \
  --role "Software Engineer" \
  --years "5" \
  --skills "Python, React, AWS" \
  --export-only
```

### Option 2: n8n-Native Workflow

**Best for:** Automation, batch processing

This workflow uses n8n to orchestrate the entire process.

**Steps:**

1. **Start the message service:**
   ```bash
   python message_service.py
   ```

2. **Configure the n8n workflow:**
   - Open the workflow in n8n
   - Set the webhook URL in the trigger node
   - Configure the message service URL (default: `http://localhost:5000`)

3. **Trigger the workflow:**

   **Option A: Via Webhook**
   ```bash
   curl -X POST http://localhost:5678/webhook/linkedin-hr-outreach \
     -H "Content-Type: application/json" \
     -d '{
       "company": "Google",
       "scenario": "job_seeker",
       "custom_data": {
         "your_role": "Software Engineer",
         "years": "5",
         "skills": "Python, React, AWS"
       }
     }'
   ```

   **Option B: Via Python**
   ```python
   import requests

   response = requests.post(
       'http://localhost:5678/webhook/linkedin-hr-outreach',
       json={
           'company': 'Google',
           'scenario': 'job_seeker',
           'custom_data': {
               'your_role': 'Software Engineer',
               'years': '5',
               'skills': 'Python, React, AWS'
           }
       }
   )
   print(response.json())
   ```

4. **Review and send in n8n:**
   - Messages appear in the workflow
   - Review each message
   - Approve or reject
   - Send to LinkedIn

## Usage

### Complete Workflow Script

The `complete_workflow.py` script provides the easiest way to use all features:

**Interactive Mode:**
```bash
python complete_workflow.py
```

**CLI Mode:**
```bash
# Export for n8n (safest)
python complete_workflow.py --company "Microsoft" --export-only

# Manual review and send
python complete_workflow.py --company "Amazon" --scenario networking

# With custom data
python complete_workflow.py \
  --company "Apple" \
  --scenario job_seeker \
  --role "Product Manager" \
  --years "7" \
  --skills "Product Strategy, User Research" \
  --export-only
```

### Message Scenarios

Four built-in scenarios are available:

1. **job_seeker** - Looking for job opportunities
2. **networking** - Professional connection
3. **recruiter_outreach** - Offering candidates
4. **informational_interview** - Seeking career advice

**Example for each scenario:**

```bash
# Job Seeker
python complete_workflow.py --company "Google" --scenario job_seeker --export-only

# Networking
python complete_workflow.py --company "Microsoft" --scenario networking --export-only

# Recruiter
python complete_workflow.py --company "Amazon" --scenario recruiter_outreach --export-only

# Informational Interview
python complete_workflow.py --company "Apple" --scenario informational_interview --export-only
```

### Message Service API Endpoints

The message service provides several REST endpoints:

**1. Health Check**
```bash
GET http://localhost:5000/health
```

**2. List Scenarios**
```bash
GET http://localhost:5000/scenarios
```

**3. Generate Single Message**
```bash
POST http://localhost:5000/generate-message
Content-Type: application/json

{
  "profile": {
    "name": "Jane Smith",
    "title": "Senior HR Manager at Google",
    "location": "San Francisco",
    "profile_url": "https://linkedin.com/in/janesmith"
  },
  "scenario": "job_seeker",
  "custom_data": {
    "your_role": "Software Engineer",
    "years": "5",
    "skills": "Python, React, AWS"
  }
}
```

**4. Generate Bulk Messages**
```bash
POST http://localhost:5000/generate-bulk
Content-Type: application/json

{
  "profiles": [...],
  "scenario": "job_seeker",
  "custom_data": {...}
}
```

**5. Generate from File**
```bash
POST http://localhost:5000/generate-from-file
Content-Type: application/json

{
  "file_path": "/path/to/linkedin_hr_results.json",
  "scenario": "job_seeker",
  "custom_data": {...},
  "output_file": "/path/to/output.json"
}
```

## Advanced Configuration

### AI-Enhanced Messages (OpenAI/Anthropic)

To enable AI-enhanced message generation:

1. **Get an API key:**
   - OpenAI: https://platform.openai.com/api-keys
   - Anthropic: https://console.anthropic.com/

2. **Update `.env`:**
   ```env
   USE_AI_MESSAGES=True
   OPENAI_API_KEY=your-key-here
   # OR
   ANTHROPIC_API_KEY=your-key-here
   ```

3. **Modify message_generator.py:**
   ```python
   # Enable AI in generator
   generator = MessageGenerator(use_ai=True, api_key=os.getenv('OPENAI_API_KEY'))
   ```

### Custom Message Templates

Edit `message_generator.py` to add custom templates:

```python
self.templates['custom_scenario'] = {
    'greeting': ['Hi {name}', ...],
    'introduction': ['Your custom intro...'],
    'value_proposition': ['Your value prop...'],
    'call_to_action': ['Your CTA...'],
    'closing': ['Your closing...']
}
```

### n8n Workflow Customization

The n8n workflow can be customized:

1. **Add LinkedIn API integration:**
   - Get LinkedIn API credentials
   - Add LinkedIn OAuth2 node
   - Connect to "Send to LinkedIn" node

2. **Add email notifications:**
   - Add Email node
   - Configure SMTP settings
   - Send summary when workflow completes

3. **Add database logging:**
   - Add PostgreSQL/MySQL node
   - Log all sent messages
   - Track response rates

4. **Add Slack notifications:**
   - Add Slack node
   - Post messages to channel
   - Track team activity

## Workflow Architecture

```
┌─────────────────────────────────────────────────────────┐
│                Python Workflow                          │
│                                                         │
│  Scraper → Message Generator → Export Files            │
│     ↓              ↓                 ↓                  │
│  Profiles     Messages        Workflow JSON            │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│                   n8n Workflow                          │
│                                                         │
│  Import Files → Review → Approve → Send                │
│                                        ↓                │
│                                   LinkedIn API          │
└─────────────────────────────────────────────────────────┘
```

## Safety & Best Practices

### DO's ✅

- ✅ Use `--export-only` mode for initial testing
- ✅ Review ALL messages before sending
- ✅ Add delays between messages (15-30 seconds minimum)
- ✅ Start with small batches (5-10 messages)
- ✅ Personalize messages with custom data
- ✅ Use a secondary LinkedIn account for testing
- ✅ Keep logs of all sent messages
- ✅ Respect LinkedIn's daily message limits

### DON'Ts ❌

- ❌ Don't use `--auto-send` without testing
- ❌ Don't send the same message to everyone
- ❌ Don't send more than 50 messages per day
- ❌ Don't send messages too quickly (rate limiting)
- ❌ Don't use your primary LinkedIn account
- ❌ Don't send unsolicited bulk messages (spam)
- ❌ Don't ignore LinkedIn's Terms of Service
- ❌ Don't send without reviewing message quality

### Rate Limits

LinkedIn has rate limits to prevent spam:

- **Connection requests:** ~100-200 per week
- **Messages:** ~50-100 per day
- **Profile views:** ~100 per day
- **Searches:** ~30 per hour

**Our default settings:**
- 15-30 seconds between messages
- Max 50 results per search
- Manual review encouraged

## Troubleshooting

### Common Issues

**1. Message service not starting**
```bash
# Check if port 5000 is in use
lsof -i :5000

# Use different port
MESSAGE_SERVICE_PORT=5001 python message_service.py
```

**2. n8n can't connect to message service**
```bash
# Check if service is running
curl http://localhost:5000/health

# Check Docker network (if using Docker)
docker network inspect bridge
```

**3. Messages too long for LinkedIn**
- LinkedIn connection notes: 300 characters max
- LinkedIn messages: 2000 characters recommended
- Edit templates in `message_generator.py`

**4. Workflow file not found in n8n**
- Use absolute paths in n8n nodes
- Check file permissions
- Verify output directory exists

**5. LinkedIn blocking/rate limiting**
- Increase delays between messages
- Reduce daily message count
- Use different account
- Wait 24-48 hours before retrying

### Debug Mode

Enable debug logging:

```bash
# Set in .env
DEBUG=True

# Or set environment variable
export DEBUG=True
python complete_workflow.py --company "Google" --export-only
```

### Logs

Check logs for errors:

```bash
# Python service logs
tail -f message_service.log

# n8n logs
docker logs -f n8n  # If using Docker
```

## Examples

### Example 1: Basic Job Search Outreach

```bash
# 1. Scrape and generate
python complete_workflow.py \
  --company "Google" \
  --scenario job_seeker \
  --role "Software Engineer" \
  --years "5" \
  --skills "Python, Kubernetes, React" \
  --export-only

# 2. Review generated files
cat output/workflow_Google.json

# 3. Import to n8n and review
# 4. Send approved messages
```

### Example 2: Networking Campaign

```bash
# Target multiple companies
for company in "Google" "Microsoft" "Amazon" "Meta"; do
  python complete_workflow.py \
    --company "$company" \
    --scenario networking \
    --industry "technology" \
    --export-only
done

# Import all workflow files to n8n
# Review and send in batches
```

### Example 3: Using n8n Webhook

```python
import requests

companies = ["Google", "Microsoft", "Amazon"]

for company in companies:
    response = requests.post(
        'http://localhost:5678/webhook/linkedin-hr-outreach',
        json={
            'company': company,
            'scenario': 'job_seeker',
            'custom_data': {
                'your_role': 'Data Scientist',
                'years': '3',
                'skills': 'Machine Learning, Python, SQL'
            }
        }
    )
    print(f"{company}: {response.status_code}")
```

## Next Steps

1. **Test the workflow:**
   ```bash
   python complete_workflow.py --company "Google" --export-only
   ```

2. **Review generated messages:**
   ```bash
   cat output/workflow_Google.json
   ```

3. **Import to n8n and refine**

4. **Start with small batches (5-10 messages)**

5. **Monitor results and iterate**

## Resources

- [n8n Documentation](https://docs.n8n.io/)
- [LinkedIn API Documentation](https://docs.microsoft.com/en-us/linkedin/)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Flask Documentation](https://flask.palletsprojects.com/)

## Support

If you encounter issues:

1. Check this guide thoroughly
2. Review the troubleshooting section
3. Check generated log files
4. Open an issue on GitHub with:
   - Error message
   - Steps to reproduce
   - Your configuration (sanitized)

---

**Happy Networking! 🚀**

Remember: Always use responsibly and respect LinkedIn's Terms of Service.
