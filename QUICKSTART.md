# Quick Start Guide - LinkedIn HR Finder

Get the AI-powered LinkedIn HR Finder running in 10 minutes!

## What You're Building

A beautiful web app that:
- Searches LinkedIn for HR contacts at any company
- Generates personalized AI messages
- Uses free APIs (Google Search + OpenAI)
- Has a Stripe-style professional UI

---

## Step 1: Set Up n8n Workflow (3 minutes)

### Using n8n Cloud (Recommended - Free)

1. Go to **https://n8n.io** → Sign up for free account
2. Create a new workflow
3. Click "..." → **"Import from File"**
4. Select: `n8n_workflows/linkedin_hr_finder_improved.json`
5. Click **"Import"**

### Using Self-hosted n8n

```bash
npx n8n
```

Then go to http://localhost:5678 and import the workflow.

---

## Step 2: Get API Keys (4 minutes)

### ✅ Google Custom Search (100/day FREE)

**Get API Key:**
1. Go to https://console.cloud.google.com/apis/credentials
2. Click **"Create Credentials"** → **"API Key"**
3. Copy the key

**Get Search Engine ID:**
1. Go to https://cse.google.com/cse/all
2. Click **"Add"** to create a search engine
3. Under "Sites to search": Select **"Search the entire web"**
4. Create and copy the **Search Engine ID**

**Add to n8n:**
1. Find the **"Google: Search LinkedIn Profiles"** node in your workflow
2. Click on it → **"Credentials"**
3. Add your API Key and Search Engine ID

### ✅ OpenAI (Pay-as-you-go, ~$0.03 per profile)

1. Get API key: https://platform.openai.com/api-keys
2. Click **"Create new secret key"**
3. Copy the key
4. In n8n, find the **"OpenAI: Generate Messages"** nodes
5. Add your OpenAI credential

### ✅ Proxycurl (Optional - 10 FREE credits)

1. Sign up: https://nubela.co/proxycurl
2. Get API key from dashboard
3. Add to the **"Proxycurl: Enrich Profiles"** node in n8n

---

## Step 3: Activate n8n Workflow (1 minute)

1. In n8n, click the **"Webhook: Start Search"** node
2. Copy the **Production Webhook URL**:
   ```
   n8n Cloud: https://yourname.app.n8n.cloud/webhook/linkedin-hr-finder
   Self-hosted: http://localhost:5678/webhook/linkedin-hr-finder
   ```

3. **⚠️ CRITICAL**: Toggle the workflow to **"Active"** (top-right corner switch)

---

## Step 4: Set Up the Next.js UI (2 minutes)

### Local Development

```bash
cd linkedin-hr-finder-ui

# Create environment file
cp .env.example .env.local

# Add your n8n webhook URL
echo "N8N_WEBHOOK_URL=https://yourname.app.n8n.cloud/webhook/linkedin-hr-finder" > .env.local

# Install dependencies
npm install

# Start development server
npm run dev
```

Open **http://localhost:3000** in your browser!

### Deploy to Vercel (Alternative)

1. Push code to GitHub
2. Go to **https://vercel.com** → Sign in with GitHub
3. Click **"Add New"** → **"Project"**
4. Import your `Search_linkedin_hrs` repository
5. Configure:
   - **Root Directory**: `linkedin-hr-finder-ui`
   - **Environment Variable**:
     - Name: `N8N_WEBHOOK_URL`
     - Value: Your webhook URL from Step 3
6. Click **"Deploy"**
7. Visit your live URL! 🎉

---

## Step 5: Test It! (2 minutes)

### Test 1: Direct Webhook Test

```bash
curl -X POST https://yourname.app.n8n.cloud/webhook/linkedin-hr-finder \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "Google",
    "max_results": 3,
    "your_name": "John Doe",
    "your_role": "Software Engineer",
    "your_experience": "3 years",
    "your_skills": "React, Python, AWS",
    "your_projects": [
      {
        "name": "E-Commerce Platform",
        "description": "Built a scalable platform serving 50K users",
        "tech": "React, Node.js, MongoDB"
      }
    ]
  }'
```

You should get a JSON response with LinkedIn profiles and AI-generated messages!

### Test 2: Use the Beautiful UI

1. Open http://localhost:3000 (or your Vercel URL)
2. Fill in the search form:
   - **Company**: "Google"
   - **Max Results**: 5
   - **Your Name**: Your name
   - **Your Role**: "Software Engineer"
   - **Skills**: "React, Python, AWS"
   - Add a project or two

3. Click **"Find HR Contacts"**
4. Watch the loading skeleton animation
5. Wait 20-30 seconds
6. **See results!** 🎉
   - Beautiful Stripe-styled cards
   - Personalized connection requests
   - AI-generated follow-up messages
   - Copy with one click

---

## Common Issues & Quick Fixes

### ❌ "Failed to fetch from n8n"

**Solutions:**
1. Is the workflow **Active**? Check the toggle in n8n (top-right)
2. Is the webhook URL correct in `.env.local`?
3. Test webhook directly with curl command above
4. Check n8n **Executions** tab for errors

### ❌ "No contacts found"

**Solutions:**
1. Try a well-known company first: "Google", "Microsoft", "Amazon"
2. Check your Google API quota (100 searches/day limit)
3. Look at n8n **Executions** tab to see what happened
4. Verify Google Search Engine ID is configured for "entire web"

### ❌ Slow Response (taking 30+ seconds)

**This is normal!** The workflow:
1. Searches Google (3-5s)
2. Enriches each profile with Proxycurl (5-10s per profile)
3. Generates AI messages (5-15s)

**To speed up testing:**
- Reduce `max_results` to 3-5
- Skip Proxycurl (remove that node)
- Use GPT-3.5 instead of GPT-4

### ❌ Environment Variable Not Working

**Solutions:**
- Restart Next.js dev server: `npm run dev`
- Ensure exact variable name: `N8N_WEBHOOK_URL`
- For Vercel: Redeploy after adding environment variable
- Check for typos in the webhook URL

### ❌ CORS Error

**Solutions:**
- Use **Production** webhook URL (not test URL)
- For self-hosted n8n, add to your environment:
  ```env
  N8N_WEBHOOK_CORS=http://localhost:3000
  ```

---

## What You Can Do Now

✅ **Search any company** for HR contacts
✅ **Get AI-generated messages** personalized to your background
✅ **Copy messages** with one click
✅ **Export results** as JSON or CSV
✅ **Share your Vercel URL** with others
✅ **Customize the workflow** in n8n

---

## Free Tier Limits

| Service | Free Tier | Cost After |
|---------|-----------|------------|
| Google Custom Search | 100 searches/day | $5 per 1000 |
| Proxycurl | 10-15 credits (3-5 searches) | $0.01-0.03/profile |
| OpenAI GPT-4 | Pay-per-use | ~$0.03/profile |
| n8n Cloud | Free forever | $20/month for more |
| Vercel | Free forever | $20/month for pro |

**Cost per search (20 profiles):** ~$0.60-1.00

---

## Next Steps

### 📚 Learn More
- Full connection guide: `CONNECTING_UI_TO_N8N.md`
- Deployment guide: `VERCEL_DEPLOYMENT.md`
- Workflow details: `IMPROVED_WORKFLOW_GUIDE.md`

### 🎨 Customize
- Edit message templates in n8n workflow
- Modify UI colors in `tailwind.config.ts`
- Add more fields to the search form

### 🚀 Go to Production
1. Set up custom domain on Vercel
2. Configure production n8n instance
3. Add monitoring and analytics
4. Set up API rate limits

---

## Quick Reference

**Workflow File**: `n8n_workflows/linkedin_hr_finder_improved.json`

**Environment Variable**: `N8N_WEBHOOK_URL`

**Webhook Path**: `/webhook/linkedin-hr-finder`

**UI Port**: http://localhost:3000

**Expected Time**: 20-40 seconds per search

**Required APIs**:
- ✅ Google Custom Search (free 100/day)
- ✅ OpenAI (pay-per-use)
- ⚪ Proxycurl (optional, 10 free credits)

---

## Support & Help

- **GitHub Issues**: Report bugs or request features
- **n8n Docs**: https://docs.n8n.io
- **Next.js Docs**: https://nextjs.org/docs
- **Vercel Support**: https://vercel.com/support

---

## ⚠️ Important Reminders

- Use responsibly and ethically
- Respect LinkedIn's Terms of Service
- Don't spam people with automated messages
- The AI messages are starting points - personalize them!
- Keep your API keys secure

---

🚀 **You're all set! Start finding HR contacts and landing your dream job!**

Have fun with your new AI-powered LinkedIn HR Finder! 🎉
