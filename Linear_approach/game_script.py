import random
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import itertools

#this is the list of points on the board. It is referenced by position_to_point and point_to_position.
offset = 0.1
point_list = [(0 + offset * 2,2), (1 + offset * 2 ,2), (2 +  offset * 2 ,2), (0 + offset ,1), (1 + offset ,1), (2 + offset , 1), (0,0), (1,0), (2,0)]

#Classes

class Board:

    def __init__(self, point_values):
        self.x_points = []
        self.o_points = []
        self.empty_points = [x for x in point_values]
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
        #If the last_player has played less than three points, they cannot have won.
        if turn_counter < 3:
            return
        #You win if the last point you played is on the same line as any of the two points you played in previous turns.
        else:
            #the x & y coordinates of the last point you played.
            x_last, y_last = last_point
            #all the possible combinations of two points, selected from your previously played points.
            previous_points_combinations = previous_points_combination_generator(previous_points)
            #now we loop through each set of two points, checking to see if the latest point is on a line with them.
            for combination in previous_points_combinations:
                #the x & y coordinates of the previous points
                point1, point2 = combination
                x1, y1 = point1
                x2, y2 = point2

                m = (y2-y1)/(x2-x1)
                b = y1 - m * x1
                if abs( y_last - (m * x_last +b)) < 0.000001: #THESE WOULD BE EQUAL IF NOT FOR ROUNDING ERROR
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
        print("Welcome, {}! You'll play {}.".format(str(self.get_name()), str(self.symbol)))

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
        print("{} will go first!".format(str(self.current_player.get_name())))

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
            print("It's your turn, {}. Where would you like to go?".format(str(self.current_player.get_name())))
            game_board.show_board()
            requested_position = input()
            if self.is_valid_move(requested_position):
                self.requested_point = position_to_point(requested_position)

    def is_valid_move(self,requested_position):
        #When the requested position comes in, it's a string. We check to see if it's an acceptable one.
        if requested_position not in ["1","2","3","4","5","6","7","8","9"]:
            print("{} isn't a spot on the board!".format(str(requested_position)))
            return False
        #If it's valid, we can turn it into a point and check for emptiness
        requested_point = position_to_point(requested_position)
        if requested_point not in game_board.empty_points:
            print("Oops! {} is already filled!".format(str(requested_position)))
            return False
        #If we haven't returned yet, all is well!
        return True

    def implement_move(self):
        game_board.update_board(self.current_player, self.requested_point)
        game_board.check_for_win(self.current_player)
        self.switch_player()

    def announce_end(self):
        if game_board.is_game_won:
            print("{} wins! Congratulations!".format(str(game_board.winner.get_name())))
        else:
            print("It's a tie!")
        game_board.show_board()

#Functions

def previous_points_combination_generator(previous_points):
    combination_list = list(itertools.combinations(previous_points,2))
    return combination_list

def position_to_point(position):
    #function may take both string and integer input
    if type(position) == str:
        position = int(position)
    #Now do the lookup
    return point_list[position - 1]

def point_to_position(point):
    return point_list.index(point) + 1

##GAME

game_board = Board(point_list)
player_x = Player("x")
player_o = Player("o")

if __name__ == "__main__":
    player_x.update_name()
    player_o.update_name()
    game = TurnLoop()
