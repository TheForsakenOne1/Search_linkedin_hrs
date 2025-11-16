# 🚀 LinkedIn HR Finder - Complete Deployment Plan

Comprehensive deployment guide for production-ready deployment of the LinkedIn HR Finder platform.

---

## 📋 Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Prerequisites](#prerequisites)
3. [Deployment Options](#deployment-options)
4. [Step-by-Step Deployment](#step-by-step-deployment)
5. [Configuration](#configuration)
6. [Monitoring & Logging](#monitoring--logging)
7. [Scaling Strategy](#scaling-strategy)
8. [Security Best Practices](#security-best-practices)
9. [Cost Estimation](#cost-estimation)
10. [Maintenance Plan](#maintenance-plan)
11. [Rollback Strategy](#rollback-strategy)
12. [Troubleshooting](#troubleshooting)

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     User's Browser                          │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ↓
┌─────────────────────────────────────────────────────────────┐
│                Next.js UI (Vercel/AWS)                      │
│  - Static site generation                                    │
│  - API proxy routes                                          │
│  - Client-side state management                              │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ↓
┌─────────────────────────────────────────────────────────────┐
│                n8n Workflow Engine                          │
│  (Self-hosted/Cloud)                                         │
│  - Webhook endpoint                                          │
│  - Workflow orchestration                                    │
│  - Error handling                                            │
└───────┬────────┬────────┬──────────────────────────────────┘
        │        │        │
        ↓        ↓        ↓
   ┌────────┐ ┌──────┐ ┌────────┐
   │ Google │ │OpenAI│ │Proxycurl│
   │ Search │ │ API  │ │  API   │
   │  API   │ │      │ │(Optional)│
   └────────┘ └──────┘ └────────┘
```

### Components:

1. **Next.js Web UI** - Frontend application
2. **n8n Workflow** - Backend automation platform
3. **External APIs** - Google Search, OpenAI, Proxycurl

### Data Flow:

1. User enters search → Next.js UI
2. UI calls n8n webhook → n8n Workflow
3. n8n calls APIs → Google/OpenAI/Proxycurl
4. Results returned → n8n → UI
5. User views/exports → Local browser

---

## ✅ Prerequisites

### Required Accounts & API Keys:

| Service | Purpose | Cost | Sign-up Link |
|---------|---------|------|--------------|
| **Google Cloud** | Custom Search API | 100/day free, then $5/1000 | [console.cloud.google.com](https://console.cloud.google.com) |
| **OpenAI** | GPT-4 message generation | ~$0.02/message | [platform.openai.com](https://platform.openai.com) |
| **Vercel** (Optional) | Next.js hosting | Free tier available | [vercel.com](https://vercel.com) |
| **DigitalOcean/AWS** (Optional) | n8n hosting | Starting $5/month | [digitalocean.com](https://digitalocean.com) |
| **Proxycurl** (Optional) | Profile enrichment | 10-15 free credits | [nubela.co/proxycurl](https://nubela.co/proxycurl) |

### Required Tools:

- Node.js 18+
- npm or yarn
- Docker (for n8n)
- Git
- Domain name (optional but recommended)

---

## 🎯 Deployment Options

### Option 1: **Quick Start (Development)**

**Best for:** Testing, local development
**Cost:** $0
**Setup time:** 30 minutes

```
Next.js: localhost:3000
n8n: localhost:5678 (Docker)
```

### Option 2: **Production (Cloud)**

**Best for:** Production use, teams
**Cost:** ~$15-30/month
**Setup time:** 2-3 hours

```
Next.js: Vercel (free/hobby plan)
n8n: DigitalOcean Droplet ($12/month)
Domain: Namecheap (~$12/year)
```

### Option 3: **Enterprise (Full Cloud)**

**Best for:** High volume, enterprise
**Cost:** ~$100-300/month
**Setup time:** 1 day

```
Next.js: Vercel Pro
n8n: AWS ECS/Fargate
Database: RDS (if needed later)
CDN: CloudFront
Monitoring: DataDog/NewRelic
```

---

## 📦 Step-by-Step Deployment

### Phase 1: Setup API Keys (30 minutes)

#### 1.1 Google Custom Search API

```bash
# 1. Go to Google Cloud Console
https://console.cloud.google.com

# 2. Create new project "LinkedIn HR Finder"

# 3. Enable Custom Search API
Navigation Menu → APIs & Services → Enable APIs

# 4. Create credentials
APIs & Services → Credentials → Create Credentials → API Key

# 5. Create Custom Search Engine
https://programmablesearchengine.google.com/create

# Settings:
- Sites to search: linkedin.com/in/*
- Name: LinkedIn Profile Search

# 6. Get Search Engine ID (cx parameter)
```

**Save these:**
- `GOOGLE_API_KEY`: Your API key
- `GOOGLE_SEARCH_ENGINE_ID`: Your cx ID

#### 1.2 OpenAI API

```bash
# 1. Sign up at platform.openai.com

# 2. Navigate to API Keys
https://platform.openai.com/api-keys

# 3. Create new secret key
Click "Create new secret key"
Name: "LinkedIn HR Finder"

# 4. Add credits
Billing → Add payment method → Add $10-20

# 5. Set usage limits (recommended)
Settings → Usage limits → $50/month
```

**Save:**
- `OPENAI_API_KEY`: Your API key

#### 1.3 Proxycurl (Optional)

```bash
# 1. Sign up at nubela.co/proxycurl

# 2. Get free credits (10-15)

# 3. Get API key from dashboard

# 4. (Optional) Top up $10 for 1000 credits
```

**Save:**
- `PROXYCURL_API_KEY`: Your API key

---

### Phase 2: Deploy n8n (1 hour)

#### Option A: Docker (Recommended for beginners)

```bash
# 1. Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# 2. Create n8n directory
mkdir -p ~/.n8n

# 3. Run n8n
docker run -d \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  --restart unless-stopped \
  n8nio/n8n

# 4. Access n8n
http://localhost:5678

# 5. Create admin account
# Follow on-screen prompts
```

#### Option B: DigitalOcean Droplet (Production)

```bash
# 1. Create Droplet
- OS: Ubuntu 22.04 LTS
- Plan: Basic $12/month (2GB RAM, 50GB SSD)
- Datacenter: Closest to your users
- Add SSH keys

# 2. SSH into droplet
ssh root@your_droplet_ip

# 3. Install Docker
apt update && apt upgrade -y
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# 4. Install Docker Compose
apt install docker-compose -y

# 5. Create docker-compose.yml
cat > docker-compose.yml <<EOF
version: '3.8'

services:
  n8n:
    image: n8nio/n8n:latest
    restart: unless-stopped
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=your_secure_password_here
      - N8N_HOST=your-domain.com
      - N8N_PROTOCOL=https
      - WEBHOOK_URL=https://your-domain.com/
    volumes:
      - n8n_data:/home/node/.n8n

volumes:
  n8n_data:
EOF

# 6. Start n8n
docker-compose up -d

# 7. Setup Nginx reverse proxy
apt install nginx certbot python3-certbot-nginx -y

# 8. Configure Nginx
cat > /etc/nginx/sites-available/n8n <<EOF
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5678;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
    }
}
EOF

# 9. Enable site
ln -s /etc/nginx/sites-available/n8n /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx

# 10. Get SSL certificate
certbot --nginx -d your-domain.com
```

#### Import Workflow to n8n

```bash
# 1. Open n8n interface
http://your-domain.com or http://localhost:5678

# 2. Click "Add workflow"

# 3. Click "Import from file"

# 4. Select: linkedin-hr-finder-improved.json

# 5. Configure credentials:
# - Add Google Custom Search API credentials
# - Add OpenAI API credentials
# - (Optional) Add Proxycurl credentials

# 6. Activate workflow
Click toggle switch to "Active"

# 7. Test webhook
curl -X POST http://your-domain.com/webhook/linkedin-hr-finder \
  -H "Content-Type: application/json" \
  -d '{"company_name": "Google"}'
```

---

### Phase 3: Deploy Next.js UI (30 minutes)

#### Option A: Vercel (Recommended - Easiest)

```bash
# 1. Install Vercel CLI
npm install -g vercel

# 2. Navigate to UI directory
cd linkedin-hr-finder-ui

# 3. Create .env.production
cat > .env.production <<EOF
N8N_WEBHOOK_URL=https://your-n8n-domain.com/webhook/linkedin-hr-finder
EOF

# 4. Deploy to Vercel
vercel

# Follow prompts:
# - Link to existing project? No
# - Project name: linkedin-hr-finder-ui
# - Directory: ./
# - Build command: npm run build
# - Output directory: .next
# - Development command: npm run dev

# 5. Add environment variables in Vercel dashboard
https://vercel.com/your-username/linkedin-hr-finder-ui/settings/environment-variables

# Add:
# N8N_WEBHOOK_URL = https://your-n8n-domain.com/webhook/linkedin-hr-finder

# 6. Redeploy
vercel --prod

# 7. Done! Your site is live at:
# https://linkedin-hr-finder-ui.vercel.app
```

#### Option B: Docker + Nginx (Self-hosted)

```bash
# 1. Create Dockerfile in linkedin-hr-finder-ui/
cat > linkedin-hr-finder-ui/Dockerfile <<EOF
FROM node:18-alpine AS base

# Install dependencies
FROM base AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci

# Build app
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
ENV NEXT_TELEMETRY_DISABLED 1
RUN npm run build

# Production image
FROM base AS runner
WORKDIR /app
ENV NODE_ENV production
ENV NEXT_TELEMETRY_DISABLED 1

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs
EXPOSE 3000
ENV PORT 3000

CMD ["node", "server.js"]
EOF

# 2. Update next.config.js
cat > next.config.js <<EOF
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  output: 'standalone',
  env: {
    N8N_WEBHOOK_URL: process.env.N8N_WEBHOOK_URL,
  },
}

module.exports = nextConfig
EOF

# 3. Build Docker image
docker build -t linkedin-hr-finder-ui .

# 4. Run container
docker run -d \
  --name linkedin-ui \
  -p 3000:3000 \
  -e N8N_WEBHOOK_URL=https://your-n8n-domain.com/webhook/linkedin-hr-finder \
  --restart unless-stopped \
  linkedin-hr-finder-ui

# 5. Setup Nginx
cat > /etc/nginx/sites-available/linkedin-ui <<EOF
server {
    listen 80;
    server_name ui.your-domain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
    }
}
EOF

# 6. Enable and get SSL
ln -s /etc/nginx/sites-available/linkedin-ui /etc/nginx/sites-enabled/
certbot --nginx -d ui.your-domain.com
systemctl restart nginx
```

---

## ⚙️ Configuration

### Environment Variables

#### Next.js UI (`.env.production`)

```env
# Required
N8N_WEBHOOK_URL=https://your-n8n.com/webhook/linkedin-hr-finder

# Optional
NEXT_PUBLIC_APP_NAME=LinkedIn HR Finder
NEXT_PUBLIC_APP_URL=https://your-ui.com
```

#### n8n (Docker Compose)

```yaml
environment:
  - N8N_BASIC_AUTH_ACTIVE=true
  - N8N_BASIC_AUTH_USER=admin
  - N8N_BASIC_AUTH_PASSWORD=secure_password
  - N8N_HOST=your-n8n-domain.com
  - N8N_PROTOCOL=https
  - WEBHOOK_URL=https://your-n8n-domain.com/
  - EXECUTIONS_DATA_PRUNE=true
  - EXECUTIONS_DATA_MAX_AGE=168  # 7 days
```

### n8n Workflow Credentials

Add in n8n UI → Settings → Credentials:

1. **Google Custom Search API**
   - Credential type: Custom API
   - API Key: `your_google_api_key`
   - Search Engine ID: `your_cx_id`

2. **OpenAI**
   - Credential type: OpenAI
   - API Key: `your_openai_key`

3. **Proxycurl** (Optional)
   - Credential type: HTTP Header Auth
   - Header Name: `Authorization`
   - Header Value: `Bearer your_proxycurl_key`

---

## 📊 Monitoring & Logging

### Option 1: Simple Logging (Free)

```bash
# n8n logs
docker logs -f n8n

# Next.js logs (if self-hosted)
docker logs -f linkedin-ui

# Nginx logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

### Option 2: Professional Monitoring

#### Setup Uptime Monitoring (Free)

```bash
# Use UptimeRobot (free)
https://uptimerobot.com

# Add monitors:
# 1. n8n webhook: https://your-n8n.com/webhook/linkedin-hr-finder
# 2. UI homepage: https://your-ui.com

# Email alerts on downtime
```

#### Setup Error Tracking

```bash
# Sentry for Next.js (free tier)

# 1. Sign up at sentry.io

# 2. Install Sentry
cd linkedin-hr-finder-ui
npm install @sentry/nextjs

# 3. Configure
npx @sentry/wizard -i nextjs

# 4. Add to next.config.js
# (Wizard handles this)

# 5. Deploy
```

#### Log Aggregation

```bash
# Option 1: Papertrail (free tier)
https://papertrailapp.com

# Option 2: Logtail
https://logtail.com

# Configure Docker logging
docker run -d \
  --name n8n \
  --log-driver=syslog \
  --log-opt syslog-address=tcp://logs.papertrailapp.com:12345 \
  ...
```

---

## 📈 Scaling Strategy

### Phase 1: Single Server (0-1000 searches/day)

```
Cost: ~$15/month
Setup: 1 Droplet + Vercel

- n8n: DigitalOcean ($12/month)
- UI: Vercel (free)
- Total: $12/month
```

### Phase 2: Multi-Server (1000-10,000 searches/day)

```
Cost: ~$50-100/month
Setup: Load balanced n8n + CDN

- n8n: 2x Droplets ($24/month) + Load Balancer ($10/month)
- UI: Vercel Pro ($20/month)
- CDN: CloudFlare (free)
- Database: PostgreSQL ($15/month) if needed
- Total: ~$70/month
```

### Phase 3: Cloud Native (10,000+ searches/day)

```
Cost: ~$200-500/month
Setup: AWS/GCP with auto-scaling

- n8n: AWS ECS Fargate (auto-scale)
- UI: Vercel Pro + Edge Functions
- Database: RDS PostgreSQL
- Cache: Redis (ElastiCache)
- CDN: CloudFront
- Monitoring: DataDog
```

### Horizontal Scaling

```bash
# n8n supports queue mode for scaling

# 1. Add Redis
docker run -d \
  --name redis \
  -p 6379:6379 \
  redis:alpine

# 2. Update n8n config
environment:
  - QUEUE_BULL_REDIS_HOST=redis
  - QUEUE_BULL_REDIS_PORT=6379
  - EXECUTIONS_MODE=queue

# 3. Run multiple n8n workers
docker run -d --name n8n-worker-1 ...
docker run -d --name n8n-worker-2 ...
```

---

## 🔒 Security Best Practices

### 1. API Key Security

```bash
# Never commit API keys
# Use environment variables
# Rotate keys quarterly

# Example: Secure key storage
# Use AWS Secrets Manager or HashiCorp Vault
```

### 2. HTTPS/SSL

```bash
# Always use HTTPS
# Free SSL from Let's Encrypt

certbot --nginx -d your-domain.com
```

### 3. Rate Limiting

```nginx
# Add to nginx config
limit_req_zone $binary_remote_addr zone=one:10m rate=10r/s;

server {
    location / {
        limit_req zone=one burst=20;
        ...
    }
}
```

### 4. Authentication

```bash
# Enable n8n basic auth (already configured)
# Add API key authentication for webhook

# In n8n workflow, add HTTP auth node
```

### 5. CORS Configuration

```javascript
// next.config.js
module.exports = {
  async headers() {
    return [
      {
        source: '/api/:path*',
        headers: [
          { key: 'Access-Control-Allow-Origin', value: 'https://your-domain.com' },
        ],
      },
    ]
  },
}
```

### 6. Input Validation

```javascript
// Already implemented in API routes
// Validates company name, max results, etc.
```

---

## 💰 Cost Estimation

### Monthly Costs (Production)

| Item | Cost | Volume |
|------|------|--------|
| **Infrastructure** |  |  |
| n8n Hosting (DigitalOcean) | $12 | 2GB RAM droplet |
| Next.js UI (Vercel) | $0-20 | Free tier / Pro |
| Domain Name | $1 | Yearly $12 |
| SSL Certificate | $0 | Let's Encrypt |
| **APIs** |  |  |
| Google Search API | $0-25 | 100/day free, $5/1000 after |
| OpenAI GPT-4 | $10-50 | ~$0.02 per message |
| Proxycurl (Optional) | $0-10 | 10-15 free, $0.01 per profile |
| **Monitoring** |  |  |
| UptimeRobot | $0 | Free tier |
| Sentry | $0 | Free tier |
| **Total** | **$23-108** | **Low to medium usage** |

### Usage-Based Pricing

```
Example: 500 searches/month

Infrastructure: $12 (n8n)
Google API: $0 (under free tier)
OpenAI: 500 × 20 contacts × $0.02 = $200
Proxycurl: $0 (skip enrichment)

Total: ~$212/month

Per contact: $0.021
Per search: $0.42
```

### Cost Optimization Tips

1. **Use free tiers**
   - Google: 100 searches/day = 3000/month free
   - Vercel: Free for personal projects
   - n8n: Self-host instead of cloud

2. **Optimize API calls**
   - Cache results (add Redis)
   - Batch requests
   - Use cheaper models (GPT-3.5 vs GPT-4)

3. **Set budget alerts**
   - OpenAI: Set monthly limit
   - Google Cloud: Set budget alerts
   - Monitor usage daily

---

## 🔧 Maintenance Plan

### Daily

- Monitor uptime (automated)
- Check error logs (automated alerts)
- Review API usage/costs

### Weekly

- Review performance metrics
- Check for n8n workflow failures
- Update dependencies (security patches)

### Monthly

- Rotate API keys
- Review and optimize costs
- Backup n8n workflows
- Update documentation

### Quarterly

- Major dependency updates
- Security audit
- Performance optimization
- User feedback review

### Backup Strategy

```bash
# Backup n8n workflows (weekly)
docker exec n8n n8n export:workflow --all --output=/data/backup.json

# Copy to safe location
docker cp n8n:/data/backup.json ./backups/n8n-$(date +%Y%m%d).json

# Upload to S3/Google Drive
aws s3 cp ./backups/n8n-$(date +%Y%m%d).json s3://your-bucket/backups/
```

---

## ↩️ Rollback Strategy

### If Deployment Fails

```bash
# 1. Rollback Next.js UI (Vercel)
vercel rollback

# 2. Rollback n8n workflow
# Import previous backup in n8n UI

# 3. Revert Docker container
docker stop n8n
docker rm n8n
docker run ... # Use previous image/config

# 4. Restore from backup
docker exec n8n n8n import:workflow --input=/data/backup.json
```

### Database Migrations (Future)

```bash
# If you add database later
# Use migration tools like Prisma

npx prisma migrate down  # Rollback
npx prisma migrate up    # Re-apply
```

---

## 🔍 Troubleshooting

### Common Issues

#### 1. n8n Webhook Returns 404

```bash
# Check workflow is active
# Verify webhook URL matches
# Check n8n logs: docker logs n8n

# Test webhook directly
curl -X POST http://localhost:5678/webhook/linkedin-hr-finder \
  -H "Content-Type: application/json" \
  -d '{"company_name": "Test"}'
```

#### 2. UI Can't Connect to n8n

```bash
# Check CORS settings in n8n
# Verify N8N_WEBHOOK_URL in UI .env
# Check network/firewall rules

# Test from UI server
curl -X POST $N8N_WEBHOOK_URL -d '{"company_name":"Test"}'
```

#### 3. Google API Quota Exceeded

```bash
# Check quota in Google Cloud Console
# Wait for daily reset (midnight PT)
# Consider upgrading to paid tier

# Monitor usage
gcloud services quota list --service=customsearch.googleapis.com
```

#### 4. OpenAI API Errors

```bash
# Check API key is valid
# Verify account has credits
# Check rate limits

# Test API key
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

#### 5. High Costs

```bash
# Review usage in dashboards
# Set billing alerts
# Optimize API calls
# Consider caching results

# Google Cloud: Set budget alerts
# OpenAI: Set monthly limits
# Track per-user/per-search costs
```

---

## 📚 Additional Resources

### Documentation

- [n8n Documentation](https://docs.n8n.io)
- [Next.js Deployment](https://nextjs.org/docs/deployment)
- [Vercel Documentation](https://vercel.com/docs)
- [Google Custom Search API](https://developers.google.com/custom-search/v1/overview)
- [OpenAI API Reference](https://platform.openai.com/docs)

### Support

- GitHub Issues: [Project Repository](https://github.com/TheForsakenOne1/Search_linkedin_hrs)
- n8n Community: [community.n8n.io](https://community.n8n.io)
- Next.js Discord: [nextjs.org/discord](https://nextjs.org/discord)

---

## ✅ Deployment Checklist

### Pre-Deployment

- [ ] All API keys obtained
- [ ] Domain purchased (if using)
- [ ] DNS configured
- [ ] SSL certificates ready
- [ ] Backup plan in place

### n8n Deployment

- [ ] n8n installed and running
- [ ] Workflows imported
- [ ] Credentials configured
- [ ] Webhooks tested
- [ ] Basic auth enabled
- [ ] HTTPS configured

### UI Deployment

- [ ] Dependencies installed
- [ ] Environment variables set
- [ ] Build successful
- [ ] Deployment completed
- [ ] Custom domain connected
- [ ] HTTPS working

### Post-Deployment

- [ ] Full end-to-end test
- [ ] Monitoring configured
- [ ] Error tracking setup
- [ ] Backup automated
- [ ] Documentation updated
- [ ] Team trained

### Production Ready

- [ ] Load testing completed
- [ ] Security audit passed
- [ ] Budget alerts configured
- [ ] Rollback plan tested
- [ ] Support channels ready
- [ ] Maintenance schedule set

---

## 🎉 Congratulations!

Your LinkedIn HR Finder is now deployed and ready for production use!

### Next Steps:

1. **Test thoroughly** - Run multiple searches
2. **Monitor closely** - Watch for errors first week
3. **Gather feedback** - Get user input
4. **Iterate** - Make improvements
5. **Scale** - Grow as needed

### Quick Support:

- 🐛 **Bug reports**: GitHub Issues
- 💬 **Questions**: GitHub Discussions
- 📧 **Enterprise**: Contact via GitHub

---

**Happy deploying! 🚀**

*Last updated: January 2025*
