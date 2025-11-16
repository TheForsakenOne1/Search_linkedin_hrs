# n8n LinkedIn HR Workflows

This directory contains n8n workflow templates for automated LinkedIn HR contact discovery and outreach.

## 📁 Available Workflows

### 1. **linkedin_hr_finder_improved.json** ⭐ RECOMMENDED

**The best all-in-one solution** - Just enter company name and get everything!

✅ **Simplest to use** - Just company name input
✅ **Free tier available** - Google Custom Search API (100/day)
✅ **AI-powered** - GPT-4/Claude message personalization
✅ **Project integration** - Auto-includes your portfolio
✅ **Complete output** - Profile + personalized messages

**Use this if:** You want the easiest, most comprehensive solution

📖 **Full Guide:** [IMPROVED_WORKFLOW_GUIDE.md](../IMPROVED_WORKFLOW_GUIDE.md)

**Quick Start:**
```bash
curl -X POST http://localhost:5678/webhook/linkedin-hr-finder \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "Google",
    "your_name": "Your Name",
    "your_role": "Software Engineer",
    "your_skills": "Python, React, AWS",
    "your_projects": [
      {
        "name": "E-Commerce Platform",
        "description": "Built platform serving 100K users",
        "tech": "React, Node.js, AWS"
      }
    ]
  }'
```

---

### 2. **linkedin_hr_messaging_workflow.json**

**Template-based messaging** - Original workflow with pre-defined message templates.

✅ Simple message templates
✅ No AI required
✅ Fast execution
❌ Less personalization
❌ Requires pre-scraped data

**Use this if:** You want simple templates without AI costs

---

### 3. **linkedin_ai_agent_workflow.json**

**Python-powered AI agent** - Runs complete Python scraper + AI workflow.

✅ Full Python control
✅ AI message generation
✅ Complete automation
❌ Requires Python environment
❌ Needs Selenium setup
❌ LinkedIn login required

**Use this if:** You want full Python-based automation

---

## 🎯 Which Workflow Should You Use?

| Need | Recommended Workflow |
|------|---------------------|
| **Easiest setup** | linkedin_hr_finder_improved.json |
| **Best personalization** | linkedin_hr_finder_improved.json |
| **No AI costs** | linkedin_hr_messaging_workflow.json |
| **Full automation** | linkedin_ai_agent_workflow.json |
| **Free tier** | linkedin_hr_finder_improved.json |
| **Most reliable** | linkedin_hr_finder_improved.json |

## 🚀 Quick Setup

### For linkedin_hr_finder_improved.json (RECOMMENDED)

1. **Get API Keys (all have free tiers):**
   - Google Custom Search API: [Get here](https://console.cloud.google.com)
   - OpenAI API: [Get here](https://platform.openai.com)

2. **Import to n8n:**
   - Open n8n
   - Import workflow file
   - Add credentials

3. **Test:**
   ```bash
   curl -X POST http://localhost:5678/webhook/linkedin-hr-finder \
     -H "Content-Type: application/json" \
     -d '{"company_name": "Google"}'
   ```

4. **Get Results:**
   - JSON with all profiles
   - Personalized messages
   - Ready to send!

## 📖 Documentation

- **Improved Workflow:** See [IMPROVED_WORKFLOW_GUIDE.md](../IMPROVED_WORKFLOW_GUIDE.md)
- **General n8n Setup:** See [N8N_INTEGRATION_GUIDE.md](../N8N_INTEGRATION_GUIDE.md)
- **Main README:** See [README.md](../README.md)

## 💡 Tips

1. **Start with improved workflow** - It's the easiest and most powerful
2. **Test with small companies first** - Try 10-20 results
3. **Review messages before sending** - AI is good but review adds value
4. **Track your quota** - Google: 100/day, plan accordingly
5. **Personalize further** - Add company-specific details to messages

## 🆘 Need Help?

1. Check the [IMPROVED_WORKFLOW_GUIDE.md](../IMPROVED_WORKFLOW_GUIDE.md) for detailed setup
2. Review [Troubleshooting section](../IMPROVED_WORKFLOW_GUIDE.md#-troubleshooting)
3. Open an issue on GitHub

---

**Happy Automating! 🎉**
