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

def perform_login(page, email, password):
    # Select the username input field and type username to it.
    username_input = page.wait_for_selector("input[name='username']", timeout=0)
    human_pause(page)

    username_input.click()
    human_pause(page)

    for char in email:
        page.keyboard.press(char)
        page.wait_for_timeout(random.randint(100, 200))

    human_pause(page)

    # Select the password input field and type password to it.
    page.click("input[name='password']")
    human_pause(page)

    for char in password:
        page.keyboard.press(char)
        page.wait_for_timeout(random.randint(100, 200))

    human_pause(page)
    
    # Click the login button
    page.click("button[type='submit']")
    human_pause(page)

    page.wait_for_url("https://www.instagram.com/explore/")
    print_log("Corretly logined")