# triple_rps_view.py
# 4/22/25
# Robert Heisey
# View file for triple RPS mode GUI

import tkinter as tk
from functools import partial
from model import GameModel
import random

class TripleRPSGUI:
    def __init__(self, root, model: GameModel):
        self.root = root
        self.model = model
        self.root.title("Triple Rock Paper Scissors")

        # ---- Top Bar ----
        self.points_label = tk.Label(root, text=f"Points: {self.model.points}", font=("Arial", 14))
        self.points_label.pack(pady=5, anchor="nw")

        self.menu_button = tk.Button(root, text="Menu", command=self.back_to_menu)
        self.menu_button.pack(pady=5, anchor="ne")
        
        self.save_button = tk.Button(root, text="Save Points", command=self.save_points)
        self.save_button.pack(pady=0, anchor="ne")

        # ---- Result Display ----
        self.result_label = tk.Label(root, text="", font=("Arial", 16))
        self.result_label.pack(pady=10)

        # ---- Choices Display ----
        self.display_frame = tk.Frame(root)
        self.display_frame.pack(pady=20)

        self.cpu1_label = tk.Label(self.display_frame, text="CPU 1 Choice:", font=("Arial", 16))
        self.cpu1_label.grid(row=0, column=0, padx=30)

        self.player_label = tk.Label(self.display_frame, text=f"{self.model.username}'s Choice:", font=("Arial", 16))
        self.player_label.grid(row=0, column=1, padx=30)

        self.cpu2_label = tk.Label(self.display_frame, text="CPU 2 Choice:", font=("Arial", 16))
        self.cpu2_label.grid(row=0, column=2, padx=30)

        self.cpu1_choice_label = tk.Label(self.display_frame, text="", font=("Arial", 24))
        self.cpu1_choice_label.grid(row=1, column=0)

        self.player_choice_label = tk.Label(self.display_frame, text="", font=("Arial", 24))
        self.player_choice_label.grid(row=1, column=1)

        self.cpu2_choice_label = tk.Label(self.display_frame, text="", font=("Arial", 24))
        self.cpu2_choice_label.grid(row=1, column=2)

        # ---- Choice Buttons ----
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=10)

        for choice in ["Rock", "Paper", "Scissors"]:
            btn = tk.Button(self.button_frame, text=choice, width=10, font=("Arial", 14),
                            command=partial(self.play_round, choice))
            btn.pack(side="left", padx=10)

    def play_round(self, player_choice):
        cpu1 = random.choice(["Rock", "Paper", "Scissors"])
        cpu2 = random.choice(["Rock", "Paper", "Scissors"])

        self.player_choice_label.config(text=player_choice)
        self.cpu1_choice_label.config(text=cpu1)
        self.cpu2_choice_label.config(text=cpu2)

        result = self.determine_result(player_choice, cpu1, cpu2)

        if result == "win":
            self.model.points += 300
            self.result_label.config(text=f"{self.model.username} Wins!", fg="green")
        elif result == "half":
            self.model.points += 150
            self.result_label.config(text=f"{self.model.username} Partial Win!", fg="goldenrod")
        elif result == "draw":
            self.result_label.config(text="It's a Draw!", fg="gray")
        else:
            self.result_label.config(text="Computers Win!", fg="red")

        self.points_label.config(text=f"Points: {self.model.points}")

    def determine_result(self, player, c1, c2):
        def beats(a, b):
            return (a == "Rock" and b == "Scissors") or \
                   (a == "Paper" and b == "Rock") or \
                   (a == "Scissors" and b == "Paper")

        if player == c1 == c2:
            return "draw"

        wins = 0
        ties = 0

        for comp in [c1, c2]:
            if player == comp:
                ties += 1
            elif beats(player, comp):
                wins += 1

        if wins == 2:
            return "win"
        elif wins == 1 and ties == 1:
            return "half"
        else:
            return "lose"

    def save_points(self):
        if self.model.username:
            self.model.save_points()
            print(f"Points saved for {self.model.username}")
        else:
            print("No username set. Cannot save.")

    def back_to_menu(self):
        from menu_view import MenuGUI
        self.root.destroy()
        new_root = tk.Tk()
        MenuGUI(new_root, model=self.model)

# External launch function
def launch_game(model):
    root = tk.Tk()
    TripleRPSGUI(root, model)
    root.mainloop()