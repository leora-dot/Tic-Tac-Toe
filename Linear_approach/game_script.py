import random
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import itertools

point_list = [(0,2), (1,2), (2,2), (0,1), (1,1), (2,1), (0,0), (1,0), (2,0)]

# TO DO LIST:
    #can you define the list of empty points with a list comprehension?
    #clean up your print statements
    #see if you can do a list of integers as strings efficiently
    #testing
    #do the dictionary thing
    #search every goddamn time you use str() and be smarter

#Classes

class Board:

    def __init__(self):
        self.x_points = []
        self.o_points = []
        self.empty_points = point_list
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
            x_last, y_last = last_point
            previous_points_combinations = previous_points_combination_generator(previous_points)
            for combination in previous_points_combinations:
                #assign variables
                point1, point2 = combination
                x1, y1 = point1
                x2, y2 = point2
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
        current_board = Visualize_Board()
        current_board.visualization()

class Visualize_Board:

    def __init__(self):
        self.x_color = "cornflowerblue"
        self.o_color = "mediumspringgreen"
        self.fig = plt.figure(figsize = (6,6))
        self.gs1 = gridspec.GridSpec(3, 3)
        self.gs1.update(wspace=0.0, hspace=0.0)

    def square(self, position):
        self.ax = self.fig.add_subplot(self.gs1[position - 1])
        self.ax.set_xlim(0,1)
        self.ax.set_ylim(0,1)
        self.ax.set_xticks([],[])
        self.ax.set_yticks([],[])

    def draw_o(self):
        self.draw_circle = plt.Circle((0.5,0.5), radius = .4, fill = False, color = self.o_color)
        self.ax.add_artist(self.draw_circle)

    def draw_x(self):
        plt.plot([0.2,0.8],[0.8,0.2], color = self.x_color)
        plt.plot([0.2,0.8],[0.2,0.8], color = self.x_color)

    def draw_legend(self, position):
        plt.scatter(1.5,1.5, label = "Press "+str(position), color = "grey")
        plt.legend(loc = "lower center")

    def visualization(self):
        for i in list(range(1,10)):
            self.square(i)
            if position_to_point(i) in game_board.x_points:
                self.draw_x()
            elif position_to_point(i) in game_board.o_points:
                self.draw_o()
            else:
                self.draw_legend(i)
        plt.show()

class Player:

    def __init__(self, symbol):
        self.symbol = symbol
        self.name = "Player "+self.symbol

    def update_name(self):
        print("What's your name?")
        requested_name = input()
        self.name = requested_name
        print("Welcome, "+str(self.get_name()+ ". You'll play "+str(self.symbol)))

    def get_name(self):
        return self.name

class TurnLoop:
    def __init__(self):
        #Game Set Up
        self.players = [player_x, player_o]
        self.turn_counter = 0
        self.random_value = random.randint(0,1)
        self.current_player = self.players[(self.turn_counter + self.random_value)%2]

        print("Flipping a coin...")
        print(str(self.current_player.get_name()) + " goes first!")

        #Game Loop
        while game_board.is_game_over == False:
            self.prompt_move()
            self.implement_move()
        self.announce_end()

    def switch_player(self):
        self.turn_counter += 1
        self.current_player = self.players[(self.turn_counter + self.random_value)%2]

    def prompt_move(self):
        self.requested_point = None
        while self.requested_point == None:
            print("It's your turn, " + str(self.current_player.get_name()))
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
            print(str(game_board.winner.get_name())+ " wins! Congratulations!")
        else:
            print("It's a tie!")
        game_board.show_board()

#Functions

def previous_points_combination_generator(previous_points):
    combination_list = list(itertools.combinations(previous_points,2))
    return combination_list

point_list = [(0,2), (1,2), (2,2), (0,1), (1,1), (2,1), (0,0), (1,0), (2,0)]

def position_to_point(position):
    #function may take both string and integer input
    if type(position) == str:
        position = str(int(position))
    #Now do the lookup
    return point_list[position - 1]

def point_to_position(point):
    return point_list.index(point) + 1

#TESTING

if __name__ == "__main__":
    game_board = Board()
    player_x = Player("x")
    player_o = Player("o")
    #player_x.update_name()
    #player_o.update_name()
    #game = TurnLoop()
