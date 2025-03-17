import random
import string
from time import sleep
import logging
from functions.screenshot import take_screenshot

logging.basicConfig(
    filename="app.log",  # Log file name
    level=logging.INFO,  # Set logging level
    format="%(asctime)s - %(levelname)s - %(message)s"  # Log format
)

def print_log(context):
    logging.info(context)

def generate_random_string(L):
    """Generate a random English string of length L."""
    return ''.join(random.choices(string.ascii_letters, k=L))

def choose_words(search_words):
    if search_words == '':
        return generate_random_string(2)
    else:
        words = search_words.split(',')
        return words[random.randint(0, len(words)-1)]

def human_pause(page):
    page.wait_for_timeout(random.randint(800, 3000))

def click_search_icon(page):
    take_screenshot(page, "After_login")
    # Todo: fix class issue
    search_selector = "a:has(svg[aria-label='Search'])"
    # Wait for the element to be visible using all class names of 'a' tag
    page.wait_for_selector(search_selector, timeout=0)
    human_pause(page)
    
    # Click the element
    page.click(search_selector)
    human_pause(page)
    print_log("correctly clicked search icon")

def fill_search_input(page, search_words):
    chosen_word = choose_words(search_words)
    print_log(f"chosen word: {chosen_word}")

    take_screenshot(page, "After_search_icon_click")
    search_input_arial_label = 'Search input'
    # Wait for the search input field to be visible using aria-label
    page.wait_for_selector(f"input[aria-label='{search_input_arial_label}']", timeout=0)
    human_pause(page)

    # Click the search input field
    page.click(f"input[aria-label='{search_input_arial_label}']")
    human_pause(page)

    for char in chosen_word:
        page.keyboard.press(char)
        page.wait_for_timeout(random.randint(100, 200))
    
    human_pause(page)
    print_log("correctly filled search input")