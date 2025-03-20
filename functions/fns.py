import random
import logging
import re
import os
import csv
import json

logging.basicConfig(
    filename="app.log",  # Log file name
    level=logging.INFO,  # Set logging level
    format="%(asctime)s - %(levelname)s - %(message)s"  # Log format
)

cookies_file = "cookies.json"

def save_cookies(context):
    # Save cookies to a file
    with open(cookies_file, 'w') as f:
        json.dump(context.storage_state(), f)

def load_cookies(context):
    # Load cookies from a file, if it exists
    if os.path.exists(cookies_file):
        with open(cookies_file, 'r') as f:
            state = json.load(f)
            # The `cookies` key contains the array of cookies
            cookies = state.get('cookies', [])
            context.add_cookies(cookies)  # Correctly add cookies as an array

# ==== fn for print log ====
def print_log(context):
    logging.info(context)

# ==== fn for mouse move action ====
def move_mouse(page, target_elem_query, real_elem = None):
    try:
        if target_elem_query == None and real_elem != None:
            target_elem = real_elem
        else:
            target_elem = page.locator(target_elem_query)
        box = target_elem.bounding_box()
        x, y = box["x"] + box["width"] / 2, box["y"] + box["height"] / 2
        page.mouse.move(x, y, steps=random.randint(40, 80))
    except Exception as e:
        pass

# ==== fn for human pause ====
def human_pause(page):
    page.wait_for_timeout(random.randint(800, 3000))

# ==== fn for capture real words from url ====
def extract_word(url):
    match = re.search(r'/([^/]+)/?$', url)
    if match:
        return match.group(1)
    return None

# ==== fn for save screenshot of page ====
def take_screenshot(page, step):
    screenshot_path = f"screenshots/{step}.png"
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")
    page.screenshot(path=screenshot_path)
    print_log(f"Screenshot saved: {screenshot_path}")

# ==== fn for save data to csv file ====
def add_path_to_csv(file_path, new_path):
    try:
        file_exists = os.path.exists(file_path)
        data = []
        
        if file_exists:
            with open(file_path, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file, delimiter=' ')
                data = list(reader)
                if any(row["Path"] == new_path for row in data):
                    return False

        new_no = int(data[-1]["No"]) + 1 if data else 1
        with open(file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=' ')
            if not file_exists:
                writer.writerow(["No", "Path"])
            writer.writerow([new_no, new_path])
            print_log("correctly added path")
            return True
    except Exception as e:
        return False