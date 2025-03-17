from time import sleep
from functions.file_operations import add_path_to_csv
from config import FILE_PATH
import random
import logging
from functions.screenshot import take_screenshot

logging.basicConfig(
    filename="app.log",  # Log file name
    level=logging.INFO,  # Set logging level
    format="%(asctime)s - %(levelname)s - %(message)s"  # Log format
)

def print_log(context):
    logging.info(context)
    
def human_pause(page):
    page.wait_for_timeout(random.randint(800, 3000))

def select_unused_link_from_search_results(page):
    
    take_screenshot(page, "After_search_fill")
    page.wait_for_timeout(random.randint(3000, 5000))
    # Find all "a" tags with the role="link"
    links = page.query_selector_all('a[role="link"]')

    flag = False
    # Loop through each link and click on it
    for index, link in enumerate(links):
        href = link.get_attribute('href')  # Get the href attribute
        print(href)

        # if add_path_to_csv(FILE_PATH, href) == False: continue
        flag = True
        
        human_pause(page)
        # link.click()  # Click the link
        page.goto(href)
        human_pause(page)
        break

    if flag == True: print_log("correctly selected link")
    else : print_log("fail selecting")
    result = {
        'flag': flag,
        'href': href,
        'page': page,
    }
    return result