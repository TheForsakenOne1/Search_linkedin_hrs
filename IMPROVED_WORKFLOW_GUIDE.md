# 🚀 LinkedIn HR Finder - Improved Workflow Guide

## Overview

This improved n8n workflow simplifies LinkedIn HR contact discovery to just **entering a company name**. It automatically finds HR professionals, enriches their profiles, and generates personalized outreach messages including your projects.

## 🎯 Key Improvements

### What's New?

✅ **Simplified Input** - Just company name (vs. complex manual scraping)
✅ **Free API Sources** - Uses Google Custom Search API (100 free/day)
✅ **AI-Powered Messages** - GPT-4/Claude generates personalized messages
✅ **Project Integration** - Automatically includes your portfolio projects
✅ **Complete Profiles** - Name, title, location, LinkedIn URL
✅ **Dual Message Versions** - Short connection request + detailed follow-up
✅ **Multiple Export Formats** - JSON and CSV
✅ **No Browser Required** - All API-based (more reliable)

### Comparison with Old Workflow

| Feature | Old Workflow | New Improved Workflow |
|---------|--------------|----------------------|
| Input Required | Multiple fields + manual scraping | Just company name |
| Data Source | Selenium browser automation | Google Custom Search API + Proxycurl |
| Free Tier | Limited | 100 searches/day |
| Message Quality | Template-based | AI-personalized with projects |
| Reliability | Browser-dependent | API-based (99.9% uptime) |
| Setup Complexity | High (Chrome, Selenium, login) | Low (just API keys) |
| Profile Data | Basic | Enriched (optional) |

## 🔧 Setup Instructions

### Prerequisites

1. **n8n installed** (self-hosted or cloud)
2. **API Keys** (all have free tiers):
   - Google Custom Search API (required)
   - OpenAI API key OR Anthropic API key (required)
   - Proxycurl API key (optional, for enrichment)

### Step 1: Get Google Custom Search API Key (FREE - 100/day)

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project or select existing
3. Enable "Custom Search API"
4. Create credentials (API key)
5. Create a Custom Search Engine:
   - Go to [Programmable Search Engine](https://programmablesearchengine.google.com/create)
   - Sites to search: `linkedin.com/in/*`
   - Get your Search Engine ID (cx parameter)

**Free Quota:** 100 search queries per day

### Step 2: Get OpenAI API Key (PAY-AS-YOU-GO)

1. Go to [OpenAI Platform](https://platform.openai.com)
2. Sign up or log in
3. Navigate to API Keys
4. Create new secret key
5. Add $5-10 credit to your account

**Cost:** ~$0.01-0.03 per message (GPT-4 Turbo)

**Alternative: Anthropic (Claude)**
- Go to [Anthropic Console](https://console.anthropic.com)
- Similar process, similar pricing
- Update workflow to use Anthropic node instead

### Step 3: Get Proxycurl API Key (OPTIONAL - 10-15 free credits)

1. Go to [Proxycurl](https://nubela.co/proxycurl)
2. Sign up for free account
3. Get 10-15 free trial credits
4. Find API key in dashboard

**Usage:**
- Employee listing: 3 credits per employee
- Profile enrichment: 1 credit per profile
- Optional but recommended for detailed data

### Step 4: Import Workflow to n8n

1. Open n8n interface
2. Click "Import from File"
3. Select: `n8n_workflows/linkedin_hr_finder_improved.json`
4. Click "Import"

### Step 5: Configure Credentials in n8n

#### Google Custom Search API:
```
Name: Google Custom Search API
API Key: [your-api-key]
Search Engine ID: [your-cx-id]
```

#### OpenAI:
```
Name: OpenAI
API Key: [your-openai-api-key]
```

#### Proxycurl (Optional):
```
Name: Proxycurl API
API Key: [your-proxycurl-api-key]
```

## 📖 How to Use

### Basic Usage (Just Company Name!)

```bash
curl -X POST http://localhost:5678/webhook/linkedin-hr-finder \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "Google"
  }'
```

### Advanced Usage (Personalized)

```bash
curl -X POST http://localhost:5678/webhook/linkedin-hr-finder \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "Google",
    "max_results": 20,
    "your_name": "John Doe",
    "your_role": "Full-Stack Software Engineer",
    "your_experience": "5 years",
    "your_skills": "Python, React, Node.js, AWS, Docker, Kubernetes",
    "your_projects": [
      {
        "name": "E-Commerce Platform",
        "description": "Built scalable e-commerce platform serving 100K+ daily users with 99.9% uptime",
        "tech": "React, Node.js, MongoDB, Redis, AWS"
      },
      {
        "name": "AI Chatbot System",
        "description": "Developed intelligent customer service bot reducing support tickets by 40%",
        "tech": "Python, OpenAI GPT-4, FastAPI, PostgreSQL"
      },
      {
        "name": "Real-time Analytics Dashboard",
        "description": "Created real-time analytics dashboard processing 1M+ events per day",
        "tech": "React, D3.js, Apache Kafka, ClickHouse"
      }
    ]
  }'
```

### Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `company_name` | ✅ Yes | - | Target company name (e.g., "Google", "Microsoft") |
| `max_results` | No | 20 | Max number of profiles to find (10-50 recommended) |
| `your_name` | No | "Professional" | Your full name |
| `your_role` | No | "Software Engineer" | Your job title/role |
| `your_experience` | No | "5 years" | Years of experience |
| `your_skills` | No | "Full-stack development" | Comma-separated skills |
| `your_projects` | No | [] | Array of project objects (see example) |
| `search_method` | No | "google" | "google" or "proxycurl" |

## 📊 Output Format

The workflow generates two files and returns JSON response:

### JSON Output Example

```json
{
  "success": true,
  "company": "Google",
  "total_profiles": 15,
  "profiles": [
    {
      "name": "Jane Smith",
      "first_name": "Jane",
      "title": "Senior Technical Recruiter",
      "company": "Google",
      "location": "San Francisco, CA",
      "profile_url": "https://www.linkedin.com/in/janesmith",

      "your_name": "John Doe",
      "your_role": "Full-Stack Software Engineer",
      "your_experience": "5 years",
      "your_skills": "Python, React, Node.js, AWS",
      "your_projects": [...],

      "connection_request": "Hi Jane! Impressed by Google's innovative approach to talent acquisition. I'm a full-stack engineer with 5 years building scalable platforms. Would love to connect and explore opportunities!",

      "follow_up_message": "Hi Jane,\n\nThank you for connecting! I wanted to share a bit more about my background.\n\nI'm a Full-Stack Software Engineer with 5 years of experience building high-scale applications. Here are some highlights:\n\n• E-Commerce Platform: Built scalable platform serving 100K+ daily users with 99.9% uptime using React, Node.js, MongoDB, and AWS\n\n• AI Chatbot System: Developed intelligent customer service bot that reduced support tickets by 40% using Python, OpenAI GPT-4, and FastAPI\n\nI'm particularly interested in Google's innovative culture and would love to discuss how my experience with scalable systems and AI could contribute to your team.\n\nWould you be open to a brief call to explore potential opportunities?\n\nBest regards,\nJohn",

      "char_count_connection": 189,
      "char_count_followup": 724,
      "generated_at": "2025-01-15T10:30:00Z",
      "ai_provider": "openai"
    }
  ],
  "export_files": {
    "json": "linkedin_hr_Google_2025-01-15.json",
    "csv": "linkedin_hr_Google_2025-01-15.csv"
  }
}
```

### CSV Output

The CSV file includes these columns:
- name
- title
- company
- location
- profile_url
- connection_request
- follow_up_message
- char_count_connection
- char_count_followup
- generated_at

## 🎯 Workflow Architecture

### Flow Diagram

```
1. Webhook Input (Company Name)
   ↓
2. Parse Parameters
   ↓
3. Google Custom Search API ← Find LinkedIn HR profiles
   ↓
4. Parse Search Results ← Extract profile data
   ↓
5. Normalize Profile Data ← Standardize fields
   ↓
6. Filter HR Roles ← Keep only HR/Talent/Recruiting
   ↓
7. AI Message Generation ← GPT-4/Claude personalization
   ↓
8. Format Final Output ← Combine all data
   ↓
9. Aggregate Results ← Collect all profiles
   ↓
10. Export (JSON + CSV) ← Save files
    ↓
11. Webhook Response ← Return success
```

### Key Nodes Explained

#### 1. Google Custom Search
- Searches LinkedIn for HR professionals at target company
- Uses Boolean operators: `site:linkedin.com/in + company + (recruiter OR "talent acquisition" OR "HR manager")`
- Returns up to 10 results per API call
- **Free tier: 100 searches/day**

#### 2. Parse Google Results
- Extracts profile URLs from search results
- Parses names and job titles from snippets
- Filters for HR-related keywords

#### 3. Proxycurl Enrichment (Optional)
- Gets detailed profile data if credits available
- Costs 1 credit per profile
- Disabled by default to conserve credits

#### 4. AI Message Generation
- Uses GPT-4 or Claude to create personalized messages
- References the person's role, company, location
- Highlights your relevant projects
- Creates TWO versions:
  - **Short**: Connection request (<300 chars)
  - **Long**: Follow-up message with project details

#### 5. Export
- Saves complete data to JSON and CSV
- Files auto-named with company and date
- Includes all profile data + messages

## 💡 Best Practices

### API Quota Management

**Google Custom Search (100/day):**
- Process 5-10 companies per day max
- Use `max_results: 10-20` to conserve quota
- Reset is at midnight Pacific Time

**OpenAI GPT-4:**
- Cost: ~$0.01-0.03 per message
- Budget: $10 = ~300-1000 messages
- Use GPT-4-turbo (cheaper, faster)

**Proxycurl (10-15 free credits):**
- Use sparingly for enrichment
- Employee listing: 3 credits per employee
- Top up $10 for 1000 credits if needed

### Message Quality Tips

1. **Provide detailed project descriptions**
   - Include metrics (users, performance, impact)
   - Specify technologies used
   - Highlight achievements

2. **Keep projects relevant**
   - Match projects to target company's industry
   - Emphasize skills they're likely hiring for

3. **Review and customize**
   - AI messages are good but review them
   - Add personal touches
   - Adjust tone for company culture

### LinkedIn Best Practices

1. **Connection Limits**
   - LinkedIn allows ~100 weekly connection requests
   - Don't send all at once
   - Spread over several days

2. **Personalization**
   - Always review AI-generated messages
   - Add company-specific details
   - Mention mutual connections if any

3. **Follow-up Timing**
   - Send follow-up 24-48 hours after connection accepted
   - Reference something from their profile
   - Keep it conversational

## 🔍 Advanced Configuration

### Using Proxycurl Instead of Google

To use Proxycurl's Employee Listing API instead of Google:

1. Enable the "Proxycurl: Get Employee List" node
2. Disable the "Google: Search LinkedIn Profiles" node
3. Update the connection from "Parse Input" to "Proxycurl"
4. Set `search_method: "proxycurl"` in request

**Note:** Costs 3 credits per employee, more expensive but more accurate.

### Customizing AI Prompts

Edit the AI node prompt to change message style:

- **More formal**: Add "Use professional, formal tone"
- **More casual**: Add "Use friendly, conversational tone"
- **Industry-specific**: Add "Focus on [industry] experience"
- **Shorter messages**: Reduce max character limits

### Adding Email Enrichment

To find email addresses (requires additional API):

1. Add Hunter.io or Clearbit node after profile normalization
2. Pass name + company domain
3. Costs: Hunter.io has 50 free searches/month

### Batch Processing Multiple Companies

Create a parent workflow:

```json
{
  "companies": ["Google", "Microsoft", "Amazon", "Meta"],
  "batch_size": 10
}
```

Loop through companies with delay between each to respect API limits.

## 🐛 Troubleshooting

### "No results found"

**Possible causes:**
1. Company name spelling - try variations
2. No HR on public LinkedIn - try larger company
3. API quota exceeded - wait for reset

**Solutions:**
- Verify company name matches LinkedIn company page
- Try generic search without company filter
- Check API quota in Google Cloud Console

### "AI message generation failed"

**Possible causes:**
1. API key invalid or expired
2. Insufficient credits/quota
3. Request timeout

**Solutions:**
- Verify API key in credentials
- Check OpenAI/Anthropic account balance
- Increase timeout in HTTP node settings

### "Google Custom Search returns 403"

**Possible causes:**
1. Daily quota (100) exceeded
2. API key invalid
3. Custom Search Engine misconfigured

**Solutions:**
- Wait until midnight PT for quota reset
- Verify API key has Custom Search API enabled
- Check Search Engine ID (cx parameter)

### "Messages are too generic"

**Possible causes:**
1. Missing your_projects parameter
2. Insufficient project details
3. AI prompt needs tuning

**Solutions:**
- Always include detailed projects array
- Add metrics and specific tech stacks
- Customize AI prompt for your industry

## 💰 Cost Breakdown

### Free Tier (Recommended for Testing)

| Service | Free Tier | Cost After |
|---------|-----------|------------|
| Google Custom Search | 100 searches/day | $5 per 1,000 queries |
| Proxycurl | 10-15 credits | $0.01 per credit |
| OpenAI GPT-4 Turbo | None (pay-as-you-go) | $0.01 per 1K input tokens |
| Anthropic Claude | None (pay-as-you-go) | $0.015 per 1K input tokens |

### Cost Estimate for 100 Profiles

| Item | Quantity | Unit Cost | Total |
|------|----------|-----------|-------|
| Google searches | 10 searches | Free (under 100/day) | $0.00 |
| AI message generation | 100 messages | $0.02 each | $2.00 |
| Proxycurl enrichment (optional) | 100 profiles | $0.01 each | $1.00 |
| **Total** | | | **$2-3** |

**Monthly budget for regular use:** $20-50 (500-1000 contacts)

## 📝 Example Use Cases

### Use Case 1: Job Seeker

```json
{
  "company_name": "Stripe",
  "max_results": 15,
  "your_name": "Sarah Chen",
  "your_role": "Backend Engineer",
  "your_experience": "7 years",
  "your_skills": "Go, Python, Kubernetes, PostgreSQL, gRPC",
  "your_projects": [
    {
      "name": "Payment Processing System",
      "description": "Built distributed payment system processing $50M+ annually with 99.99% uptime",
      "tech": "Go, PostgreSQL, Redis, Kafka, Kubernetes"
    },
    {
      "name": "Microservices Architecture Migration",
      "description": "Led migration from monolith to microservices for 100+ engineers",
      "tech": "Go, gRPC, Kubernetes, Istio, Prometheus"
    }
  ]
}
```

### Use Case 2: Freelancer Looking for Clients

```json
{
  "company_name": "Shopify",
  "max_results": 20,
  "your_name": "Mike Rodriguez",
  "your_role": "Full-Stack Developer & Consultant",
  "your_experience": "8 years",
  "your_skills": "React, Node.js, AWS, E-commerce, Shopify Apps",
  "your_projects": [
    {
      "name": "Shopify App Development",
      "description": "Built 5+ successful Shopify apps with 10K+ active merchants",
      "tech": "React, Node.js, Shopify API, PostgreSQL"
    },
    {
      "name": "Custom E-commerce Solutions",
      "description": "Delivered custom integrations for 50+ e-commerce businesses",
      "tech": "Shopify, WooCommerce, Stripe, AWS Lambda"
    }
  ]
}
```

### Use Case 3: Career Transitioner

```json
{
  "company_name": "OpenAI",
  "max_results": 10,
  "your_name": "Alex Kumar",
  "your_role": "ML Engineer (Transitioning from Backend)",
  "your_experience": "6 years backend, 1 year ML",
  "your_skills": "Python, PyTorch, TensorFlow, NLP, FastAPI, Docker",
  "your_projects": [
    {
      "name": "LLM Fine-tuning Pipeline",
      "description": "Built automated pipeline for fine-tuning open-source LLMs on custom datasets",
      "tech": "Python, PyTorch, HuggingFace, MLflow, Kubernetes"
    },
    {
      "name": "Sentiment Analysis API",
      "description": "Deployed production ML API processing 1M+ requests/day",
      "tech": "Python, TensorFlow, FastAPI, Redis, AWS SageMaker"
    }
  ]
}
```

## 🚀 Next Steps

### After Running the Workflow

1. **Review Results**
   - Open the JSON/CSV file
   - Review profile matches
   - Check message quality

2. **Customize Messages**
   - Add personal touches
   - Reference specific company initiatives
   - Mention mutual connections

3. **Send Connection Requests**
   - Use the short "connection_request" version
   - Send 10-20 per day max
   - Track acceptance rate

4. **Follow Up**
   - Use "follow_up_message" after they accept
   - Wait 24-48 hours
   - Keep it conversational

5. **Track Results**
   - Monitor response rates
   - A/B test different message styles
   - Iterate on project descriptions

### Scaling Up

Once you've tested and refined:

1. **Batch Processing**: Process multiple companies
2. **Auto-scheduling**: Set up cron job or n8n scheduler
3. **CRM Integration**: Connect to HubSpot, Salesforce, etc.
4. **Analytics**: Track conversion rates, response times
5. **A/B Testing**: Test different message templates

## 📚 Additional Resources

- [n8n Documentation](https://docs.n8n.io)
- [Google Custom Search API](https://developers.google.com/custom-search/v1/overview)
- [Proxycurl API Docs](https://nubela.co/proxycurl/docs)
- [OpenAI API Docs](https://platform.openai.com/docs)
- [Anthropic API Docs](https://docs.anthropic.com)

## 🤝 Support

For issues or questions:
1. Check troubleshooting section above
2. Review n8n logs for errors
3. Open an issue on GitHub
4. Join n8n community forum

---

**Happy Networking! 🎯**

Remember: Quality over quantity. Personalized outreach always wins.
