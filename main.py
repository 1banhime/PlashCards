import tkinter as tk
from tkinter import messagebox
import random
from dictionary import *
import pickle

def save():
    with open("kanji_data.pickle", "wb") as file:
        pickle.dump((mastery_level, seen_words), file)

def load():
    global mastery_level, seen_words
    try:
        with open("kanji_data.pickle", "rb") as file:
            mastery_level, seen_words = pickle.load(file)
    except FileNotFoundError: 
        mastery_level = 0
        seen_words = [random.choice(list(kanji_data.keys()))]

load()


def mastery(exp=0):
    global mastery_level  
    mastery_level += exp
    return mastery_level

def card_pick():
        if len(seen_words) > mastery():
            return random.choice(seen_words)
        else:
            return random.choice(list(kanji_data.keys()))

def display_card():
    global current_kanji
    current_kanji = card_pick()
    if current_kanji not in seen_words:
        seen_words.append(current_kanji) 
    kanji_label.config(text=current_kanji)

def check_answer(event = None):
    global mastery_level
    user_answer = answer_entry.get().strip().lower()
    correct_answer = kanji_data[current_kanji]["Meaning"].lower()

    if user_answer == correct_answer:
        messagebox.showinfo("Correct", f"The kun reading is: {kanji_data[current_kanji]['Kun Reading']} \n\n the on reading is: {kanji_data[current_kanji]['On Reading']}")
        mastery(random.randint(1,3))
    else:
        messagebox.showerror("Incorrect", f"Wrong answer! The correct answer is: {correct_answer}")
        mastery(random.randint(-3,0))
    
    answer_entry.delete(0, tk.END)
    display_card()



root = tk.Tk()
root.geometry("1280x800")
root.title("Kanji Flashcards")

current_kanji = card_pick()

kanji_label = tk.Label(root, font=("Helvetica", 48), text=current_kanji)
kanji_label.pack(pady=20)

answer_entry = tk.Entry(root, font=("Helvetica", 20))
answer_entry.pack(pady=10)

submit_button = tk.Button(root, text="Next", command=check_answer)
submit_button.pack(pady=10)

root.bind("<Return>", lambda event = None: check_answer(event))

display_card()

root.protocol("WM_DELETE_WINDOW", save())

root.mainloop()



# #HOW TO DO THE CHECK!!!!!
# # c = random.choice(list(kanji_data.keys())) 
# # l = kanji_data[c]

# # print(c)
# # print(l["Meaning"])
    
# print(kanji_data[card_pick()]["Meaning"])