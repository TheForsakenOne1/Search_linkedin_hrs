# 🚀 LinkedIn HR Finder - Next.js UI

Beautiful, modern web interface for finding and messaging LinkedIn HR contacts with AI-powered personalization. No database required!

![LinkedIn HR Finder](https://img.shields.io/badge/Next.js-14-black?style=for-the-badge&logo=next.js)
![TypeScript](https://img.shields.io/badge/TypeScript-5-blue?style=for-the-badge&logo=typescript)
![Tailwind CSS](https://img.shields.io/badge/Tailwind-3-38bdf8?style=for-the-badge&logo=tailwind-css)

## ✨ Features

- 🎯 **Simple Search** - Just enter a company name
- 🤖 **AI-Powered** - GPT-4/Claude generates personalized messages
- 📋 **One-Click Copy** - Copy messages to clipboard instantly
- 🔗 **Direct LinkedIn Links** - Open profiles with one click
- 💾 **Profile Saving** - Save your info locally (no database!)
- 📊 **Export Results** - Download as JSON or CSV
- 🎨 **Beautiful UI** - Modern, responsive design
- ⚡ **Fast & Lightweight** - Built with Next.js 14

## 🎯 Screenshots

### Main Interface
![Main Interface](screenshots/main.png)

### Search Form with Projects
![Search Form](screenshots/search.png)

### Results with AI Messages
![Results](screenshots/results.png)

## 🚀 Quick Start

### Prerequisites

1. **n8n workflow running** (see main README)
2. **Node.js 18+** installed
3. **npm or yarn** installed

### Installation

```bash
# Navigate to the UI directory
cd linkedin-hr-finder-ui

# Install dependencies
npm install

# Copy environment variables
cp .env.example .env.local

# Edit .env.local if your n8n is not on localhost:5678
# N8N_WEBHOOK_URL=http://localhost:5678/webhook/linkedin-hr-finder

# Run development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser!

## 📖 How to Use

### 1. **Basic Search**

1. Enter company name (e.g., "Google", "Microsoft")
2. Adjust max results slider (5-50)
3. Click "Find HR Contacts"
4. Wait 30-60 seconds for results

### 2. **Advanced Search (Personalized Messages)**

1. Click "Show Advanced Options"
2. Fill in your profile:
   - Your name
   - Your role
   - Years of experience
   - Your skills
3. Add your projects:
   - Project name
   - Description (with metrics!)
   - Technologies used
4. Click "Save Profile" to remember for next time
5. Click "Find HR Contacts"

### 3. **Using Results**

For each HR contact, you'll see:

- **Profile Info** - Name, title, location
- **Connection Request** - Short message (<300 chars)
- **Follow-up Message** - Detailed message with your projects

**Actions:**

- 📋 **Copy Message** - Copies to clipboard
- 🔗 **View Profile** - Opens LinkedIn profile
- 📤 **Send on LinkedIn** - Opens profile (you send manually)
- 💾 **Download** - Export all results as JSON/CSV

### 4. **Sending Messages**

1. Click "Copy Message" on connection request
2. Click "Send on LinkedIn" or "View Profile"
3. LinkedIn opens in new tab
4. Click "Connect" button
5. Paste your message
6. Send!

After they accept:
1. Copy the follow-up message
2. Send as a LinkedIn message
3. Start the conversation!

## 🏗️ Project Structure

```
linkedin-hr-finder-ui/
├── app/
│   ├── api/
│   │   └── search/
│   │       └── route.ts          # Proxy API to n8n
│   ├── globals.css               # Global styles
│   ├── layout.tsx                # Root layout
│   └── page.tsx                  # Main page
├── components/
│   ├── SearchForm.tsx            # Search form with profile
│   ├── ProfileCard.tsx           # Individual HR contact card
│   └── ResultsDisplay.tsx        # Results grid & export
├── lib/
│   ├── types.ts                  # TypeScript types
│   └── utils.ts                  # Utilities (storage, clipboard)
├── public/                       # Static assets
├── .env.example                  # Environment variables example
├── next.config.js                # Next.js configuration
├── tailwind.config.ts            # Tailwind CSS configuration
├── tsconfig.json                 # TypeScript configuration
└── package.json                  # Dependencies
```

## 🔧 Configuration

### Environment Variables

Create `.env.local` file:

```env
# n8n Webhook URL (default: localhost)
N8N_WEBHOOK_URL=http://localhost:5678/webhook/linkedin-hr-finder

# For production:
# N8N_WEBHOOK_URL=https://your-n8n-instance.com/webhook/linkedin-hr-finder
```

### Customizing Colors

Edit `tailwind.config.ts` to change LinkedIn blue color:

```typescript
linkedin: {
  500: '#0a66c2',  // Main LinkedIn blue
  600: '#004182',  // Darker shade
  // ...
}
```

## 💾 Local Storage

The app uses browser localStorage to save your profile:

- **Key:** `userProfile`
- **Data:** Your name, role, experience, skills, projects
- **Duration:** Persists until you clear browser data
- **Privacy:** Stored only in your browser, never sent anywhere

### Clear Saved Profile

Open browser console and run:
```javascript
localStorage.removeItem('userProfile')
```

## 📊 API Reference

### POST `/api/search`

Searches for LinkedIn HR contacts.

**Request Body:**
```json
{
  "company_name": "Google",
  "max_results": 20,
  "your_name": "John Doe",
  "your_role": "Software Engineer",
  "your_experience": "5 years",
  "your_skills": "Python, React, AWS",
  "your_projects": [
    {
      "name": "E-Commerce Platform",
      "description": "Built platform serving 100K users",
      "tech": "React, Node.js, AWS"
    }
  ]
}
```

**Response:**
```json
{
  "success": true,
  "company": "Google",
  "total_profiles": 15,
  "profiles": [
    {
      "name": "Jane Smith",
      "title": "Senior Technical Recruiter",
      "location": "San Francisco, CA",
      "profile_url": "https://linkedin.com/in/janesmith",
      "connection_request": "Hi Jane! ...",
      "follow_up_message": "Hi Jane,\n\n...",
      "char_count_connection": 189,
      "char_count_followup": 724,
      "generated_at": "2025-01-15T10:30:00Z",
      "ai_provider": "openai"
    }
  ]
}
```

## 🎨 UI Components

### SearchForm
- Company name input
- Max results slider
- Advanced options (collapsible)
- Your profile fields
- Dynamic project list
- Save/load profile from localStorage

### ProfileCard
- Contact information
- LinkedIn profile link
- Connection request message
- Follow-up message
- Copy-to-clipboard buttons
- "Send on LinkedIn" button
- AI provider badge

### ResultsDisplay
- Summary header
- Total profiles count
- Export buttons (JSON/CSV)
- Grid of profile cards
- Empty states
- Error handling

## 🚢 Deployment

### Vercel (Recommended)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Set environment variable in Vercel dashboard
# N8N_WEBHOOK_URL=https://your-n8n-instance.com/webhook/linkedin-hr-finder
```

### Docker

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]
```

```bash
# Build
docker build -t linkedin-hr-finder-ui .

# Run
docker run -p 3000:3000 -e N8N_WEBHOOK_URL=http://your-n8n:5678/webhook/linkedin-hr-finder linkedin-hr-finder-ui
```

### Manual Deployment

```bash
# Build for production
npm run build

# Start production server
npm start
```

## 🔍 Troubleshooting

### "Failed to fetch from n8n"

**Problem:** Can't connect to n8n webhook

**Solutions:**
1. Verify n8n is running: `curl http://localhost:5678`
2. Check N8N_WEBHOOK_URL in `.env.local`
3. Ensure n8n workflow is active
4. Check n8n webhook URL matches

### "No results found"

**Problem:** Search returns 0 profiles

**Solutions:**
1. Verify company name spelling
2. Try different company (some have fewer public profiles)
3. Check n8n workflow execution logs
4. Verify Google Custom Search API is configured
5. Check API quota (100/day limit)

### "CORS error"

**Problem:** Browser blocks n8n requests

**Solution:** Use the API proxy route (`/api/search`) - already configured!

### Messages not copying

**Problem:** Copy to clipboard doesn't work

**Solutions:**
1. Use HTTPS (required for clipboard API)
2. Check browser permissions
3. Try manual copy (select + Ctrl+C)

## 💡 Tips & Best Practices

### For Best Results:

1. **Fill in your profile** - AI generates better messages
2. **Add projects with metrics** - Numbers make messages compelling
3. **Review before sending** - Personalize further for best results
4. **Use follow-up strategically** - Send 24-48 hours after connection
5. **Track responses** - Note what works for iteration

### Sending Messages:

1. ❌ Don't spam - Max 20-30 per day
2. ✅ Personalize further - Add company-specific details
3. ✅ Be genuine - AI is a starting point
4. ✅ Follow up - Use the detailed message after acceptance
5. ✅ Track results - See what works

## 🛠️ Development

### Run in Development Mode

```bash
npm run dev
```

### Build for Production

```bash
npm run build
```

### Run Production Build Locally

```bash
npm start
```

### Lint Code

```bash
npm run lint
```

## 📦 Tech Stack

- **Framework:** Next.js 14 (App Router)
- **Language:** TypeScript 5
- **Styling:** Tailwind CSS 3
- **Icons:** Lucide React
- **State:** React Hooks
- **Storage:** localStorage
- **API:** Next.js API Routes

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

MIT License - see main repository

## 🆘 Support

- **Issues:** [GitHub Issues](https://github.com/TheForsakenOne1/Search_linkedin_hrs/issues)
- **Discussions:** [GitHub Discussions](https://github.com/TheForsakenOne1/Search_linkedin_hrs/discussions)
- **Main README:** [Parent Directory](../README.md)

## 🎉 Acknowledgments

- Built with [Next.js](https://nextjs.org/)
- Icons by [Lucide](https://lucide.dev/)
- Styled with [Tailwind CSS](https://tailwindcss.com/)
- Powered by [n8n](https://n8n.io/)

---

**Made with ❤️ for job seekers, networkers, and recruiters**

*Remember: Quality > Quantity. Personal touches make all the difference!*
