import tkinter as tk
from tkinter import messagebox
import random
import json
import pickle

class KanjiApp(tk.Tk):
    '''super class that handles the tkinter GUI and configurations'''
    def __init__(self):
        #it init innit? it's the framework for the applications GUI layout
        super().__init__() 
        self.geometry("1280x800")
        self.title("Kanji Flashcards")
        
        self.load_data()
        
        self.kanji_label = tk.Label(self, font=("Helvetica", 48)) 
        self.kanji_label.pack(pady=20)
        
        self.answer_entry = tk.Entry(self, font=("Helvetica", 20))
        self.answer_entry.pack(pady=10)
        
        self.submit_button = tk.Button(self, text="Next", command=self.check_answer)
        self.submit_button.pack(pady=10)
        
        self.menubar = tk.Menu(self)
        self.menubar.add_command(label="Change card set", command=None)
        self.config(menu=self.menubar)
        
        self.bind("<Return>", self.check_answer)
        
        self.protocol("WM_DELETE_WINDOW", self.close)
        
        self.display_card()
        
    def load_data(self): 
        '''Loads the seen_words and mastery_level varaibles from the kanji_data.pickle file
        or creates the file if no file exists and sets mastery_level to 0 and seen words 
        as an empty list'''
        try:
            with open("kanji_data.pickle", "rb") as file:
                self.mastery_level, self.seen_words = pickle.load(file)
        except FileNotFoundError: 
            self.mastery_level = 0
            self.seen_words = []
        
        try:
            with open("dictionary.json", "r") as file:
                self.kanji_data = json.load(file)     
        except FileNotFoundError:
            quit()
            
    def save_data(self):
        '''Writes the mastery_level and seen_words variables to the kanji_data.pickle file'''
        with open("kanji_data.pickle", "wb") as file:
            pickle.dump((self.mastery_level, self.seen_words), file)
    
    def mastery(self, exp=0):
        '''Stores and modifies the mastery_level variable whenever an answer is given'''
        self.mastery_level += exp
        return self.mastery_level
    
    def pick_card(self):
        '''picks a "card" at random from the kanji_data dictionary or seen_words list 
        based on the current mastery level'''
        if len(self.seen_words) > self.mastery():
            return random.choice(self.seen_words)
        else:
            return random.choice(list(self.kanji_data.keys()))
        
    def display_card(self):
        '''displays the current_kanji as the kanji_label and adds the current_kanji to the
        seen_words list if it's the first time it is shown.'''
        self.current_kanji = self.pick_card()
        if self.current_kanji not in self.seen_words:
            self.seen_words.append(self.current_kanji) 
        self.kanji_label.config(text=self.current_kanji)
        
    def check_answer(self, coconut = None):
        '''checks if the answer_entry given by the user matches the current_kanji. calls the 
        mastery function to increase the mastery_level with a random postive or negative 
        integer depending on if the answer is correct.'''
        user_answer = self.answer_entry.get().strip().lower()
        correct_answer = self.kanji_data[self.current_kanji]["Meaning"].lower()

        if user_answer == correct_answer:
            messagebox.showinfo("Correct", f"The kun reading is: {self.kanji_data[self.current_kanji]['Kun Reading']} \n\n the on reading is: {self.kanji_data[self.current_kanji]['On Reading']}")
            self.mastery(random.randint(1,3)) #TODO: Test rand float 
        else:
            messagebox.showerror("Incorrect", f"Wrong answer! The correct answer is: {correct_answer}")
            self.mastery(random.randint(-3,0)) #TODO: Test rand float
        
        self.answer_entry.delete(0, tk.END)
        self.display_card()
        
    def close(self):
        '''calls the save_data function and closes the application'''
        print(self.seen_words, self.mastery_level)
        self.save_data()
        self.destroy() #I wish™
        
            
if __name__ == "__main__":
    #Program runtime... obviously
    app = KanjiApp()
    app.mainloop()
    
                

