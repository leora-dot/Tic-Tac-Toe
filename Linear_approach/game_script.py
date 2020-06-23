import random
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# TO DO LIST:
    #can you define the list of empty points with a list comprehension?

#Classes

class Board:

    def __init__(self):
        self.x_points = []
        self.o_points = []
        self.x_turn_counter = 0
        self.o_turn_counter = 0
        self.empty_points = [(0,0), (1,0), (2,0), (0,1), (1,1), (2,1), (0,2), (1,2), (2,2)]
        self.is_game_won = False
        self.is_game_over = False
        self.winner = None

    def is_valid_move(self, requested_point):
        return requested_point in self.empty_points

    def update_board(self, player, requested_point):
        self.empty_points.remove(requested_point)
        if player == "x":
            self.x_points.append(requested_point)
            self.x_turn_counter += 1
        if player == "o":
            self.o_points.append(requested_point)
            self.o_turn_counter += 1

    def show_board(self):
        pass

#Functions

def position_to_point(position):
    pass

#Game
