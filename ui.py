import tkinter as tk
import logging
from tkinter import Entry, Label, Button, Text, ttk
from config import LABEL_FONT, ENTRY_FONT, BTN_FONT, ENTRY_BG, ENTRY_FG, BTN_BG, BTN_FG, HOVER_BG, DMS_HOURS_OPTIONS, BTN_BG, BTN_FG, ORIGINAL_PASSWORD, EMAIL_OPTIONS
from main import perform_automation_DM

logging.basicConfig(
    filename="app.log",  # Log file name
    level=logging.INFO,  # Set logging level
    format="%(asctime)s - %(levelname)s - %(message)s"  # Log format
)


def print_log(context):
    logging.info(context)

def show_alert(value):
    # Create custom alert message in the center of the window
    alert_window = tk.Toplevel(root)
    alert_window.title("Alert")
    alert_window.configure(bg="#2C2F33")

    # Get the dimensions of the main window and the alert window
    window_width = 250
    window_height = 100
    screen_width = root.winfo_width()
    screen_height = root.winfo_height()

    # Calculate the position to center the alert window in the parent window
    position_top = int(screen_height / 2 - window_height / 2)
    position_left = int(screen_width / 2 - window_width / 2)

    # Set the size and position of the alert window
    alert_window.geometry(f'{window_width}x{window_height}+{root.winfo_x() + position_left}+{root.winfo_y() + position_top}')

    # Button to close the alert
    def close_alert():
        alert_window.destroy()
    # Label for the alert
    alert_label = Label(alert_window, text=value, font=("Arial", 10, "bold"), fg="white", bg="#2C2F33")
    alert_label.pack(pady=20)
    alert_btn = Button(alert_window, text="OK", font=("Arial", 10, "bold"), bg=BTN_BG, fg=BTN_FG, relief="flat", command=close_alert)
    alert_btn.pack(pady=5)

def initialize_automation_DM():
    print_log("init automate")
    # email = email_var.get()
    # password = password_entry.get()
    email = "eagle.free27@gmail.com"
    password = "clrhslrjwsoqjr"    
    link = link_entry.get()
    keyword = keyword_entry.get()
    message = message_text.get("1.0", "end-1c")  # Get text from Text widget
    search_words = search_entry.get()
    dms_hours = dms_hours_var.get()

    # Check if any of the fields are empty or non-valued
    if not password or not link or not keyword or not message or dms_hours == 'choose option' or email == 'choose email':
        text = "Please fill in all fields correctly!"
        show_alert(text)
    else:
        print_log("correctly initialized")
        perform_automation_DM(email, password, link, keyword, message, search_words, dms_hours)

# Create main window
root = tk.Tk()
root.title("DM Bot UI")
root.geometry("420x600")  # Adjusted height for the Submit button to fit
root.configure(bg="#2C2F33")  # Dark background color
root.resizable(False, False)  # Disable maximize button

# Title
Label(root, text="DM Bot (only an account)", font=("Arial", 14, "bold"), fg="white", bg="#2C2F33").pack(pady=5)

# Function to change button color on hover
def on_enter(e):
    submit_btn.config(bg=HOVER_BG)

def on_leave(e):
    submit_btn.config(bg=BTN_BG)

# Custom input field function (rounded effect)
def create_entry(parent, show=None):
    entry = Entry(parent, font=ENTRY_FONT, bg=ENTRY_BG, fg=ENTRY_FG, insertbackground="white", relief="flat", show=show)
    entry.pack(fill="x", padx=10, pady=3, ipady=5)
    entry.configure(highlightthickness=2, highlightbackground="#5B6EAE", highlightcolor="#5B6EAE")  # Rounded effect
    return entry

# Fields
# Add Email Dropdown
Label(root, text="Email:", font=LABEL_FONT, fg="white", bg="#2C2F33").pack(anchor="w", padx=10, pady=5)

# Create a list of email options (you can modify this list as needed)
email_options = EMAIL_OPTIONS # Replace with your actual email options
email_var = tk.StringVar()
email_dropdown = ttk.Combobox(root, textvariable=email_var, values=email_options, state="readonly", font=ENTRY_FONT)
email_dropdown.pack(fill="x", padx=10, pady=3, ipady=3)
email_dropdown.current(0)  # Default selection

# Adjust the rest of the layout and positioning as needed...

Label(root, text="Password:", font=LABEL_FONT, fg="white", bg="#2C2F33").pack(anchor="w", padx=10)
password_entry = create_entry(root, show="*")  # Password input type

Label(root, text="Link:", font=LABEL_FONT, fg="white", bg="#2C2F33").pack(anchor="w", padx=10)
link_entry = create_entry(root)

Label(root, text="Keyword:", font=LABEL_FONT, fg="white", bg="#2C2F33").pack(anchor="w", padx=10)
keyword_entry = create_entry(root)

Label(root, text="Recommand Search Words:", font=LABEL_FONT, fg="white", bg="#2C2F33").pack(anchor="w", padx=10)
search_entry = create_entry(root)

Label(root, text="Message:", font=LABEL_FONT, fg="white", bg="#2C2F33").pack(anchor="w", padx=10)
message_text = Text(root, font=ENTRY_FONT, bg=ENTRY_BG, fg=ENTRY_FG, height=4, wrap="word", relief="flat")
message_text.pack(fill="x", padx=10, pady=3)
message_text.configure(highlightthickness=2, highlightbackground="#5B6EAE", highlightcolor="#5B6EAE")  # Rounded effect

# DMs/Hours Dropdown
Label(root, text="DMs/Hours:", font=LABEL_FONT, fg="white", bg="#2C2F33").pack(anchor="w", padx=10)
dms_hours_var = tk.StringVar()
dms_hours_options = DMS_HOURS_OPTIONS
dms_hours_dropdown = ttk.Combobox(root, textvariable=dms_hours_var, values=dms_hours_options, state="readonly", font=ENTRY_FONT)
dms_hours_dropdown.pack(fill="x", padx=10, pady=3, ipady=3)
dms_hours_dropdown.current(0)

# Start Button (NOW VISIBLE)
submit_btn = Button(root, text="Start", font=BTN_FONT, bg=BTN_BG, fg=BTN_FG, relief="flat", command=initialize_automation_DM)
submit_btn.pack(pady=15, ipadx=10, ipady=5)  # Increased padding to ensure visibility

# Hover Effects
submit_btn.bind("<Enter>", on_enter)
submit_btn.bind("<Leave>", on_leave)

# Run application
root.mainloop()