import random
from functions.screenshot import take_screenshot

def human_pause(page):
    page.wait_for_timeout(random.randint(5000, 10000))

def validate_user_selection(page, link, keyword):
    take_screenshot(page, "After_select_user")
    # def check_user():
    #     words = keyword.split(',')
    #     flag = False
    #     for word in words:
    #         if word not in newtext: continue
    #         flag = True
    #         break
    #     if not flag and newlink == link:
    #         flag = True
    #     return flag
    
    # newtext = page.locator("")  # Adjust selector
    # newlink = page.locator("")  # Adjust selector

    # human_pause(page)

    # return check_user()
    return True