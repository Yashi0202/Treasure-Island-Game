import tkinter as tk
from tkinter import messagebox, ttk
from functools import partial
import random

class TreasureIslandForKids:
    def __init__(self, root):
        self.root = root
        self.root.title("🏝️ Treasure Hunt Adventure for Kids")
        self.root.geometry("700x550")
        self.root.configure(bg="#FFF9E3")
        self.stage = "start"
        self.score = 0

        # Style setup
        self.style = ttk.Style()
        self.style.configure("TButton",
                             font=("Comic Sans MS", 14),
                             padding=10,
                             background="#FDD835",
                             foreground="#000")
        self.style.map("TButton",
                       foreground=[('active', '#ffffff')],
                       background=[('active', '#FFA000')])

        # Title and score labels
        self.title_label = tk.Label(root,
                                    text="🏝️ Welcome to Treasure Island!",
                                    font=("Comic Sans MS", 24, "bold"),
                                    bg="#FFF9E3",
                                    fg="#3E2723")
        self.title_label.pack(pady=(20, 10))

        self.score_label = tk.Label(root,
                                    text=f"Score: {self.score}",
                                    font=("Comic Sans MS", 18, "bold"),
                                    bg="#FFF9E3",
                                    fg="#4E342E")
        self.score_label.pack(pady=(0, 20))

        self.text = tk.Label(root,
                             text="Let's go on a fun treasure hunt adventure! 🪙",
                             font=("Comic Sans MS", 16),
                             wraplength=600,
                             justify="center",
                             bg="#FFF9E3",
                             fg="#4E342E")
        self.text.pack(pady=(10, 30))

        self.button_frame = tk.Frame(root, bg="#FFF9E3")
        self.button_frame.pack()

        self.buttons = []

        # Riddles as dicts with question, options list, and correct index
        self.riddles = [
            {
                "question": "What has keys but can't open locks?",
                "options": ["Piano", "Map", "Clock"],
                "answer_index": 0
            },
            {
                "question": "What has hands but can't clap?",
                "options": ["Clock", "Robot", "Chair"],
                "answer_index": 0
            },
            {
                "question": "What runs but never walks?",
                "options": ["Water", "Dog", "Car"],
                "answer_index": 0
            },
            {
                "question": "What has to be broken before you can use it?",
                "options": ["Egg", "Glass", "Window"],
                "answer_index": 0
            },
            {
                "question": "What has a face and two hands but no arms or legs?",
                "options": ["Clock", "Human", "Statue"],
                "answer_index": 0
            },
        ]
        self.current_riddle = None

        self.stages = {
            "start": ("Let's go on a fun treasure hunt adventure! 🪙", ["Let's Start!"]),
            "choose_path": ("You're at a forest path. Which way should we go? 🌲", ["Left", "Right"]),
            "lake_scene": ("You see a big shiny lake. What should we do? 🐸", ["Wait for a boat", "Swim across"]),
            "door_scene": ("Yay! You reached a magical house with 3 colorful doors! 🚪", ["Red", "Yellow", "Blue"]),
            "vault_scene": ("🎉 Wow! You found the treasure! Should we open the super secret vault?", ["Yes", "No"]),
        }

        self.create_buttons(self.stages["start"][1])

    def create_buttons(self, choices):
        # Clear existing buttons
        for btn in self.buttons:
            btn.destroy()
        self.buttons.clear()

        for choice in choices:
            btn = ttk.Button(self.button_frame, text=choice,
                             command=partial(self.handle_choice, choice.lower()))
            btn.pack(pady=10, ipadx=10, ipady=5, fill='x', expand=True)
            self.buttons.append(btn)

    def handle_choice(self, choice):
        if self.stage == "start":
            self.update_stage("choose_path")

        elif self.stage == "choose_path":
            if "left" in choice:
                self.update_stage("lake_scene")
            else:
                self.game_over("Oh no! You fell into a big muddy hole! 💀")

        elif self.stage == "lake_scene":
            if "wait" in choice:
                self.pick_riddle()
                self.update_stage("riddle_scene")
            else:
                self.game_over("Oops! An alligator scared you away! 🐊")

        elif self.stage == "door_scene":
            if "yellow" in choice:
                self.update_stage("vault_scene")
            elif "red" in choice:
                self.game_over("Yikes! That room was full of fire! 🔥")
            elif "blue" in choice:
                self.game_over("Oh no! Some silly monsters were hiding there! 👹")
            else:
                self.game_over("Hmm... That door didn’t exist! 🚪")

        elif self.stage == "vault_scene":
            if "yes" in choice:
                self.game_win("🎉 Hooray! You found even more treasure! You're super RICH!! 💰")
            else:
                self.game_win("😊 Good thinking! You walk away happy with your treasure! 🎒")

        elif self.stage == "riddle_scene":
            # In riddle stage, choice will be option text clicked
            self.check_riddle_answer(choice)

    def update_stage(self, stage):
        self.stage = stage

        # Update score label anytime
        self.score_label.config(text=f"Score: {self.score}")

        if stage != "riddle_scene":
            text, buttons = self.stages.get(stage, ("", []))
            self.text.config(text=text)
            self.create_buttons(buttons)

    def pick_riddle(self):
        self.button_frame.pack()  # ensure button frame visible
        # Clear old buttons
        for btn in self.buttons:
            btn.destroy()
        self.buttons.clear()

        self.current_riddle = random.choice(self.riddles)
        question = self.current_riddle["question"]
        options = self.current_riddle["options"]

        self.text.config(text=f"Solve this riddle to cross!\n\n🧩 {question}")

        # Create buttons for MCQ options
        for idx, option in enumerate(options):
            btn = ttk.Button(self.button_frame, text=option,
                             command=partial(self.handle_choice, option.lower()))
            btn.pack(pady=10, ipadx=10, ipady=5, fill='x', expand=True)
            self.buttons.append(btn)

    def check_riddle_answer(self, selected_option):
        correct_option = self.current_riddle["options"][self.current_riddle["answer_index"]].lower()

        if selected_option == correct_option:
            self.score += 10
            messagebox.showinfo("Correct! 🎉", "Great job! You solved the riddle!")
            self.update_stage("door_scene")
        else:
            self.score -= 5
            messagebox.showerror("Oops! ❌", "That's not correct. Try again or choose another path!")
            # Allow retry by re-showing riddle
            self.pick_riddle()

        self.score_label.config(text=f"Score: {self.score}")

    def game_over(self, message):
        messagebox.showinfo("Game Over 😢", message)
        self.reset_game()

    def game_win(self, message):
        messagebox.showinfo("You Win! 🥳", message)
        self.reset_game()

    def reset_game(self):
        self.score = 0
        self.score_label.config(text=f"Score: {self.score}")
        self.stage = "start"
        self.text.config(text="Wanna play again?")
        self.create_buttons(["Let's Start!"])

if __name__ == "__main__":
    root = tk.Tk()
    game = TreasureIslandForKids(root)
    root.mainloop()

