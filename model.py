# model.py
# 4/22/25
# Robert Heisey
# Model file for RPS program

import csv
import random
import os

class GameModel:
    def __init__(self):
        self.username = ""
        self.points = 0
        self.streak = 0  # For Knockout RPS mode

    def set_username(self, username):
        self.username = username

    def load_points(self):
        filename = f"{self.username}.csv"
        if os.path.exists(filename):
            with open(filename, newline='') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    self.points = int(row[0])
        else:
            self.points = 0

    def save_points(self):
        filename = f"{self.username}.csv"
        with open(filename, mode='w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([self.points])

    def play_rps(self, player_choice):
        # Rock = 0, Paper = 1, Scissors = 2
        choices = ['Rock', 'Paper', 'Scissors']
        computer_choice = random.choice(choices)
        result = self._determine_winner(player_choice, computer_choice)
        if result == 'win':
            self.points += 200
        return computer_choice, result

    def play_triple_rps(self, player_choice):
        choices = ['Rock', 'Paper', 'Scissors']
        cpu1 = random.choice(choices)
        cpu2 = random.choice(choices)
        result = self._determine_triple_winner(player_choice, cpu1, cpu2)
        if result == 'win':
            self.points += 300
        return cpu1, cpu2, result

    def play_knockout_rps(self, player_choice):
        choices = ['Rock', 'Paper', 'Scissors']
        computer_choice = random.choice(choices)
        result = self._determine_winner(player_choice, computer_choice)
        if result == 'win':
            self.streak += 1
            self.points += 200 * (2 ** (self.streak - 1))
        elif result == 'lose':
            # Lose all Knockout points earned during this streak
            self.points -= sum(200 * (2 ** i) for i in range(self.streak))
            self.streak = 0
        return computer_choice, result

    def _determine_winner(self, player, computer):
        if player == computer:
            return "draw"
        elif (player == "Rock" and computer == "Scissors") or \
             (player == "Paper" and computer == "Rock") or \
             (player == "Scissors" and computer == "Paper"):
            return "win"
        else:
            return "lose"

    def _determine_triple_winner(self, player, cpu1, cpu2):
        choices = {player, cpu1, cpu2}
        if len(choices) == 3:
            return "draw"
        # Use majority win rules if two are the same and beat the third
        results = [self._determine_winner(player, cpu1),
                   self._determine_winner(player, cpu2)]
        if results.count('win') == 2:
            return "win"
        elif results.count('lose') == 2:
            return "lose"
        return "draw"