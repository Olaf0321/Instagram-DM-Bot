import os

def take_screenshot(page, step):
    screenshot_path = f"screenshots/{step}.png"
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")
    page.screenshot(path=screenshot_path)
    print(f"Screenshot saved: {screenshot_path}")