# I'm bored, and Tyler suggested I make tic-tac-toe.

import random
import pandas as pd
import matplotlib.pyplot as plt

board_df = pd.read_csv('board.csv')

#Project Plan
# INITIALIZE GAME
# Get player names
# Flip the coin
# Announce player order
# Generate board
# Set Current turn
# Set random number
# PLAY GAME
# Set winner
# while winner = none, turn
#TURN: prompt turn, valid turn, update board, check for winner, either update current turn or announce winner

## FUNCTIONS THAT WILL POWER THE GAME GO HERE

def position_to_index(position):
    return position - 1

# This function shows the current board
def show_board():
    char_color = "blue"
    #Creating the Visualization
    plt.figure()
    for position in board_df.position.tolist():
        #Creating the Square
        ax = plt.subplot(3,3,position)
        ax.set_xlim(0,1)
        ax.set_ylim(0,1)
        ax.set_xticks([],[])
        ax.set_yticks([],[])
        ax.set_aspect(1)
        #If position is available (Identified based on the fact that nan objects are floats)
        if isinstance(board_df.symbol.iloc[position_to_index(position)], float):
            plt.scatter(1.5,1.5, label = "Press "+str(position), color = "grey")
            plt.legend(loc = "lower center")
        #If position is an o
        elif board_df.symbol.iloc[position_to_index(position)] == "o":
            draw_circle = plt.Circle((0.5,0.5), radius = .4, fill = False, color = char_color)
            ax.add_artist(draw_circle)
        #If position is an x
        else:
            plt.plot([0.2,0.8],[0.8,0.2], color = char_color)
            plt.plot([0.2,0.8],[0.2,0.8], color = char_color)
    #Show & Close
    plt.show()
    plt.close("all")
    plt.clf()

# This function adds a character to the current board
def update_board(pos,char):
    #Updating symbol
    board_df.loc[board_df.position == pos, "symbol"] = char
    #Updating support columns
    board_df["is_available"] = board_df.symbol.isna()

update_board(3,"x")
update_board(4,"o")

print(board_df)

#This function checks if a move is valid:

def is_valid_move(pos):
    return board_df.is_available.iloc[position_to_index(pos)])

is_valid_move(2)
is_valid_move(3)

def turn(current_turn):
    # Setting Player & Symbol
    if current_turn%2 == rand_val:
        player = player_x_name
        symbol = "x"
    else:
        player = player_o_name
        symbol = "o"
    print(player)
    # Introducing the Turn
    print("It's your turn, "+player+"!")
    print("Here is the current board")
    show_board()
    print("Enter a number to chose a spot to play")
    available_spots(board)
    print_available_board()
    position = None
    while position not in available_spots:
        pass

## INITIALIZE GAME

#Set Up Variables

board_df = pd.read_csv('board.csv')

current_turn = 0
rand_val = random.randint(0,1)

# Get Player Names. Player names start as generic so that the code can run even if these are commented out.

player_x_name = "Player X"
player_o_name = "Player O"

#print("Enter your name, player one:")
#player_x_name = input()
#print("Welcome, "+player_x_name +"!\n You will play x")

#print("Enter your name, player two:")
#player_o_name = input()
#print("Welcome, "+player_o_name +"!\n You will play o")

#Announcing Player Order. This is just announcements and can be commented out.

#print("Flipping a coin...")

#if rand_val == 0:
    #print(player_x_name+ "goes first!")
#else:
    #print(player_o_name+ "goes first!")

## PLAY GAME
