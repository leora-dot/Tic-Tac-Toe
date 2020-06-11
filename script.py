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
    index = position - 1
    return position

# This function shows the current board
def print_board():
    #This section creates nine figures
    plt.figure()
    for position in board_df.position.tolist():
        plt.subplot(3,3,position)
    #Show & Close
    plt.show()
    plt.close("all")
    plt.clf()

#print_board()

def update_board(pos,char):
    #Updating symbol
    board_df.loc[board_df.position == pos, "symbol"] = char
    #Updating support columns
    board_df["is_available"] = board_df.symbol.isna()
    #print(board_df)

update_board(3,"x")
update_board(4,"o")

#print(board_df)

print_board()

# This function, I want to delete
def print_available_board():
    print(str(board_with_available_spots[0])+str(board_with_available_spots[1])+str(board_with_available_spots[2]))
    print(str(board_with_available_spots[3])+str(board_with_available_spots[4])+str(board_with_available_spots[5]))
    print(str(board_with_available_spots[6])+str(board_with_available_spots[7])+str(board_with_available_spots[8]))

# This function, I also want to delete
def available_spots(board):
    global board_with_available_spots
    board_with_available_spots = []
    global available_spots
    available_spots = []
    for i in range(0,9):
        if board[i] == "-":
            board_with_available_spots.append(i)
            available_spots.append(i)
        else:
            board_with_available_spots.append(board[i])

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
    print_board()
    print("Enter a number to chose a spot to play")
    available_spots(board)
    print_available_board()
    position = None
    while position not in available_spots:
        pass

## INITIALIZE GAME

#Set Up Variables

board = ["-","-","-","-","-","-","-","-","-"]

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
