#!/bin/bash
# Setup script for Xiaohongshu Daily Autoposter

echo "🚀 Setting up Xiaohongshu Daily Autoposter..."

# Create output directory
mkdir -p output/logs

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Make scripts executable
chmod +x scripts/*.py

# Create cron job for daily execution (optional)
echo "⏰ Would you like to set up automatic daily execution? (y/n)"
read -r setup_cron

if [ "$setup_cron" = "y" ] || [ "$setup_cron" = "Y" ]; then
    echo "Enter daily execution time (default: 08:00):"
    read -r exec_time
    exec_time=${exec_time:-08:00}
    
    # Add cron job
    cron_job="0 ${exec_time#*:} * * * cd $(pwd) && python scripts/autoposter.py --mode daily >> output/logs/cron.log 2>&1"
    
    # Get current crontab and add new job
    (crontab -l 2>/dev/null | grep -v "autoposter.py" || true; echo "$cron_job") | crontab -
    
    echo "✅ Cron job set up! Daily execution at ${exec_time}"
    echo "📋 Current crontab:"
    crontab -l
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Usage examples:"
echo "  # Generate today's content"
echo "  python scripts/autoposter.py --mode daily"
echo ""
echo "  # Generate specific topic"
echo "  python scripts/autoposter.py --mode generate --topic '职场效率'"
echo ""
echo "  # Start scheduler"
echo "  python scripts/autoposter.py --mode schedule --time 08:00"
echo ""
echo "  # Manual trigger"
echo "  python scripts/autoposter.py --trigger-now"
