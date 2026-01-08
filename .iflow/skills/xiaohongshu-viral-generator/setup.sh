#!/bin/bash
# Setup script for Xiaohongshu Viral Generator
# Installs dependencies and initializes the skill

set -e

echo "🚀 Setting up Xiaohongshu Viral Generator..."
echo ""

# Create required directories
echo "📁 Creating directory structure..."
mkdir -p output logs assets/themes

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Set executable permissions
echo "🔧 Setting permissions..."
chmod +x scripts/*.py

# Check for API keys
echo ""
echo "⚙️  Configuration Check:"
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  OPENAI_API_KEY not set. AI image generation will not work."
    echo "   Set it with: export OPENAI_API_KEY='your-api-key'"
else
    echo "✅ OPENAI_API_KEY is set"
fi

if [ -z "$XIAOHONGSHU_API_KEY" ]; then
    echo "⚠️  XIAOHONGSHU_API_KEY not set. Posting feature will be disabled."
    echo "   Set it with: export XIAOHONGSHU_API_KEY='your-api-key'"
else
    echo "✅ XIAOHONGSHU_API_KEY is set"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "📖 Quick Start:"
echo "   # Generate today's content (preview mode)"
echo "   python scripts/main.py daily --preview"
echo ""
echo "   # Generate content with AI images"
echo "   python scripts/main.py daily"
echo ""
echo "   # Start scheduler (8:00 AM daily)"
echo "   python scripts/main.py schedule --time 08:00"
echo ""
echo "📖 Full documentation: See SKILL.md"
