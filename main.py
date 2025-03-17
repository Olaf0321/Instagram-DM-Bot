from playwright.sync_api import sync_playwright
from functions.login import perform_login
from functions.search import click_search_icon, fill_search_input
from functions.link_selector import select_unused_link_from_search_results
from functions.validation import validate_user_selection
from functions.message import send_message
from functions.screenshot import take_screenshot
from time import sleep
from config import LOGIN_URL
import random
import logging
logging.basicConfig(
    filename="app.log",  # Log file name
    level=logging.INFO,  # Set logging level
    format="%(asctime)s - %(levelname)s - %(message)s"  # Log format
)


def print_log(context):
    logging.info(context)

def human_pause(page):
    page.wait_for_timeout(random.randint(800, 3000))

def perform_automation_DM(email, password, link, keyword, message, search_words, dms_hours):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(LOGIN_URL)

        take_screenshot(page, 'main_page')

        human_pause(page)

        perform_login(page, email, password)  # login into Instagram
        human_pause(page)

        while 1:
            click_search_icon(page)
            human_pause(page)

            fill_search_input(page, search_words)
            human_pause(page)

            result = select_unused_link_from_search_results(page)  # Refactor the function properly
            page = result['page']

            human_pause(page)


            if result['flag'] == False:
                continue

            if validate_user_selection(page, link, keyword) == True:
                human_pause(page)
                print_log("correctly checked: validate")

                page.wait_for_url(result['href'], timeout=0)
                # Wait for the div element with the text "Message" and role="button" to appear
                page.wait_for_selector('div[role="button"]:has-text("Message")', timeout=0)
                human_pause(page)

                # Select the element after it appears and click it
                div_element = page.locator('div[role="button"]:has-text("Message")')
                div_element.click()
                human_pause(page)
                print_log("correctly clicked message button!")

            else:
                print_log("fail checked: unvalidate")
                continue

            human_pause(page)
            send_message(page, message)
            human_pause(page)
            
            if dms_hours == "50DMs/24Hours":
                # sleep(1728)
                human_pause(page)
            elif dms_hours == "25DMs/12Hours":
                # sleep(1728)
                human_pause(page)
            elif dms_hours == "10DMs/8Hours":
                # sleep(2880)
                human_pause(page)

        browser.close()