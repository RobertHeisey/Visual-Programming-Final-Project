#knockout_rps_view.py
# 4/22/25
# Robert Heisey
# View file for knockout RPS mode GUI

import tkinter as tk
from functools import partial
from model import GameModel

class KnockoutRPSGUI:
    def __init__(self, root, model: GameModel):
        self.root = root
        self.model = model
        self.root.title("Knockout Rock Paper Scissors")

        # ---- Session Variables ----
        self.session_points = 0
        self.streak = 0

        # ---- Top Bar ----
        self.points_label = tk.Label(root, text=f"Points: {self.model.points}  |  Session: {self.session_points}", font=("Arial", 14))
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

        self.player_label = tk.Label(self.display_frame, text=f"{self.model.username}'s Choice:", font=("Arial", 16))
        self.player_label.grid(row=0, column=0, padx=40)

        self.computer_label = tk.Label(self.display_frame, text="Computer's Choice:", font=("Arial", 16))
        self.computer_label.grid(row=0, column=1, padx=40)

        self.player_choice_label = tk.Label(self.display_frame, text="", font=("Arial", 24))
        self.player_choice_label.grid(row=1, column=0)

        self.computer_choice_label = tk.Label(self.display_frame, text="", font=("Arial", 24))
        self.computer_choice_label.grid(row=1, column=1)

        # ---- Choice Buttons ----
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=10)

        for choice in ["Rock", "Paper", "Scissors"]:
            btn = tk.Button(self.button_frame, text=choice, width=10, font=("Arial", 14),
                            command=partial(self.play_round, choice))
            btn.pack(side="left", padx=10)

    def play_round(self, player_choice):
        comp_choice, result = self.model.play_rps(player_choice)
        self.player_choice_label.config(text=player_choice)
        self.computer_choice_label.config(text=comp_choice)

        if result == "win":
            points_earned = 200 * (2 ** self.streak)
            self.session_points += points_earned
            self.streak += 1
            self.result_label.config(
                text=f"{self.model.username} Wins! Streak: {self.streak} (+{points_earned} points)", fg="green"
            )
        elif result == "lose":
            self.session_points = 0
            self.streak = 0
            self.result_label.config(
                text="Computer Wins! You lost all session points.", fg="red"
            )
        else:
            self.result_label.config(text="It's a Draw!", fg="gray")

        self.update_points_label()
    
    def save_points(self):
        if self.model.username:
            self.model.points += self.session_points
            self.model.save_points()
            print(f"Saved {self.session_points} points for {self.model.username}")
            self.result_label.config(text=f"Saved {self.session_points} points!", fg="blue")
            self.session_points = 0
            self.streak = 0
            self.update_points_label()
        else:
            print("No username set. Cannot save.")

    def back_to_menu(self):
        # Do NOT add session points — player forfeits them by exiting without saving
        from menu_view import MenuGUI
        self.root.destroy()
        new_root = tk.Tk()
        MenuGUI(new_root, model=self.model)

    def update_points_label(self):
        self.points_label.config(
            text=f"Points: {self.model.points}  |  Session: {self.session_points}"
        )

# External launch function
def launch_game(model):
    root = tk.Tk()
    KnockoutRPSGUI(root, model)
    root.mainloop()