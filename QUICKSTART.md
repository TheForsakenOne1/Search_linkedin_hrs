# Quick Start Guide

Get up and running with LinkedIn HR Scraper in 5 minutes!

## 🚀 Quick Setup

### Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Configure Your Credentials

```bash
# Copy the example file
cp .env.example .env
```

Then edit `.env` and add your LinkedIn credentials:

```env
LINKEDIN_EMAIL=your_email@example.com
LINKEDIN_PASSWORD=your_password
```

### Step 3: Run Your First Search

```bash
python main.py --company "Google" --max-results 20
```

That's it! Your results will be saved in the `output/` directory.

## 📋 Common Use Cases

### Use Case 1: Find HR Contacts for Job Application

```bash
# Search for HR at your target company
python main.py --company "Microsoft" --max-results 30 --format excel
```

Then use the Excel file to find the right person to contact about job opportunities.

### Use Case 2: Recruitment Research

```bash
# Get a comprehensive list of hiring team
python main.py --company "Amazon" --max-results 100 --format all
```

This exports to CSV, JSON, and Excel for different uses.

### Use Case 3: Market Research

```bash
# Compare hiring teams at different companies
python main.py --company "Google"
python main.py --company "Meta"
python main.py --company "Apple"
```

### Use Case 4: Silent Mode (No Browser Window)

```bash
# Run without showing the browser
python main.py --company "Netflix" --headless
```

## 🎯 Interactive Mode

For beginners, just run:

```bash
python main.py
```

You'll be guided through:
1. Entering company name
2. Choosing max results
3. Selecting export format

## ⚡ Pro Tips

1. **Start Small**: Begin with `--max-results 20` to test
2. **Save Your Credentials**: Keep `.env` file secure and never share it
3. **Check Output**: Results are in `output/` directory
4. **Be Patient**: Scraping takes time due to rate limiting
5. **Use Secondary Account**: Consider using a non-primary LinkedIn account

## 🔧 Troubleshooting Quick Fixes

**Chrome/ChromeDriver issues?**
```bash
# Make sure Chrome is installed
google-chrome --version  # or chrome --version

# The script will auto-download the right driver
```

**Login not working?**
- Try running without `--headless` to see what's happening
- Check if you need to solve a CAPTCHA manually
- Verify your credentials in `.env` file

**No results?**
- Double-check company name spelling
- Try with a well-known company first (Google, Microsoft, etc.)
- Ensure your LinkedIn account is active and not restricted

## 📊 Understanding Output Files

All files are saved with timestamps in the `output/` directory:

- **CSV**: Best for spreadsheet analysis
- **JSON**: Best for programming/API integration
- **Excel**: Best for sharing with non-technical users

Example filename: `linkedin_hr_Google_20231115_143022.csv`
- Format: `linkedin_hr_{company}_{timestamp}.{extension}`

## 🎓 Next Steps

Once you're comfortable with basic usage:

1. Read the full README.md for advanced options
2. Customize HR keywords in `config.py`
3. Explore the source code to understand how it works
4. Consider contributing improvements!

## ⚠️ Remember

- Use responsibly and ethically
- Respect LinkedIn's Terms of Service
- Don't spam or harass people
- This is for research and legitimate networking

---

Need more help? Check the full [README.md](README.md) for detailed documentation.
