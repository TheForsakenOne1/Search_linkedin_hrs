# Connecting Next.js UI with n8n Workflow

This guide will help you connect the LinkedIn HR Finder UI with your n8n workflow.

## Overview

The connection flow:
```
User (Browser) → Next.js UI → API Route → n8n Webhook → AI APIs → Response
```

## Prerequisites

✅ n8n installed and running
✅ n8n workflow imported
✅ API keys configured in n8n (Google Custom Search, Proxycurl, OpenAI/Claude)

---

## Step 1: Import n8n Workflow

### Option A: Using n8n Cloud
1. Go to https://n8n.io and sign in
2. Click "Workflows" → "Import Workflow"
3. Upload the file: `n8n_workflows/linkedin_hr_finder_improved.json`
4. Click "Import"

### Option B: Using Self-hosted n8n
1. Access your n8n instance (e.g., http://localhost:5678)
2. Click "..." menu → "Import from File"
3. Select `n8n_workflows/linkedin_hr_finder_improved.json`
4. Click "Import"

---

## Step 2: Configure n8n Credentials

### 2.1 Google Custom Search API
1. In n8n, go to **Credentials** → **Create New**
2. Select **"HTTP Request"** or create a custom credential
3. Add your Google API Key and Search Engine ID

**Get Google Credentials:**
- API Key: https://console.cloud.google.com/apis/credentials
- Search Engine ID: https://cse.google.com/cse/all
- Free tier: 100 searches/day

### 2.2 Proxycurl API (Optional but Recommended)
1. Go to https://nubela.co/proxycurl
2. Sign up for free account (10-15 free credits)
3. Get your API key
4. Add to n8n credentials

### 2.3 OpenAI API
1. Get API key from https://platform.openai.com/api-keys
2. Add to n8n as OpenAI credential
3. Model used: GPT-4 (or GPT-3.5 for lower cost)

**Alternative: Use Claude AI**
1. Get API key from https://console.anthropic.com
2. Configure in n8n workflow
3. Model: claude-3-sonnet

---

## Step 3: Activate Webhook in n8n

1. Open the imported workflow in n8n
2. Find the **"Webhook: Start Search"** node (first node)
3. Click on it to see the webhook details
4. Note the webhook URL - it will look like:
   - **Production**: `https://your-n8n.app.n8n.cloud/webhook/linkedin-hr-finder`
   - **Test**: `https://your-n8n.app.n8n.cloud/webhook-test/linkedin-hr-finder`
   - **Self-hosted**: `http://localhost:5678/webhook/linkedin-hr-finder`

5. **Activate the workflow** by toggling the switch in the top-right corner to "Active"

⚠️ **Important**: The workflow MUST be active for the webhook to respond!

---

## Step 4: Configure Next.js Environment Variables

### For Local Development:

1. Create `.env.local` in the `linkedin-hr-finder-ui` directory:

```bash
cd linkedin-hr-finder-ui
cp .env.example .env.local
```

2. Edit `.env.local` and add your n8n webhook URL:

```env
# Use the production webhook URL (not test URL)
N8N_WEBHOOK_URL=https://your-n8n.app.n8n.cloud/webhook/linkedin-hr-finder

# Or for local n8n:
# N8N_WEBHOOK_URL=http://localhost:5678/webhook/linkedin-hr-finder
```

3. Restart your Next.js dev server:
```bash
npm run dev
```

### For Vercel Deployment:

1. Go to your Vercel project dashboard
2. Click **Settings** → **Environment Variables**
3. Add a new variable:
   - **Name**: `N8N_WEBHOOK_URL`
   - **Value**: `https://your-n8n.app.n8n.cloud/webhook/linkedin-hr-finder`
   - **Environment**: Production (and Preview if needed)
4. Click **Save**
5. Redeploy your app (go to Deployments → click "..." → Redeploy)

---

## Step 5: Test the Connection

### Test 1: Direct n8n Webhook Test

Test the n8n webhook directly using curl:

```bash
curl -X POST https://your-n8n.app.n8n.cloud/webhook/linkedin-hr-finder \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "Google",
    "max_results": 5,
    "your_name": "John Doe",
    "your_role": "Software Engineer",
    "your_experience": "3 years",
    "your_skills": "React, Node.js, Python",
    "your_projects": [
      {
        "name": "E-Commerce Platform",
        "description": "Built a scalable platform",
        "tech": "React, Node.js"
      }
    ]
  }'
```

**Expected response:**
```json
{
  "success": true,
  "company": "Google",
  "total_profiles": 5,
  "profiles": [
    {
      "name": "...",
      "title": "...",
      "connection_request": "...",
      "follow_up_message": "..."
    }
  ]
}
```

### Test 2: Test via Next.js UI

1. Start your Next.js app:
   - Local: `npm run dev` → http://localhost:3000
   - Vercel: Visit your deployment URL

2. Fill in the search form:
   - **Company Name**: "Google"
   - **Your Name**: Your actual name
   - **Your Role**: "Software Engineer"
   - Add your skills and projects

3. Click **"Find HR Contacts"**

4. You should see:
   - Loading skeleton animation
   - Results appear in ~10-30 seconds
   - Profile cards with personalized messages

### Test 3: Check Browser Console

1. Open browser DevTools (F12)
2. Go to **Console** tab
3. Look for:
   - ✅ `Calling n8n webhook: https://...`
   - ✅ `n8n response: {...}`
   - ❌ Error messages if something fails

### Test 4: Check n8n Executions

1. In n8n, go to **Executions** tab
2. You should see your workflow run
3. Click on it to see:
   - Each node's execution
   - Data flowing through
   - Any errors

---

## Step 6: Enable CORS (If Needed)

If you get CORS errors when calling from browser:

### For n8n Cloud:
CORS is usually handled automatically.

### For Self-hosted n8n:

Add to your n8n environment variables:

```env
N8N_WEBHOOK_CORS=https://your-vercel-app.vercel.app
# Or for development:
N8N_WEBHOOK_CORS=http://localhost:3000
```

Or allow all origins (not recommended for production):
```env
N8N_WEBHOOK_CORS=*
```

---

## Troubleshooting

### Problem: "Failed to fetch from n8n"

**Solutions:**
1. Check if n8n workflow is **Active** (toggle in top-right)
2. Verify webhook URL in `.env.local` or Vercel settings
3. Test webhook directly with curl (see Test 1 above)
4. Check n8n Executions tab for errors

### Problem: "CORS Error"

**Solutions:**
1. For n8n Cloud: Usually auto-configured
2. For self-hosted: Add `N8N_WEBHOOK_CORS` env var (see Step 6)
3. Use production webhook URL (not test URL)

### Problem: Slow Response

**Normal behavior:**
- First request: 20-40 seconds (API calls + AI generation)
- Expected flow:
  1. Google Search (3-5s)
  2. Proxycurl enrichment (5-10s per profile)
  3. AI message generation (5-15s)

**Solutions:**
- Reduce `max_results` to 5-10 for faster responses
- Use GPT-3.5 instead of GPT-4 for faster generation
- Consider caching common searches

### Problem: "No contacts found"

**Solutions:**
1. Try a larger, well-known company (Google, Microsoft, Amazon)
2. Check Google Custom Search API quota (100/day limit)
3. Verify Google Search credentials in n8n
4. Check n8n Executions for specific error

### Problem: Environment variable not working

**Solutions:**
1. Verify exact name: `N8N_WEBHOOK_URL` (not `NEXT_PUBLIC_N8N_WEBHOOK_URL`)
2. Restart Next.js dev server after changing `.env.local`
3. For Vercel: Redeploy after adding env vars
4. Check for typos in the URL

---

## Architecture Diagram

```
┌─────────────────┐
│   Browser UI    │
│  (Next.js App)  │
└────────┬────────┘
         │
         │ HTTP POST /api/search
         ▼
┌─────────────────┐
│  Next.js API    │
│   Route Handler │
└────────┬────────┘
         │
         │ HTTP POST (with env var N8N_WEBHOOK_URL)
         ▼
┌─────────────────┐
│  n8n Webhook    │
│  /webhook/...   │
└────────┬────────┘
         │
         ├──► Google Custom Search API
         ├──► Proxycurl API
         └──► OpenAI/Claude API
         │
         ▼
┌─────────────────┐
│   Response      │
│  (JSON with     │
│   profiles)     │
└─────────────────┘
```

---

## Production Checklist

Before going live:

- [ ] n8n workflow is **Active**
- [ ] All API credentials configured in n8n
- [ ] Production webhook URL set in Vercel env vars
- [ ] Tested with real company search
- [ ] Checked API quota limits
- [ ] CORS configured (if needed)
- [ ] SSL/HTTPS enabled on n8n (required for production)
- [ ] Error handling tested
- [ ] Response times acceptable (<30s)

---

## Cost Estimation

**Free Tier Usage:**
- Google Custom Search: 100 searches/day = FREE
- Proxycurl: 10-15 free credits (3-5 searches) = FREE
- OpenAI GPT-4: ~$0.03 per profile = ~$0.60 for 20 profiles
- n8n Cloud: Free tier available
- Vercel: Free tier (sufficient)

**After free tier:**
- Need to add billing to Google Cloud, Proxycurl, OpenAI
- See `DEPLOYMENT_PLAN.md` for detailed cost breakdown

---

## Next Steps

1. ✅ Import workflow to n8n
2. ✅ Configure API credentials
3. ✅ Activate workflow
4. ✅ Set environment variable
5. ✅ Test connection
6. ✅ Deploy to Vercel
7. 🎉 Start finding HR contacts!

Need help? Check the troubleshooting section or the full deployment guide in `DEPLOYMENT_PLAN.md`.
