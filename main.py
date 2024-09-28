from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
window = Tk()
current_card = {}
to_learn = {}
try:
    data = pandas.read_csv("word_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(word, text=current_card["French"], fill="black")
    canvas.itemconfig(title, text="French", fill="black")
    canvas.itemconfig(front_card_background, image=card_front_photo)
    flip_timer = window.after(4000, show_english_word)

 
def is_known():
    to_learn.remove(current_card)
    data_file = pandas.DataFrame(to_learn)
    data_file.to_csv("word_to_learn.csv", index=False)
    next_card()


def show_english_word():
    canvas.itemconfig(word, text=current_card["English"], fill="white")
    canvas.itemconfig(title, text="English", fill="white")
    canvas.itemconfig(front_card_background, image=card_back_photo)


window.title("Flashy")
window.config(background=BACKGROUND_COLOR, padx=50, pady=50)
canvas = Canvas(width=800, height=526)
canvas.config(background=BACKGROUND_COLOR, highlightthickness=0)

flip_timer = window.after(4000, show_english_word)

card_front_photo = PhotoImage(file="./images/card_front.png")
card_back_photo = PhotoImage(file="./images/card_back.png")
front_card_background = canvas.create_image(400, 263, image=card_front_photo)
canvas.grid(row=0, column=0, columnspan=2)

title = canvas.create_text(400, 150, text="title", font=("Courier", 30, "bold"))
word = canvas.create_text(400, 250, text="word", font=("Courier", 30, "bold"))

right_photo = PhotoImage(file="./images/right.png")
known_button = Button(image=right_photo, highlightthickness=0, command=is_known)
known_button.grid(row=1, column=1)

wrong_photo = PhotoImage(file="./images/wrong.png")
unknown_button = Button(image=wrong_photo, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)

next_card()

window.mainloop()
