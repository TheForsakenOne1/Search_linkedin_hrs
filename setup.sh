#!/bin/bash

echo "╔══════════════════════════════════════════════════════════╗"
echo "║      LinkedIn HR Scraper - Setup Script                ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip."
    exit 1
fi

echo "✓ pip3 found"
echo ""

# Create virtual environment (optional but recommended)
read -p "Do you want to create a virtual environment? (recommended) [y/n]: " create_venv

if [ "$create_venv" = "y" ] || [ "$create_venv" = "Y" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
    echo ""
    echo "To activate it, run:"
    echo "  source venv/bin/activate  # On Linux/Mac"
    echo "  venv\\Scripts\\activate     # On Windows"
    echo ""

    # Activate virtual environment
    source venv/bin/activate 2>/dev/null || . venv/bin/activate
fi

# Install requirements
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""

# Setup .env file
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✓ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env file and add your LinkedIn credentials:"
    echo "   - LINKEDIN_EMAIL"
    echo "   - LINKEDIN_PASSWORD"
    echo ""
else
    echo "✓ .env file already exists"
    echo ""
fi

# Create output directory
mkdir -p output
echo "✓ Output directory created"
echo ""

# Make scripts executable
chmod +x main.py
chmod +x example_usage.py
chmod +x setup.sh

echo "✓ Scripts made executable"
echo ""

# Run environment check
echo "Running environment check..."
python3 utils.py --check

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║              Setup Complete!                            ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "Next steps:"
echo "  1. Edit .env file with your LinkedIn credentials"
echo "  2. Run: python3 main.py --company \"Google\""
echo "  3. Check output/ directory for results"
echo ""
echo "For more information, see:"
echo "  - README.md (full documentation)"
echo "  - QUICKSTART.md (quick start guide)"
echo ""
