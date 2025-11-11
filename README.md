# LinkedIn HR & Hiring Personnel Scraper + Automated Outreach

A comprehensive Python tool to scrape HR contacts from LinkedIn, generate personalized messages using AI, and manage outreach campaigns through n8n workflows.

## 🎯 Key Features

### Scraping & Discovery
- 🔍 **Smart Search**: Automatically searches for HR personnel using 20+ job title keywords
- 🏢 **Company-Specific**: Target any company to find their hiring team
- 📊 **Multiple Export Formats**: Export results to CSV, JSON, or Excel
- 🤖 **Automated Browser Control**: Uses Selenium for reliable scraping

### Message Generation & Outreach
- ✉️ **AI-Powered Messages**: Generate personalized, human-like messages for each contact
- 🎭 **Multiple Scenarios**: Job seeker, networking, recruiter outreach, informational interviews
- 🔄 **n8n Integration**: Automate workflows with the included n8n workflow templates
- 🛡️ **Safety Features**: Manual review mode, rate limiting, message validation

### HR Keywords Targeting
- Human Resources Managers
- Recruiters & Talent Acquisition
- HR Business Partners
- Hiring Managers
- People Operations
- Talent Partners & Directors
- Chief People Officers
- And many more...

## Prerequisites

- Python 3.8 or higher
- Google Chrome browser installed
- Active LinkedIn account
- Basic understanding of web scraping ethics and LinkedIn's terms of service

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/Search_linkedin_hrs.git
cd Search_linkedin_hrs
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure credentials**
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your LinkedIn credentials
# Use a text editor to edit .env:
nano .env  # or vim .env, or any editor
```

Edit the `.env` file and add your credentials:
```env
LINKEDIN_EMAIL=your_email@example.com
LINKEDIN_PASSWORD=your_password
HEADLESS_MODE=False
EXPORT_FORMAT=csv
```

## Usage

### Interactive Mode (Recommended for beginners)

Simply run the script without arguments:

```bash
python main.py
```

You'll be prompted to enter:
- Company name
- Maximum number of results
- Export format preference

### Command Line Mode

**Basic usage:**
```bash
python main.py --company "Google"
```

**With options:**
```bash
# Search with maximum 100 results
python main.py --company "Microsoft" --max-results 100

# Export to JSON format
python main.py --company "Amazon" --format json

# Export to all formats (CSV, JSON, Excel)
python main.py --company "Apple" --format all

# Run in headless mode (no browser window)
python main.py --company "Meta" --headless
```

### Command Line Arguments

```
Options:
  -c, --company COMPANY       Company name to search
  -m, --max-results NUM       Maximum number of results (default: 50)
  -f, --format FORMAT         Export format: csv, json, excel, or all (default: csv)
  --headless                  Run browser in headless mode
  -h, --help                  Show help message
```

## 🚀 Complete Workflow (Scraping + Messaging)

**NEW!** Use the complete workflow to scrape, generate messages, and prepare for outreach:

### Quick Start - Complete Workflow

```bash
# Interactive mode with all features
python complete_workflow.py
```

### Export Mode (Recommended - Safest)

Generate messages and export for review in n8n:

```bash
# Basic export
python complete_workflow.py --company "Google" --export-only

# With personalization
python complete_workflow.py \
  --company "Microsoft" \
  --scenario job_seeker \
  --role "Software Engineer" \
  --years "5" \
  --skills "Python, React, AWS" \
  --export-only
```

This creates:
- `output/linkedin_hr_<company>.json` - Scraped HR contacts
- `output/messages_<company>_<scenario>.json` - Generated messages
- `output/workflow_<company>.json` - Complete workflow for n8n

### Message Scenarios

Choose from 4 built-in message scenarios:

1. **job_seeker** - Looking for job opportunities (default)
2. **networking** - Professional connection and networking
3. **recruiter_outreach** - Offering candidates to HR teams
4. **informational_interview** - Seeking career advice

**Examples:**

```bash
# Job seeker messages
python complete_workflow.py \
  --company "Amazon" \
  --scenario job_seeker \
  --role "Product Manager" \
  --years "7" \
  --skills "Product Strategy, Agile" \
  --export-only

# Networking messages
python complete_workflow.py \
  --company "Meta" \
  --scenario networking \
  --industry "technology" \
  --export-only

# Informational interview
python complete_workflow.py \
  --company "Apple" \
  --scenario informational_interview \
  --export-only
```

### n8n Integration

**See [N8N_INTEGRATION_GUIDE.md](N8N_INTEGRATION_GUIDE.md) for complete setup instructions.**

**Quick n8n Setup:**

1. Install n8n:
   ```bash
   docker run -it --rm --name n8n -p 5678:5678 -v ~/.n8n:/home/node/.n8n n8nio/n8n
   ```

2. Start message service:
   ```bash
   python message_service.py
   ```

3. Import workflow:
   - Open n8n at `http://localhost:5678`
   - Import `n8n_workflows/linkedin_hr_messaging_workflow.json`
   - Configure and run!

**n8n Benefits:**
- Visual workflow management
- Message review and approval
- Batch processing
- Integration with other tools (Slack, Email, CRM)
- Scheduling and automation

### Message Service API

The message service provides a REST API for generating messages:

```bash
# Start the service
python message_service.py

# Test it
curl http://localhost:5000/health
```

**API Endpoints:**
- `GET /health` - Health check
- `GET /scenarios` - List available scenarios
- `POST /generate-message` - Generate single message
- `POST /generate-bulk` - Generate bulk messages
- `POST /generate-from-file` - Generate from scraped data file

See [N8N_INTEGRATION_GUIDE.md](N8N_INTEGRATION_GUIDE.md) for API documentation.

## Configuration

Edit `config.py` or `.env` file to customize:

### Environment Variables (.env)

```env
# LinkedIn Credentials
LINKEDIN_EMAIL=your_email@example.com
LINKEDIN_PASSWORD=your_password

# Scraping Configuration
HEADLESS_MODE=False          # Set to True to run without browser window
IMPLICIT_WAIT=10             # Seconds to wait for elements
PAGE_LOAD_TIMEOUT=30         # Page load timeout in seconds

# Export Settings
EXPORT_FORMAT=csv            # Default format: csv, json, or excel
OUTPUT_DIRECTORY=./output    # Where to save results
```

### HR Keywords

You can customize the HR-related keywords in `config.py`:

```python
HR_KEYWORDS = [
    'Human Resources',
    'HR Manager',
    'Recruiter',
    'Talent Acquisition',
    # Add more keywords...
]
```

## Output

Results are saved in the `output/` directory with timestamps:

```
output/
├── linkedin_hr_Google_20231115_143022.csv
├── linkedin_hr_Microsoft_20231115_143525.json
└── linkedin_hr_Amazon_20231115_144101.xlsx
```

### Output Fields

Each result includes:
- **Name**: Full name of the person
- **Title**: Current job title
- **Location**: Geographic location
- **Profile URL**: Direct link to LinkedIn profile

### Example CSV Output

```csv
name,title,location,profile_url
John Doe,Senior HR Manager,San Francisco Bay Area,https://www.linkedin.com/in/johndoe
Jane Smith,Talent Acquisition Partner,New York City,https://www.linkedin.com/in/janesmith
```

### Example JSON Output

```json
{
  "company": "Google",
  "scraped_at": "2023-11-15T14:30:22",
  "total_profiles": 45,
  "profiles": [
    {
      "name": "John Doe",
      "title": "Senior HR Manager",
      "location": "San Francisco Bay Area",
      "profile_url": "https://www.linkedin.com/in/johndoe"
    }
  ]
}
```

## Important Notes & Best Practices

### ⚠️ Legal & Ethical Considerations

1. **LinkedIn Terms of Service**: This tool is for educational purposes. Be aware that automated scraping may violate LinkedIn's Terms of Service.

2. **Rate Limiting**: The scraper includes delays to avoid overwhelming LinkedIn's servers. Don't modify these without good reason.

3. **Privacy**: Respect people's privacy. Don't use this data for spam or unauthorized marketing.

4. **Account Safety**:
   - Use a secondary LinkedIn account if possible
   - Don't run excessive searches in short periods
   - Your account may be temporarily restricted if you scrape too aggressively

### 🛡️ Security

- Never commit your `.env` file to version control
- Use environment variables for sensitive data
- Consider using LinkedIn's official API for production use

### 🐛 Troubleshooting

**Problem: Login fails or CAPTCHA appears**
- Solution: Run in non-headless mode and manually solve the CAPTCHA
- The script will wait 10 seconds for you to handle it

**Problem: No results found**
- Check company name spelling
- LinkedIn Premium accounts may get better search results
- Try running with fewer max results first

**Problem: ChromeDriver errors**
- The script automatically downloads the correct ChromeDriver
- Ensure Google Chrome is installed and up to date

**Problem: Elements not found**
- LinkedIn frequently changes its HTML structure
- You may need to update the CSS selectors in `linkedin_scraper.py`

## Project Structure

```
Search_linkedin_hrs/
├── Core Scraping
│   ├── main.py                      # Basic scraper CLI
│   ├── linkedin_scraper.py          # Core scraping engine
│   ├── data_exporter.py             # Export to CSV/JSON/Excel
│   └── config.py                    # Configuration & HR keywords
│
├── Message Generation & Outreach
│   ├── complete_workflow.py         # Complete scrape+message+send workflow
│   ├── message_generator.py         # AI-powered message generation
│   ├── message_service.py           # Flask API for message generation
│   └── linkedin_messenger.py        # LinkedIn message sending integration
│
├── n8n Integration
│   └── n8n_workflows/
│       └── linkedin_hr_messaging_workflow.json  # n8n workflow template
│
├── Utilities & Examples
│   ├── utils.py                     # Environment validation utilities
│   ├── example_usage.py             # Code examples
│   └── setup.sh                     # Automated setup script
│
├── Documentation
│   ├── README.md                    # Main documentation (this file)
│   ├── QUICKSTART.md                # Quick start guide
│   └── N8N_INTEGRATION_GUIDE.md     # Complete n8n integration guide
│
├── Configuration
│   ├── .env.example                 # Example environment variables
│   ├── .env                         # Your credentials (gitignored)
│   ├── .gitignore                   # Git ignore rules
│   └── requirements.txt             # Python dependencies
│
└── output/                          # Generated files (gitignored)
    ├── linkedin_hr_*.csv            # Scraped profiles (CSV)
    ├── linkedin_hr_*.json           # Scraped profiles (JSON)
    ├── messages_*.json              # Generated messages
    └── workflow_*.json              # n8n workflow files
```

## Advanced Usage

### Custom Search

Modify `linkedin_scraper.py` to customize search behavior:

```python
# Change the number of HR keywords to search
for keyword in config.HR_KEYWORDS[:10]:  # Search more keywords
    # ... search logic
```

### Programmatic Usage

Use the scraper in your own Python code:

```python
from linkedin_scraper import LinkedInScraper
from data_exporter import DataExporter

# Initialize
scraper = LinkedInScraper(email="your_email", password="your_pass")
scraper.setup_driver()
scraper.login()

# Search
results = scraper.search_hr_personnel("Google", max_results=100)

# Export
exporter = DataExporter()
exporter.export_to_csv(results, "Google")

# Cleanup
scraper.close()
```

## Limitations

- LinkedIn may limit search results for free accounts
- Some profiles may be hidden or private
- Search results depend on your LinkedIn network and account type
- LinkedIn's HTML structure changes frequently, requiring updates

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Disclaimer

This tool is for educational and research purposes only. Users are responsible for complying with LinkedIn's Terms of Service and applicable laws. The authors are not responsible for any misuse of this tool.

## License

MIT License - feel free to use and modify as needed.

## Support

If you encounter issues:

1. Check the Troubleshooting section above
2. Review LinkedIn's current HTML structure
3. Open an issue on GitHub with:
   - Error message
   - Steps to reproduce
   - Your Python version
   - Your Chrome version

## Roadmap

Future enhancements:
- [ ] Support for other job roles (Sales, Engineering, etc.)
- [ ] Profile detail extraction (email, phone if available)
- [ ] Connection request automation (with user approval)
- [ ] Better CAPTCHA handling
- [ ] Proxy support
- [ ] Multi-threading for faster scraping
- [ ] GUI interface

---

**Happy Scraping! 🚀**

Remember to use this tool responsibly and ethically.
