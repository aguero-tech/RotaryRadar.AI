# RotaryRadar.AI

AI-powered web scraper to help Rotary Clubs discover local community service opportunities by analyzing news sources. Automatically scans local news websites daily, uses GPT-4 to identify potential Rotary projects, and publishes results to a static website.

**Live Example**: [rotaryradar-gurnee.aguero.tech](https://rotaryradar-gurnee.aguero.tech/)

## Features

- 🤖 **AI-Powered Analysis**: Uses OpenAI GPT-4 to analyze articles and suggest relevant Rotary service opportunities
- 🌐 **Automated Scraping**: Scrapes multiple local news sources with customizable URL patterns
- 📅 **Dynamic Date Handling**: Automatically updates URLs with today's date (e.g., Daily Herald archives)
- 📊 **Web Dashboard**: Flask-based interface to view and export results
- ☁️ **S3 Publishing**: Automatically generates and uploads static HTML reports to S3/CloudFront
- 🗓️ **Daily Automation**: Cron-ready for scheduled daily scans

## Prerequisites

- Python 3.12+
- Chrome/Chromium browser (for Selenium)
- AWS Account (for S3 hosting)
- OpenAI API Key
- AWS CLI configured

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/mannydgaguero/RotaryRadar.AI.git
cd RotaryRadar.AI
```

### 2. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r app/requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the root directory:
```bash
OPENAI_API_KEY=your-openai-api-key-here

# AWS credentials are loaded from ~/.aws/credentials (configured with 'aws configure')
# No need to set AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY here
```

### 5. Configure AWS CLI

```bash
aws configure
# Enter your AWS Access Key ID
# Enter your AWS Secret Access Key
# Default region name: us-east-1
# Default output format: json
```

### 6. Set up S3 bucket

```bash
# Enable static website hosting
aws s3 website s3://your-bucket-name/ --index-document index.html --error-document index.html

# Update bucket name in s3_upload.py (line 15)
bucket = 'your-bucket-name'
```

## Configuration

### sources.yaml

Configure the news sources to scrape in `sources.yaml`:

```yaml
urls:
  # Use {TODAY} placeholder for dynamic dates (YYYYMMDD format)
  - "https://www.dailyherald.com/archive/{TODAY}/"
  - "https://www.chicagotribune.com/lake-county-news-sun/"
  - "https://patch.com/illinois/grayslake"

full_story_depth1:
  # Sites with "Full Story" links - scrapes articles from last 7 days
  - "https://www.gurnee.il.us/news"
```

**URL Types:**
- **urls**: Direct scraping - captures entire page content
- **full_story_depth1**: Clicks "Full Story" links and scrapes linked pages (filters by date in URL)

## Usage

### Run a scan manually

```bash
# Activate virtual environment
source venv/bin/activate

# Run the scraper and upload to S3
python3 main.py
```

This will:
1. Scrape all configured news sources
2. Analyze articles with GPT-4
3. Store results in SQLite database (`rotary.db`)
4. Generate HTML reports
5. Upload to S3
6. Update the index page

### View results locally

Start the Flask web server:
```bash
python3 web.py
```

Then open http://127.0.0.1:5000 in your browser.

### Automated Daily Scans

Set up a cron job to run daily at 8 AM:

```bash
crontab -e
```

Add this line:
```bash
0 8 * * * cd /path/to/RotaryRadar.AI && /path/to/venv/bin/python3 main.py >> /tmp/rotaryradar.log 2>&1
```

## Project Structure

```
RotaryRadar.AI/
├── main.py                 # Main entry point - runs scraper, analyzer, and S3 upload
├── web.py                  # Flask web interface
├── s3_upload.py           # S3 upload and HTML generation
├── sources.yaml           # News source configuration
├── .env                   # Environment variables (not in git)
├── rotary.db              # SQLite database (generated)
├── app/
│   ├── scraper.py        # Web scraping logic with Selenium
│   ├── analyzer.py       # GPT-4 analysis
│   ├── db.py             # Database operations
│   └── day_url_limit.py  # Date filtering for URLs
└── templates/            # HTML templates for Flask
```

## How It Works

1. **Scraping**: Uses Selenium with headless Chrome to scrape configured news sources
2. **Content Analysis**: Sends article content to OpenAI GPT-4 with a custom prompt focused on identifying Rotary service opportunities
3. **Storage**: Saves articles and AI suggestions to SQLite database
4. **Publishing**: Generates static HTML files and uploads to S3
   - Daily reports: `YYYYMMDD.html`
   - Index page: `index.html` (lists all reports)
5. **Hosting**: Served via S3 static website + CloudFront CDN

## CloudFront Cache Management

The system automatically handles cache invalidation:
- Uploads include `CacheControl='no-cache'` headers
- No manual cache invalidation needed for daily updates

If you need to manually invalidate:
```bash
aws cloudfront create-invalidation --distribution-id YOUR_DIST_ID --paths "/*.html"
```

## Contributing

Contributions welcome! Areas for improvement:
- Additional news source parsers
- RSS feed support
- Email notifications
- Enhanced AI prompt engineering
- Additional export formats

## License

See [LICENSE](LICENSE) file.

## Support

If this project helps your Rotary club, consider:
- ⭐ Starring the repo on GitHub
- 🐛 Reporting bugs or suggesting features
- 💻 Contributing code improvements
- 📣 Sharing with other Rotary clubs

**#ServiceAboveSelf**



