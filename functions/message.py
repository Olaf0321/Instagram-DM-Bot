from time import sleep
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

def send_message(page, message):
    take_screenshot(page, "After_click_message_btn")
    msg_input = 'div[aria-label="Message"][contenteditable="true"]'
    # Wait for the div element with the aria-label="Message" and contenteditable="true"
    page.wait_for_selector(msg_input, timeout=0)
    human_pause(page)
    
    # Select the element after it appears and click it
    div_element = page.locator(msg_input)
    div_element.click()
    human_pause(page)

    for char in message:
        page.keyboard.press(char)
        page.wait_for_timeout(random.randint(100, 200))

    human_pause(page)

    print_log("correctly entered message")

    send_btn = 'div[role="button"]:has-text("Send")'

    # Wait for the div element with the "Send" text and role="button"
    page.wait_for_selector(send_btn, timeout=0)
    human_pause(page)
    
    # Select the element after it appears and click it
    # send_button = page.locator(send_btn)
    # send_button.click()
    human_pause(page)
    print_log("correctly sended message")