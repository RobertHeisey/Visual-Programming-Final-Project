# basic_rps_view.py
# 4/22/25
# Robert Heisey
# View file for basic RPS mode GUI

import tkinter as tk
from functools import partial
from model import GameModel

class BasicRPSGUI:
    def __init__(self, root, model: GameModel):
        self.root = root
        self.model = model
        self.root.title("Basic Rock Paper Scissors")

        # ---- Top Bar ----
        self.points_label = tk.Label(root, text=f"Points: {self.model.points}", font=("Arial", 14))
        self.points_label.pack(pady=5, anchor="nw")

        self.menu_button = tk.Button(root, text="Menu", command=self.back_to_menu)
        self.menu_button.pack(pady=5, anchor="ne")
        
        self.save_button = tk.Button(root, text="Save Points", command=self.save_points)
        self.save_button.pack(pady=0, anchor="ne")

        # ---- Winner Display ----
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
            self.result_label.config(text=f"{self.model.username} Wins!", fg="green")
        elif result == "lose":
            self.result_label.config(text="Computer Wins!", fg="red")
        else:
            self.result_label.config(text="It's a Draw!", fg="gray")

        self.points_label.config(text=f"Points: {self.model.points}")

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

# External launch function used by menu_view.py
def launch_game(model):
    root = tk.Tk()
    BasicRPSGUI(root, model)
    root.mainloop()