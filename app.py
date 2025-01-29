import tkinter as tk
from tkinter import ttk, messagebox
import random
from PIL import Image, ImageTk

# ========== SETUP ==========

# Replace with your data set
words = {
    "Strasse": "die",
    "Post": "die",
    "Blumenladen": "der",
    "Platz": "der",
    "Hotel": "das",
    "Kaufhaus": "das",
    "Kino": "das",
    "Bahnhof": "der",
    "Info-Buro": "das",
    "Spielothek": "die",
    "Apotheke": "die",
    "Park": "der",
    "Restaurant": "das",
    "Cafe": "das",
    "Schule": "die",
    "Theather": "das",
    "Zentrum": "das",
    "Parkhaus": "das",
    "Backerei": "die",
    "Schiff": "das",
    "Zug": "der",
    "Flugzeug": "das",
    "Bus": "der",
    "Strassebahn": "die",
    "Taxi": "das",
    "Mofa": "das",
    "U-Bahn": "die",
    "Fahrrad": "das",
    "Motorrad": "das",
    "Fahre": "die",
    "S-Bahn": "die",
    "Supermarkt": "der",
    "Stadion": "das",
    "Eisdiele": "die",
    "Shop": "der",
    "Shaft": "der",
    "Buchhandlung":"die",
    "Laden": "der",
    "Arbeit": "die",
    "Universitat": "die",
}

word_list = list(words.items())
random.shuffle(word_list)

current_index = 0
score = 0
correct = 0
wrong = 0

# ========== STYLING ==========
BG_COLOR = "#2E3440"          # Dark background
BUTTON_COLOR = "#434C5E"      # Button base color
TEXT_COLOR = "#ECEFF4"        # White text (MUST be defined!)
ACCENT_COLOR = "#88C0D0"      # Interactive elements
FONT_NAME = "Arial"           # System font

# ========== ROOT WINDOW ==========
root = tk.Tk()
root.title("German Articles Quiz")
root.attributes('-fullscreen', True)
root.configure(bg=BG_COLOR)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

try:
    bg_image = Image.open("background_german.jpg") # Change with your own image path
    bg_image = bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    background_label = tk.Label(root, image=bg_photo)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
except Exception as e:
    print(f"Background image error: {e}")
    background_label = tk.Label(root, bg=BG_COLOR)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

# ========== CUSTOM STYLES ==========
style = ttk.Style()
style.theme_create("Nord", parent="alt", settings={
    "TButton": {
        "configure": {
            "font": (FONT_NAME, 18, "bold"),
            "borderwidth": 0,
            "relief": "flat",
            "padding": 20,
            "background": BUTTON_COLOR,
            "foreground": TEXT_COLOR,
            "borderradius": 15 
        },
        "map": {
            "background": [("active", ACCENT_COLOR), ("disabled", BG_COLOR)],
            "foreground": [("active", TEXT_COLOR)]
        }
    }
})
style.theme_use("Nord")

# ========== WIDGETS ==========
main_frame = tk.Frame(root, bg=BG_COLOR)
main_frame.place(relx=0.5, rely=0.5, anchor="center")

question_label = tk.Label(
    main_frame,
    text=f"What is the article for '{word_list[current_index][0]}'?",
    font=(FONT_NAME, 28, "bold"),
    bg=BG_COLOR,
    fg=TEXT_COLOR
)
question_label.pack(pady=40)

button_frame = tk.Frame(main_frame, bg=BG_COLOR)
button_frame.pack(pady=20)

button_style = {
    "style": "TButton",
    "width": 8
}

der_button = ttk.Button(
    button_frame,
    text="der",
    command=lambda: check_answer("der"),
    **button_style
)
die_button = ttk.Button(
    button_frame,
    text="die",
    command=lambda: check_answer("die"),
    **button_style
)
das_button = ttk.Button(
    button_frame,
    text="das",
    command=lambda: check_answer("das"),
    **button_style
)

der_button.pack(side="left", padx=15, pady=10)
die_button.pack(side="left", padx=15, pady=10)
das_button.pack(side="left", padx=15, pady=10)

progress_frame = tk.Frame(root, bg=BG_COLOR)
progress_frame.place(x=20, y=20)

progress_labels = {
    "correct": tk.Label(progress_frame, text="Correct: 0", font=(FONT_NAME, 14), bg=BG_COLOR, fg="#A3BE8C"),
    "wrong": tk.Label(progress_frame, text="Wrong: 0", font=(FONT_NAME, 14), bg=BG_COLOR, fg="#BF616A"),
    "remaining": tk.Label(progress_frame, text=f"Remaining: {len(word_list)}", font=(FONT_NAME, 14), bg=BG_COLOR, fg=TEXT_COLOR)
}

for label in progress_labels.values():
    label.pack(anchor="w", pady=5)

close_btn = ttk.Button(
    root,
    text="X",
    command=root.destroy,
    style="TButton",
    width=3
)
close_btn.place(relx=0.98, rely=0.02, anchor="ne")

# ========== GAME LOGIC ==========
def check_answer(article):
    global current_index, score, correct, wrong
    
    correct_article = word_list[current_index][1]
    buttons = {"der": der_button, "die": die_button, "das": das_button}

    for btn in buttons.values():
        btn.config(style="TButton")

    if article == correct_article:
        buttons[article].config(style="Success.TButton")
        score += 1
        correct += 1
    else:
        buttons[article].config(style="Error.TButton")
        buttons[correct_article].config(style="Success.TButton")
        wrong += 1

    update_progress()
    root.after(1000, next_question)

def next_question():
    global current_index
    current_index += 1
    
    if current_index < len(word_list):
        der_button.config(style="TButton")
        die_button.config(style="TButton")
        das_button.config(style="TButton")
        
        question_label.config(text=f"What is the definite article for '{word_list[current_index][0]}'?")
        update_progress()
    else:
        messagebox.showinfo("Finished!", f"Final Score: {score}/{len(word_list)}\nCorrect: {correct}\nWrong: {wrong}")
        root.destroy()

def update_progress():
    progress_labels["correct"].config(text=f"Correct: {correct}")
    progress_labels["wrong"].config(text=f"Wrong: {wrong}")
    progress_labels["remaining"].config(text=f"Remaining: {len(word_list) - current_index - 1}")

# ========== CUSTOM BUTTON STATES ==========
style.configure("Success.TButton", 
               background="#A3BE8C",
               foreground=TEXT_COLOR,
               activebackground="#A3BE8C",
               activeforeground=TEXT_COLOR)
style.map("Success.TButton",
         background=[('active', '#A3BE8C'), ('disabled', '#A3BE8C')],
         foreground=[('active', TEXT_COLOR)])

style.configure("Error.TButton", 
               background="#BF616A",
               foreground=TEXT_COLOR,
               activebackground="#BF616A",
               activeforeground=TEXT_COLOR)
style.map("Error.TButton",
         background=[('active', '#BF616A'), ('disabled', '#BF616A')],
         foreground=[('active', TEXT_COLOR)]) 

# ========== START ==========
root.mainloop()
