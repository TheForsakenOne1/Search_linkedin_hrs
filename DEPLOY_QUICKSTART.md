# ⚡ Quick Deployment Guide

Get LinkedIn HR Finder running in production in under 1 hour!

## 🚀 30-Minute Production Deployment

### Step 1: Get API Keys (10 min)

```bash
# Google Custom Search API
1. Visit: https://console.cloud.google.com
2. Create project → Enable "Custom Search API"
3. Create API key
4. Create search engine: https://programmablesearchengine.google.com
   - Sites: linkedin.com/in/*
5. Save: API_KEY and SEARCH_ENGINE_ID

# OpenAI API
1. Visit: https://platform.openai.com
2. Create API key
3. Add $10 credit
4. Save: OPENAI_API_KEY
```

### Step 2: Deploy n8n (10 min)

```bash
# Option A: Local (for testing)
docker run -d --name n8n -p 5678:5678 -v ~/.n8n:/home/node/.n8n n8nio/n8n

# Option B: Cloud (production)
# DigitalOcean One-Click App:
# https://marketplace.digitalocean.com/apps/n8n
# Or use deployment script:
wget https://raw.githubusercontent.com/n8n-io/n8n/master/docker/compose/withPostgres/docker-compose.yml
docker-compose up -d
```

**Configure n8n:**

1. Open: `http://localhost:5678` or `http://your-droplet-ip:5678`
2. Create admin account
3. Import workflow: `n8n_workflows/linkedin_hr_finder_improved.json`
4. Add credentials:
   - Google Custom Search API
   - OpenAI API
5. Activate workflow

### Step 3: Deploy UI (10 min)

```bash
cd linkedin-hr-finder-ui

# Install dependencies
npm install

# Option A: Deploy to Vercel (recommended)
npm i -g vercel
vercel

# Add environment variable in Vercel dashboard:
# N8N_WEBHOOK_URL=http://your-n8n-domain:5678/webhook/linkedin-hr-finder

# Option B: Deploy with Docker
docker build -t linkedin-ui .
docker run -d -p 3000:3000 \
  -e N8N_WEBHOOK_URL=http://your-n8n:5678/webhook/linkedin-hr-finder \
  linkedin-ui
```

### Step 4: Test (5 min)

```bash
# 1. Open UI
https://your-vercel-app.vercel.app
# or http://localhost:3000

# 2. Enter test search
Company: Google
Max Results: 5

# 3. Verify results
# Should see 5 HR contacts with AI messages

# 4. Test copy-to-clipboard
# Click "Copy Message" button

# 5. Export test
# Click "Download JSON" button
```

## ✅ You're Live!

Your deployment is complete. Here's what you have:

- ✅ Next.js UI running on Vercel or Docker
- ✅ n8n workflow processing searches
- ✅ Google Search API finding profiles
- ✅ OpenAI generating personalized messages
- ✅ Export functionality working

## 📊 Production Checklist

### Security

```bash
# Enable HTTPS (if self-hosting)
sudo certbot --nginx -d your-domain.com

# Enable n8n basic auth
# Set in docker-compose.yml:
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=secure_password

# Set API rate limits
# In nginx.conf:
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
```

### Monitoring

```bash
# Setup UptimeRobot (free)
https://uptimerobot.com
# Monitor: UI homepage + n8n webhook

# Setup Sentry for errors (free)
cd linkedin-hr-finder-ui
npm install @sentry/nextjs
npx @sentry/wizard -i nextjs
```

### Backups

```bash
# Backup n8n workflows (run weekly)
docker exec n8n n8n export:workflow --all --output=/data/backup.json
docker cp n8n:/data/backup.json ./backups/n8n-$(date +%Y%m%d).json
```

## 💰 Cost Estimate

### Minimal Setup ($12/month)

- n8n: DigitalOcean Droplet ($12/mo)
- UI: Vercel Free tier ($0)
- Google API: Free tier (100/day)
- OpenAI: Pay per use (~$10-20/mo for 500 messages)
- **Total: ~$22-32/month**

### Recommended Setup ($35/month)

- n8n: DigitalOcean Droplet ($12/mo)
- UI: Vercel Pro ($20/mo)
- Domain: Namecheap ($1/mo)
- APIs: ~$10-20/mo
- **Total: ~$43-53/month**

## 🔧 Common Commands

```bash
# View n8n logs
docker logs -f n8n

# Restart n8n
docker restart n8n

# View UI logs (if self-hosted)
docker logs -f linkedin-ui

# Check n8n workflow executions
# Visit: http://your-n8n/executions

# Update n8n
docker pull n8nio/n8n:latest
docker-compose up -d

# Update UI
cd linkedin-hr-finder-ui
git pull
vercel --prod
```

## 🆘 Quick Troubleshooting

### UI can't connect to n8n

```bash
# Check environment variable
vercel env ls

# Update if needed
vercel env add N8N_WEBHOOK_URL

# Verify n8n is accessible
curl http://your-n8n:5678/webhook/linkedin-hr-finder
```

### No results from search

```bash
# Check n8n workflow execution logs
# n8n UI → Executions → Latest execution

# Common issues:
# - Google API quota exceeded (wait till midnight PT)
# - Invalid API keys
# - Workflow not activated
```

### High costs

```bash
# Set OpenAI budget limit
# platform.openai.com → Settings → Usage limits

# Monitor Google API usage
# console.cloud.google.com → APIs → Quotas

# Consider caching results (add Redis later)
```

## 📚 Next Steps

1. **Customize messages**: Edit AI prompts in workflow
2. **Add more sources**: Enable Proxycurl for enrichment
3. **Set up analytics**: Add Google Analytics to UI
4. **Automate backups**: Create cron job for daily backups
5. **Scale**: Add Redis queue for high volume

## 🎯 Production Tips

1. **Test with small batches** - Start with 5-10 results
2. **Review AI messages** - Personalize further for best results
3. **Monitor costs daily** - Check dashboards first week
4. **Set budget alerts** - Avoid surprise bills
5. **Backup regularly** - Export workflows weekly

## 📖 Full Documentation

- Complete deployment plan: `DEPLOYMENT_PLAN.md`
- n8n workflow guide: `IMPROVED_WORKFLOW_GUIDE.md`
- UI documentation: `linkedin-hr-finder-ui/README.md`

---

**That's it! You're ready to find HR contacts and send personalized messages! 🎉**

Questions? Open an issue on GitHub or check the troubleshooting section.
