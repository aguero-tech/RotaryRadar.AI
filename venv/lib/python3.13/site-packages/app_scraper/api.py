from app_scraper import scraper
# import scraper

def details(app_id,hl="en", gl="us"):
    """Sends a GET request to the app's info page, parses the app's details, and
    returns them as a dict.
    :param app_id: the app to retrieve details from, e.g. 'com.nintendo.zaaa'
    :return: a dictionary of app details
    """
    s = scraper.AppScraper(hl, gl)
    return s.details(app_id)

# if __name__ == "__main__":
#     crawler = scraper.AppScraper(website='xpose repo')
#     crawler.details('com.devadvance.rootcloak2')