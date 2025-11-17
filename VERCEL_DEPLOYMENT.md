# Deploy LinkedIn HR Finder to Vercel

This guide will help you deploy the LinkedIn HR Finder UI to Vercel in minutes.

## Prerequisites

- GitHub account
- Vercel account (free tier is perfect for this)
- Your n8n workflow deployed and webhook URL ready

## Quick Deployment (5 minutes)

### Option 1: Deploy via Vercel Dashboard (Recommended)

1. **Push your code to GitHub** (if not already done)
   ```bash
   git push origin claude/improve-n8n-workflow-01KZ7pJbZuJsD9SEgpq4KNMX
   ```

2. **Go to Vercel**
   - Visit https://vercel.com
   - Sign in with your GitHub account
   - Click "Add New" → "Project"

3. **Import Repository**
   - Select your `Search_linkedin_hrs` repository
   - Vercel will auto-detect it's a Next.js project

4. **Configure Build Settings**
   - Framework Preset: **Next.js** (auto-detected)
   - Root Directory: `linkedin-hr-finder-ui`
   - Build Command: `npm run build` (auto-filled)
   - Output Directory: `.next` (auto-filled)
   - Install Command: `npm install` (auto-filled)

5. **Add Environment Variable**
   - Click "Environment Variables"
   - Add:
     - **Name**: `N8N_WEBHOOK_URL`
     - **Value**: Your n8n webhook URL (e.g., `https://your-n8n.app.n8n.cloud/webhook/linkedin-hr-finder`)
   - Click "Add"

6. **Deploy**
   - Click "Deploy"
   - Wait 1-2 minutes for build to complete
   - You'll get a URL like: `https://search-linkedin-hrs.vercel.app`

### Option 2: Deploy via Vercel CLI

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Deploy from project directory**
   ```bash
   cd linkedin-hr-finder-ui
   vercel
   ```

4. **Follow the prompts:**
   - Set up and deploy? **Y**
   - Which scope? (Select your account)
   - Link to existing project? **N**
   - Project name? (Press enter for default)
   - Directory? `./` (current directory)
   - Override settings? **N**

5. **Add environment variable**
   ```bash
   vercel env add N8N_WEBHOOK_URL
   ```
   - Paste your n8n webhook URL when prompted (e.g., `https://your-n8n.app.n8n.cloud/webhook/linkedin-hr-finder`)

6. **Deploy to production**
   ```bash
   vercel --prod
   ```

## Post-Deployment

### Your Live URLs
- **Production**: `https://your-project.vercel.app`
- **Preview**: Every push creates a preview URL

### Test the Deployment
1. Visit your Vercel URL
2. Enter a company name (e.g., "Google")
3. Click "Find HR Contacts"
4. You should see the beautiful Stripe-styled UI with results

### Configure Custom Domain (Optional)
1. In Vercel dashboard, go to your project
2. Click "Settings" → "Domains"
3. Add your custom domain
4. Follow DNS configuration instructions

## Environment Variables

### Required:
- `N8N_WEBHOOK_URL` - Your n8n webhook endpoint (e.g., `https://your-n8n.app.n8n.cloud/webhook/linkedin-hr-finder`)

### To Update Environment Variables:
1. Go to Vercel Dashboard → Your Project → Settings → Environment Variables
2. Edit the value
3. Redeploy (click "Redeploy" in Deployments tab)

Or via CLI:
```bash
vercel env rm N8N_WEBHOOK_URL production
vercel env add N8N_WEBHOOK_URL production
vercel --prod
```

## Continuous Deployment

Vercel automatically deploys:
- **Production**: When you push to your main branch
- **Preview**: When you push to any other branch (like your current claude branch)

To set up auto-deployment:
1. Go to Project Settings → Git
2. Select your production branch (e.g., `main` or `master`)
3. Every push to that branch will auto-deploy

## Troubleshooting

### Build Fails
**Error**: "Module not found"
- **Fix**: Make sure all dependencies are in `package.json`
- Run `npm install` locally first to verify

### Environment Variable Not Working
**Error**: `N8N_WEBHOOK_URL is undefined`
- **Fix**:
  1. Ensure variable name is exactly `N8N_WEBHOOK_URL`
  2. Redeploy after adding env vars
  3. Check variable is set for "Production" environment
  4. Verify the webhook URL is correct

### API Calls Failing (CORS)
**Error**: CORS policy blocking requests
- **Fix**: Your n8n instance needs to allow requests from your Vercel domain
- Add your Vercel URL to n8n's CORS whitelist

### Slow Build Times
- Vercel free tier: ~2-3 minutes
- This is normal for Next.js builds
- Consider caching optimization if needed

## Monitoring & Analytics

### Built-in Vercel Analytics
1. Go to your project dashboard
2. Click "Analytics" tab
3. View:
   - Page views
   - Unique visitors
   - Top pages
   - Performance metrics

### Enable Web Vitals (Recommended)
Already configured in the app:
- Core Web Vitals tracking
- Real User Monitoring
- Performance insights

## Cost

**Free Tier includes:**
- Unlimited deployments
- 100GB bandwidth/month
- Automatic HTTPS
- DDoS protection
- Global CDN
- Preview deployments

**This is perfect for personal/demo use!**

## Advanced Configuration

### Custom Build Settings
Edit `vercel.json` in the `linkedin-hr-finder-ui` directory:

```json
{
  "buildCommand": "npm run build",
  "framework": "nextjs",
  "regions": ["iad1"],
  "env": {
    "N8N_WEBHOOK_URL": "@n8n_webhook_url"
  }
}
```

### Edge Runtime (Optional)
For faster response times, consider moving API routes to Edge Runtime.
Edit `linkedin-hr-finder-ui/app/api/search/route.ts`:

```typescript
export const runtime = 'edge'
```

## Next Steps

1. ✅ Deploy to Vercel
2. ✅ Test with real company searches
3. ✅ Share the URL with others
4. ✅ Monitor analytics
5. ✅ Consider custom domain

## Support

- Vercel Docs: https://vercel.com/docs
- Next.js Docs: https://nextjs.org/docs
- Deployment Issues: Check Vercel Dashboard → Deployments → Build Logs

---

**Enjoy your beautifully deployed LinkedIn HR Finder!** 🚀
