# RotaryRadar.AI
small app to assist Rotary Clubs to tailor local sources (websites) to crawl for Rotary Opportunities using AI.

This application consists of 2 main python apps.

## 1. main.py 
run ```python main.py``` in the terminal

executing this runs a "scan" and exports; it will have an option to PDF export from terminal so you don't have to run the web.py browser GUI instance.

## 2. web.py 
run ```python web.py``` in the terminal, (keep terminal open while using web browser)

spins up a web browser GUI where you can see all your database results and choose from various views/print options.  Required to see results. Requires for user to open a web browser and go to http://127.0.0.1:5000 after executing web.py

# Set up your environment and requirements
1. set up your chat GPT api key in your .env (and other keys)
2. ```pip install -r requirements.txt``` to install python modules in your env

# Executing A radar scan
3. run ```python main.py```

# Adding sources - sources.yaml
sources are in the sources.yaml file in the root directory.  The sources are organized by scanning optimazation operation.
## urls
any url you want to hit up and scan.  Will only scan that page and will not gather any other information.  Good for sites that have a daily page.

## full_story_depth1:
Some source URLs, such as forums or municipal websites, may not update frequently but often contain summarized posts with hyperlinks labeled "Full Story" that lead to the complete article.
For example, https://www.gurnee.il.us/news displays news headlines that expand to full articles when "Full Story" is clicked. These links typically follow a YYYY/MM/DD format in the URL.

This program automatically clicks all "Full Story" links found on pages defined in the day_rules_limit section and evaluates the date embedded in each link. It only retrieves content published within the last 7 days, helping reduce API usage and avoid collecting outdated or irrelevant data.



