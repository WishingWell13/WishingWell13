#!/bin/bash

# LinkedIn Profile Scraper Demo Script
# This demonstrates how to use the LinkedIn scraper

echo "🔍 LinkedIn Profile Scraper Demo"
echo "================================="
echo

echo "📝 Installing dependencies..."
pip install -r requirements.txt --quiet

echo
echo "🚀 Running LinkedIn profile extraction..."
python3 linkedin_scraper.py

echo
echo "📊 Showing extracted profile information:"
echo "----------------------------------------"
if [ -f "linkedin_profile_info.json" ]; then
    python3 -c "
import json
with open('linkedin_profile_info.json', 'r') as f:
    data = json.load(f)
for key, value in data.items():
    print(f'✓ {key.replace(\"_\", \" \").title()}: {value}')
"
else
    echo "❌ Profile information file not found"
fi

echo
echo "📋 README.md has been updated with LinkedIn information!"
echo "✅ Demo completed successfully!"