import boto3
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def upload_to_s3(date_str, articles):
    """Upload daily results to S3 as static HTML files"""
    
    # Use default AWS CLI credentials (from ~/.aws/credentials)
    # Or fall back to environment variables if set
    s3 = boto3.client('s3', region_name='us-east-1')
    
    bucket = 'rotaryradar-gurnee.aguero.tech'
    
    # Generate daily results HTML
    daily_html = generate_daily_html(date_str, articles)
    
    # Upload daily file (e.g., 20260112.html)
    s3.put_object(
        Bucket=bucket,
        Key=f'{date_str}.html',
        Body=daily_html,
        ContentType='text/html',
        CacheControl='no-cache, no-store, must-revalidate'
    )
    
    print(f"✅ Uploaded {date_str}.html to S3")
    
    # Get list of all HTML files to build index
    all_dates = get_all_date_files(s3, bucket)
    
    # Update index.html with link to all dates
    index_html = generate_index_html(all_dates)
    s3.put_object(
        Bucket=bucket,
        Key='index.html',
        Body=index_html,
        ContentType='text/html',
        CacheControl='no-cache, no-store, must-revalidate'
    )
    
    print(f"✅ Updated index.html")
    print(f"🌐 View at: https://rotaryradar-gurnee.aguero.tech/")

def get_all_date_files(s3, bucket):
    """Get all date-formatted HTML files from S3 bucket"""
    response = s3.list_objects_v2(Bucket=bucket)
    dates = []
    
    if 'Contents' in response:
        for obj in response['Contents']:
            key = obj['Key']
            # Match files like 20260112.html
            if key.endswith('.html') and len(key) == 13 and key[:8].isdigit():
                dates.append(key[:-5])  # Remove .html extension
    
    # Sort dates in descending order (newest first)
    dates.sort(reverse=True)
    return dates

def generate_daily_html(date_str, articles):
    """Generate HTML for daily results page"""
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Rotary Radar - {date_str}</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{ 
            font-family: Arial, sans-serif; 
            max-width: 1200px; 
            margin: 0 auto; 
            padding: 20px; 
            background: #f5f5f5;
        }}
        h1 {{ 
            color: #2c3e50; 
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        .article {{ 
            background: white;
            border: 1px solid #ddd; 
            padding: 20px; 
            margin: 15px 0; 
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .article h3 {{ 
            color: #3498db; 
            margin-top: 0;
        }}
        .article h3 a {{
            text-decoration: none;
            color: #3498db;
        }}
        .article h3 a:hover {{
            text-decoration: underline;
        }}
        .source {{ 
            color: #7f8c8d; 
            font-size: 0.9em; 
            margin: 5px 0;
        }}
        .ai-suggestion {{ 
            background: #e8f5e9; 
            padding: 15px; 
            margin-top: 10px; 
            border-radius: 5px;
            border-left: 4px solid #4caf50;
            line-height: 1.8;
            white-space: pre-wrap;
        }}
        .back-link {{
            display: inline-block;
            margin-bottom: 20px;
            color: #3498db;
            text-decoration: none;
        }}
        .back-link:hover {{
            text-decoration: underline;
        }}
        .credit {{
            text-align: center;
            color: #7f8c8d;
            font-size: 0.9em;
            margin-bottom: 20px;
        }}
        .credit a {{
            color: #3498db;
            text-decoration: none;
        }}
        .credit a:hover {{
            text-decoration: underline;
        }}
        .count {{
            color: #7f8c8d;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <a href="index.html" class="back-link">← Back to Index</a>
    <div class="credit">
        <p>Powered by <a href="https://www.aguero.tech" target="_blank">aguero.tech</a></p>
    </div>
    <h1>Rotary Radar - {date_str}</h1>
    <p class="count">Found {len(articles)} articles</p>
"""
    
    if not articles:
        html += """
    <div class="article">
        <p>No articles found for today. Check back tomorrow!</p>
    </div>
"""
    else:
        for article in articles:
            html += f"""
    <div class="article">
        <h3><a href="{article.get('url', '#')}" target="_blank">{article.get('title', 'No Title')}</a></h3>
        <p class="source">Source: {article.get('source', 'Unknown')}</p>
        <p>{article.get('snippet', 'No description available.')}</p>
"""
            if article.get('ai_suggestion'):
                # Preserve line breaks and formatting in AI suggestions
                suggestion = article['ai_suggestion'].replace('<', '&lt;').replace('>', '&gt;')
                html += f"""
        <div class="ai-suggestion">
            <strong>🤖 AI Suggestion:</strong><br><br>
            {suggestion}
        </div>
"""
            html += "    </div>\n"
    
    html += """
</body>
</html>"""
    return html

def generate_index_html(all_dates):
    """Generate index page with links to all date results"""
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Rotary Radar - Gurnee IL - District: 6440</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{ 
            font-family: Arial, sans-serif; 
            max-width: 800px; 
            margin: 0 auto; 
            padding: 20px;
            background: #f5f5f5;
        }}
        .container {{
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{ 
            color: #2c3e50; 
            text-align: center;
            margin-bottom: 10px;
        }}
        .subtitle {{
            text-align: center;
            color: #7f8c8d;
            margin-bottom: 20px;
        }}
        .link {{
            text-align: center;
            margin-bottom: 40px;
        }}
        .link a {{
            color: #3498db;
            text-decoration: none;
        }}
        .link a:hover {{
            text-decoration: underline;
        }}
        .intro {{
            text-align: center;
            margin: 30px 0;
            line-height: 1.6;
        }}
        .tagline {{
            text-align: center;
            color: #7f8c8d;
            font-style: italic;
            margin: 20px 0;
        }}
        .support {{
            text-align: center;
            margin: 30px 0;
            font-weight: bold;
        }}
        .support-links {{
            text-align: center;
            margin-bottom: 30px;
        }}
        .support-links a {{
            color: #3498db;
            text-decoration: none;
            margin: 0 10px;
        }}
        .support-links a:hover {{
            text-decoration: underline;
        }}
        .contribute {{
            text-align: center;
            margin-bottom: 40px;
        }}
        .contribute a {{
            color: #3498db;
            text-decoration: none;
        }}
        .date-list {{
            border-top: 2px solid #e0e0e0;
            padding-top: 20px;
        }}
        .date-list ul {{
            list-style: none;
            padding: 0;
        }}
        .date-list li {{
            margin: 10px 0;
            text-align: center;
        }}
        .date-list a {{
            display: inline-block;
            padding: 10px 20px;
            background: #f8f9fa;
            border-radius: 5px;
            color: #3498db;
            text-decoration: none;
            transition: background 0.2s;
            min-width: 150px;
        }}
        .date-list a:hover {{
            background: #e9ecef;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Rotary Radar - Gurnee IL - District: 6440</h1>
        
        <div class="link">
            <a href="http://www.aguero.tech" target="_blank">www.aguero.tech</a>
        </div>
        
        <div class="intro">
            <p>Rotary Radar is a free civic resource built to help communities serve. <strong>#serviceaboveself</strong></p>
            <p>If you'd like to support this effort:</p>
        </div>
        
        <div class="support-links">
            <a href="https://paypal.me/yourusername" target="_blank">Donate via PayPal</a> | 
            <a href="https://venmo.com/yourusername" target="_blank">Donate via Venmo</a>
        </div>
        
        <div class="contribute">
            <p>or by contributing on<br>
            <a href="https://github.com/mannydgaguero/RotaryRadar.AI" target="_blank">GitHub - RotaryRadar.AI</a></p>
        </div>
        
        <hr style="margin: 40px 0; border: none; border-top: 2px solid #e0e0e0;">
        
        <div class="date-list">
            <ul>
"""
    
    # Add all dates as links
    for date in all_dates:
        html += f'                <li><a href="{date}.html">{date}</a></li>\n'
    
    html += """            </ul>
        </div>
    </div>
</body>
</html>"""
    return html
