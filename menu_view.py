# menu_view.py
# 4/22/25
# Robert Heisey
# View file for Menu GUI

import tkinter as tk
from tkinter import messagebox
from model import GameModel

class MenuGUI:
    def __init__(self, root, model=None):
        self.root = root
        self.model = model or GameModel()
        self.root.title("Rock Paper Scissors Menu")

        # ---- Title ----
        self.title_label = tk.Label(root, text="Rock! Paper! Scissors!", font=("Arial", 24))
        self.title_label.pack(pady=10)

        # ---- Username Input ----
        self.username_entry = tk.Entry(root, font=("Arial", 14))
        self.username_entry.pack(pady=5)
        
        # ---- Login and Save Buttons ----
        self.login_button = tk.Button(root, text="Login", command=self.login)
        self.login_button.pack(pady=2)
        
        self.save_button = tk.Button(root, text="Save Points", command=self.save_points)
        self.save_button.pack(pady=2)

        # ---- Points Display ----
        self.points_label = tk.Label(root, text="Points: 0", font=("Arial", 14))
        self.points_label.pack(pady=10, anchor="nw")

        # ---- Game Mode Buttons ----
        self.rps_button = tk.Button(root, text="RPS", width=20, command=self.launch_basic_rps)
        self.rps_button.pack(pady=4)

        self.triple_rps_button = tk.Button(root, text="Triple RPS", width=20, state="disabled", command=self.launch_triple_rps)
        self.triple_rps_button.pack(pady=4)

        self.knockout_rps_button = tk.Button(root, text="Knockout RPS", width=20, state="disabled", command=self.launch_knockout_rps)
        self.knockout_rps_button.pack(pady=4)

    def login(self):
        username = self.username_entry.get().strip()
        if not username:
            messagebox.showerror("Error", "Please enter a username.")
            return
        self.model.set_username(username)
        self.model.load_points()
        self.update_points_display()
        self.update_unlocks()

    def save_points(self):
        self.model.save_points()
        messagebox.showinfo("Saved", "Points saved successfully.")

    def update_points_display(self):
        self.points_label.config(text=f"Points: {self.model.points}")

    def update_unlocks(self):
        if self.model.points >= 1000:
            self.triple_rps_button.config(state="normal")
        if self.model.points >= 5000:
            self.knockout_rps_button.config(state="normal")

    def launch_basic_rps(self):
        import basic_rps_view
        self.root.destroy()
        basic_rps_view.launch_game(self.model)

    def launch_triple_rps(self):
        import triple_rps_view
        self.root.destroy()
        triple_rps_view.launch_game(self.model)

    def launch_knockout_rps(self):
        import knockout_rps_view
        self.root.destroy()
        knockout_rps_view.launch_game(self.model)

# Entry point
if __name__ == "__main__":
    root = tk.Tk()
    menu = MenuGUI(root)
    root.mainloop()