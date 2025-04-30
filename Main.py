# main.py
# 4/22/25
# Robert Heisey
# Main launcher for RPS program

import tkinter as tk
from model import GameModel
from menu_view import MenuGUI

def main():
    root = tk.Tk()
    model = GameModel()
    MenuGUI(root, model=model)
    root.mainloop()

if __name__ == "__main__":
    main()