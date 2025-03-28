import random
import os
import sys
from config import *
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pyperclip
import csv

from functions.choose_words import choose_words
from functions.fns import *

# Setup Chrome driver
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(options=options)
actions = ActionChains(driver)

def human_delay(min_time, max_time):
    """Adds a random delay to mimic human behavior."""
    time.sleep(random.uniform(min_time, max_time))

def login_instagram(email, password):
    """Logs into Instagram with human-like interaction."""
    try:
        driver.get(LOGIN_URL)
        human_delay(5, 7)
        username_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        password_input = driver.find_element(By.NAME, "password")
        for char in email:
            username_input.send_keys(char)
            time.sleep(random.uniform(0.1, 0.3))
        for char in password:
            password_input.send_keys(char)
            time.sleep(random.uniform(0.1, 0.3))
        password_input.send_keys(Keys.RETURN)
        human_delay(7, 12)
        print_log("Logged in successfully!")
    except Exception as e:
        print_log("Error logging in:", e)

def navigate_to_search_icon():
    """Clicks the search icon using its SVG element."""
    try:
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//*[name()='svg' and @aria-label='Search']"))
        ).click()
        print_log("Clicked on search icon successfully.")
    except Exception as e:
        print_log("Error clicking search icon:", e)

def search_user(search_words):
    chosen_word = choose_words(search_words)
    print_log(f"chosen word: {chosen_word}")
    result = False
    try:
        navigate_to_search_icon()
        search_box = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search']"))
        )
        search_box.clear()
        time.sleep(1)
        for char in chosen_word:
            search_box.send_keys(char)
            time.sleep(0.2)
        time.sleep(3)  # Wait for results to appear
        results_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@placeholder='Search']/ancestor::div[3]/following-sibling::div")
            )
        )
        profile_links = results_container.find_elements(By.XPATH, ".//a")
        valid_profiles = [a for a in profile_links if 
                          "explore/tags" not in a.get_attribute("href") and 
                          "about.meta" not in a.get_attribute("href")]
        
        # Loop through each link and click on it
        for chosen_profile in valid_profiles:
            profile_href = chosen_profile.get_attribute("href")
            if add_path_to_csv(FILE_PATH, profile_href) == False: continue
            result = True
            driver.execute_script("arguments[0].click();", chosen_profile)
            print_log("Found valid profile:", profile_href)
            human_delay(5, 8)
            break
        
        if result == False: print_log("No valid profile found for search term:", chosen_word)
        return result
    except Exception as e:
        print_log("Error in search_user:", e)
        return result

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def capture_profile_data():
    """
    Extracts profile data from the profile page.
    Captures the profile URL, display name, bio, and external link if available.
    Returns profile_url, display_name, bio_text, external_link, and a list of keywords.
    """
    try:
        profile_url = driver.current_url
        
        # Extract display name (h1 first, fallback to h2)
        try:
            display_name = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//header//section//h1"))
            ).text.strip()
            if not display_name:
                raise Exception("Empty h1")
        except Exception:
            try:
                display_name = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//header//h2"))
                ).text.strip()
            except Exception:
                display_name = "No display name found"

        # Extract bio text
        try:
            bio_text = driver.find_element(By.XPATH, "//header//section//div/span").text.strip()
            if not bio_text:
                raise Exception("Empty bio")
        except Exception:
            try:
                bio_text = driver.find_element(By.XPATH, "//div[contains(@class, '_aa_c')]//span").text.strip()
            except Exception:
                bio_text = "No bio found"

        # Extract external profile link (if available)
        try:
            external_link_element = driver.find_element(By.XPATH, "//a[contains(@href, 'http')]")
            external_link = external_link_element.get_attribute("href")
        except Exception:
            external_link = "No external link found"

        # Generate keywords from extracted text
        combined_text = f"{display_name} {bio_text}"
        keywords = combined_text.split()

        print_log(f"Profile URL: {profile_url}")
        print_log(f"Display Name: {display_name}")
        print_log(f"Bio: {bio_text}")
        print_log(f"External Link: {external_link}")
        print_log("Extracted Keywords:", keywords)

        return profile_url, display_name, bio_text, external_link, keywords
    
    except Exception as e:
        print_log("❌ Error capturing profile data:", e)
        return None, None, None, None, None

def send_dm_from_profile(profile_url, message):
    """
    Navigates to the given profile URL (if not already loaded), clicks the Message button,
    dismisses any overlays (including Turn on Notifications), and sends the message.
    """
    try:
        if driver.current_url != profile_url:
            driver.get(profile_url)
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//header"))
            )
            human_delay(3, 5)
        else:
            print_log("✅ Profile already loaded.")
    except Exception as e:
        print_log("❌ Error loading profile header:", e)
        return

    # Dismiss popups like "Not Now" or "Turn on Notifications"
    popup_xpaths = [
        "//button[normalize-space()='Not Now']",
        "//button[contains(text(),'Not Now')]",
        "//div[contains(@class, '_a9-z')]//button[normalize-space()='Not Now']"
    ]
    for xpath in popup_xpaths:
        try:
            popup_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            driver.execute_script("arguments[0].click();", popup_button)
            human_delay(1, 2)
            print_log(f"✅ Dismissed popup using: {xpath}")
        except Exception:
            continue

    # Locate and click the DM button
    dm_button = None
    dm_locators = [
        (By.XPATH, "//div[@role='button' and contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'message')]"),
        (By.XPATH, "//button[normalize-space()='Message']"),
        (By.XPATH, "//div[contains(.,'Message') and @role='button']")
    ]
    for locator in dm_locators:
        try:
            dm_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(locator))
            if dm_button:
                print_log("✅ Found DM button using locator:", locator)
                break
        except Exception:
            continue

    if not dm_button:
        print_log("❌ DM button not found.")
        return

    try:
        driver.execute_script("arguments[0].scrollIntoView(true);", dm_button)
        human_delay(1, 2)
        driver.execute_script("arguments[0].click();", dm_button)
        print_log("✅ Clicked DM button.")
    except Exception as e:
        print_log("❌ Error clicking DM button:", e)
        return

    human_delay(3, 5)

    # After clicking DM button, check for any notification popup again
    try:
        notif_popup = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, '_a9-z')]"))
        )
        not_now_notif = notif_popup.find_element(By.XPATH, ".//button[normalize-space()='Not Now']")
        driver.execute_script("arguments[0].click();", not_now_notif)
        human_delay(1, 2)
        print_log("✅ Dismissed 'Turn on Notifications' popup.")
    except Exception:
        print_log("⚠️ No 'Turn on Notifications' popup found.")

    # Locate the DM textarea using multiple fallback locators
    text_area = None
    dm_textarea_locators = [
        "/html/body/div[1]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/section/main/section/div/div/div/div[1]/div/div[2]/div/div/div[1]/div/div[2]/div[2]/div/div/div[2]/div/div[1]",  # New XPath
        "//div[@role='dialog']//textarea",  # Default textarea
        "//div[@role='dialog']//div[contains(@class, 'x1i10hfl')]//p",  # Alternative locator
        "//textarea"  # Generic fallback
    ]
    for locator in dm_textarea_locators:
        try:
            text_area = WebDriverWait(driver, 15).until(
                EC.visibility_of_element_located((By.XPATH, locator))
            )
            if text_area:
                print_log(f"✅ Found DM textarea using: {locator}")
                break
        except Exception:
            continue

    if not text_area:
        print_log("❌ DM textarea not found.")
        return

    # Click the text area to activate it
    try:
        text_area.click()
        human_delay(1, 2)
    except Exception as e:
        print_log("❌ Error clicking DM textarea:", e)
        return

    # Use clipboard paste to handle emojis
    try:
        pyperclip.copy(message)
        text_area.send_keys(Keys.CONTROL, "v")  # For Windows
        # text_area.send_keys(Keys.COMMAND, "v")  # For Mac
        print_log("✅ Pasted message using clipboard.")
    except Exception as e:
        print_log("❌ Error pasting message:", e)
        return

    human_delay(2, 3)

    # Attempt to click the Send button; if not found, use RETURN as fallback
    try:
        send_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[@role='dialog']//div[@role='button' and contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'send')]")
            )
        )
        # driver.execute_script("arguments[0].click();", send_button)
        print_log("✅ Clicked Send button.")
    except Exception as e:
        print_log("⚠️ Send button not clickable, sending RETURN instead:", e)
        text_area.send_keys(Keys.RETURN)
    
    print_log("✅ Message sent!")

def perform_automation_DM(email, password, links, keywords, message, search_words, dms_hours):
    try:
        login_instagram(email, password)
        while 1:
            result = search_user(search_words)
            if result == False: continue
            human_delay(10, 20)
            profile_url, display_name, bio_text, external_link, combine_text = capture_profile_data()

            if profile_url:
                # Fixing the condition
                check_link = any(word in external_link for word in REJECT_URL)
                check_keyword = any(word.lower() in keywords for word in INJECT_KEYWORD)
                link_match = any(word in external_link for word in links.split(","))
                keyword_match = any(target.lower() in combine_text for target in keywords.split(","))

                if links == '': link_match = True
                if keywords == '': keyword_match = True

                if check_link == True: continue
                if check_keyword == True or link_match and keyword_match:
                    send_dm_from_profile(profile_url, message)
                    human_delay(10, 20)
    finally:
        driver.quit()
        print_log("✅ Program execution complete. Exiting...")
        sys.exit()  # Ensures the program quits after execution