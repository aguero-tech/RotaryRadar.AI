#!/bin/bash

# RotaryRadar.AI Daily Scan Script
# Runs the scraper, analyzer, and uploads to S3

# Set working directory
cd /home/manny/Desktop/Repos/RotaryRadar.AI

# Activate virtual environment
source venv/bin/activate

# Run the main scraper
python3 main.py

# Log completion
echo "RotaryRadar scan completed at $(date)" >> /tmp/rotaryradar.log
