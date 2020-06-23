import random
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

import math
import itertools

# TO DO LIST:
    #can you define the list of empty points with a list comprehension?
    #get rid of the repetition in update_board_status

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

    def check_for_win(self, last_player):
        #Assigning variables
        if last_player == "x":
            previous_points = self.x_points[:-1]
            last_point = self.x_points[-1]
            turn_counter = self.x_turn_counter
        if last_player == "o":
            previous_points = self.o_points[:-1]
            last_point = self.o_points[-1]
            turn_counter = self.o_turn_counter
        #Was the game won in this move?
        if turn_counter < 3:
            return
        else:
            x_last = last_point[0]
            y_last = last_point[1]
            previous_points_combinations = previous_points_combination_generator(previous_points)
            for combination in previous_points_combinations:
                #assign variables
                point1 = combination[0]
                x1 = point1[0]
                y1 = point1[1]
                point2 = combination[1]
                x2 = point2[0]
                y2 = point2[1]
                #calculate line based on previous points
                #vertical line
                if x1 == x2:
                    #If last_point is on that line, game is won
                    if x_last == x1:
                        update_board_winner(winner)
                        return
                #horizontal or diagnal line:
                else:
                    m = (y2-y1)/(x2-x1)
                    b = y1 - m * x1
                    if y_last == m * x_last +b:
                        #If last_point is on that line, game is won
                        update_board_winner(winner)
                        return
            #If the game is not won, check for a tie
            self.is_game_over = len(self.empty_points) == 0

    def update_board_winner(winner):
        self.is_game_won = True
        self.is_game_over = True
        self.winner = winner

    def show_board(self):
        #just some print statements for testing. Will replace this with the visualization.
        print("x points:")
        print(self.x_points)
        print("o points:")
        print(self.o_points)
        print("empty points:")
        print(self.empty_points)
        print("is_game_won:")
        print(self.is_game_won)

#Functions

def position_to_point(position):
    pass

def previous_points_combination_generator(previous_points):
    combination_list = list(itertools.combinations(previous_points,2))
    return combination_list

#Game

#TESTING

game_board = Board()
game_board.update_board("x", (0,0))
game_board.update_board("x", (1,1))
game_board.update_board("x", (2,2))
game_board.update_board_status("x")
game_board.show_board()
