# I'm bored, and Tyler suggested I make tic-tac-toe.

import random

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

# Let's make the board and set up a mechanism to print it. I want to have x,o, and -. Let's start with nine dashes.

## FUNCTIONS THAT WILL POWER THE GAME GO HERE

# This function shows the current board
def print_board():
    print(board[0]+board[1]+board[2])
    print(board[3]+board[4]+board[5])
    print(board[6]+board[7]+board[8])

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
