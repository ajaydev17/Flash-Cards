from tkinter import Tk, Canvas, PhotoImage, Button
import pandas
import random

# Constants

BACKGROUND_COLOR = "#B1DDC6"
TITLE_FONT = ("Arial", 40, "italic")
WORD_FONT = ("Arial", 60, "bold")
french_to_learn = {}
current_card = {}


# Read data from csv

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    french_to_learn = original_data.to_dict(orient="records")
else:
    french_to_learn = data.to_dict(orient="records")


# Generate random word

def generate_new_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(french_to_learn)
    
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card['French'], fill="black")
    canvas.itemconfig(card_background, image=card_front_image)

    flip_timer = window.after(3000, func=flip_card)
    

# Flip card

def flip_card():
    global current_card
    canvas.itemconfig(card_title, text="English", fill="white")

    try:
        canvas.itemconfig(card_word, text=current_card['English'], fill="white")
        canvas.itemconfig(card_background, image=card_back_image)
    except KeyError:
        generate_new_card()


# If known Card

def is_known():
    try:
        french_to_learn.remove(current_card)
        data_after_remove = pandas.DataFrame(french_to_learn)

        data_after_remove.to_csv("data/words_to_learn.csv", index=False)
        generate_new_card()
    except ValueError:
        generate_new_card()


# UI Components

window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

# Canvas

canvas = Canvas(width=800, height=526)
card_front_image = PhotoImage(file="images/card_front.png")
card_back_image = PhotoImage(file="images/card_back.png")

card_background = canvas.create_image(400, 263, image=card_front_image)
card_title = canvas.create_text(400, 150, text="", font=TITLE_FONT)

card_word = canvas.create_text(400, 263, text="Flash Cards", font=WORD_FONT)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

# Buttons

cross_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_image, highlightthickness=0, bd=0, command=generate_new_card)
unknown_button.grid(row=1, column=0)

check_image = PhotoImage(file="images/right.png")
known_button = Button(image=check_image, highlightthickness=0, bd=0, command=is_known)
known_button.grid(row=1, column=1)
window.mainloop()
