import random
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import itertools

# TO DO LIST:
    #can you define the list of empty points with a list comprehension?
    #clean up your print statements
    #see if you can clean up the tuple unpacking
    #see if you can do a list of integers as strings efficiently
#Classes

class Board:

    def __init__(self):
        self.x_points = []
        self.o_points = []
        self.empty_points = [(0,0), (1,0), (2,0), (0,1), (1,1), (2,1), (0,2), (1,2), (2,2)]
        self.is_game_won = False
        self.is_game_over = False
        self.winner = None

    def is_valid_move(self, requested_point):
        return requested_point in self.empty_points

    def update_board(self, player, requested_point):
        self.empty_points.remove(requested_point)
        if player == player_x:
            self.x_points.append(requested_point)
        if player == player_o:
            self.o_points.append(requested_point)

    def check_for_win(self, last_player):
        #Assigning variables
        if last_player == player_x:
            previous_points = self.x_points[:-1]
            last_point = self.x_points[-1]
            turn_counter = len(self.x_points)
        if last_player == player_o:
            previous_points = self.o_points[:-1]
            last_point = self.o_points[-1]
            turn_counter = len(self.o_points)
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
                        self.update_board_winner(last_player)
                        return
                #horizontal or diagnal line:
                else:
                    m = (y2-y1)/(x2-x1)
                    b = y1 - m * x1
                    if y_last == m * x_last +b:
                        #If last_point is on that line, game is won
                        self.update_board_winner(last_player)
                        return
            #If the game is not won, check for a tie
            self.is_game_over = len(self.empty_points) == 0

    def update_board_winner(self, winner):
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

class Player:

    def __init__(self, symbol):
        self.symbol = symbol
        #default name
        self.name = "Player "+self.symbol

    def update_name(self, name):
        #later, add input request to this function
        self.name = name

    def get_name(self):
        return self.name

class TurnLoop:
    def __init__(self):
        #Game Set Up
        self.turn_counter = 0
        self.rand_value = random.randint(0,1)
        self.players = [player_x, player_o]
        self.current_player = self.players[self.turn_counter%2]
        print("Flipping a coin...")
        print(str(self.current_player.get_name) + "goes first!")
        #Game Loop
        while game_board.is_game_over == False:
            self.prompt_move()
            self.implement_move()
        self.announce_end

    def switch_player(self):
        self.turn_counter += 1
        self.current_player = self.players[self.turn_counter%2]

    def prompt_move(self):
        self.requested_point = None
        while self.requested_point == None:
            print("It's your turn, " + str(self.current_player.get_name))
            print("Where would you like to go?")
            game_board.show_board()
            requested_position = input()
            if self.is_valid_move(requested_position):
                self.requested_point = position_to_point(int(requested_position))
                print(self.requested_point)

    def is_valid_move(self,requested_position):
        #When the requested position comes in, it's a string. We check to see if it's an acceptable one.
        if requested_position not in ["1","2","3","4","5","6","7","8","9"]:
            print(str(requested_position) + "isn't a spot on the board!")
            return False
        #If it's valid, we can turn it into a point and check for emptiness
        requested_point = position_to_point(int(requested_position))
        if requested_point not in game_board.empty_points:
            print("Oops! "+(str(requested_position))+ "is already filled!")
            return False
        #If we haven't returned yet, all is well!
        return True

    def implement_move(self):
        game_board.update_board(self.current_player, self.requested_point)
        game_board.check_for_win(self.current_player)
        self.switch_player()

    def announce_end(self):
        if game_board.is_game_won:
            print(game_board.winner+ "wins! Congratulations!")
        else:
            print("It's a tie!")
        game_board.show_board

#Functions

def previous_points_combination_generator(previous_points):
    combination_list = list(itertools.combinations(previous_points,2))
    return combination_list

def position_to_point(position):
    dict = {
 1: (0, 2),
 2: (1, 2),
 3: (2, 2),
 4: (0, 1),
 5: (1, 1),
 6: (2, 1),
 7: (0, 0),
 8: (1, 0),
 9: (2, 0)
}
    return dict.get(position)

#game_board

#TESTING

game_board = Board()
player_x = Player("x")
player_o = Player("o")
game = TurnLoop()

#game_board.update_board(player_x, (0,0))
#game_board.update_board(player_x, (1,1))
#game_board.update_board(player_x, (2,2))
#game_board.check_for_win(player_x)
#game_board.show_board()
