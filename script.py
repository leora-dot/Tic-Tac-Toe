#Tyler suggested that I make a tic-tac-toe game. The challenge is to be as efficient as possible in checking whether or not the game has been won.
#Just for fun (since this is a distraction from the data science coding), I am adding a visualization

import random
import pandas as pd
import matplotlib.pyplot as plt

## FUNCTIONS THAT WILL POWER THE GAME GO HERE

#this function turns board position numbers (1-9) into board_df index numbers (0-8)
def position_to_index(position):
    return position-1

#this function shows a visual of the current board, using matplotlib
def show_board():
    #the color for x and o characters
    char_color = "blue"
    #Creating the visualization. A figure which will hold the grid
    plt.figure()
    #Creating the nine subplots one at a time
    for position in board_df.position.tolist():
        #Creating the a 1x2 square for the border
        ax = plt.subplot(3,3,position)
        ax.set_xlim(0,1)
        ax.set_ylim(0,1)
        ax.set_xticks([],[])
        ax.set_yticks([],[])
        ax.set_aspect(1)
        #If the square is empty, we want to show how to select it.
        if isinstance(board_df.symbol.iloc[position_to_index(position)], float):
            #The scatterplot adds a single point, which is not shown.
            #Its legend acts as the instruction for the player.
            plt.scatter(1.5,1.5, label = "Press "+str(position), color = "grey")
            plt.legend(loc = "lower center")
        #If the square has an "o"
        elif board_df.symbol.iloc[position_to_index(position)] == "o":
            draw_circle = plt.Circle((0.5,0.5), radius = .4, fill = False, color = char_color)
            ax.add_artist(draw_circle)
        #If the square has an x
        else:
            #two lines make an x
            plt.plot([0.2,0.8],[0.8,0.2], color = char_color)
            plt.plot([0.2,0.8],[0.2,0.8], color = char_color)
    #Show & Close
    plt.show()
    plt.close("all")
    plt.clf()

# This function adds a character to the current board
def update_board(pos,char):
    #Bringing in global parameters
    global center_symbol
    global current_turn
    global is_board_full
    #Updating the position column
    board_df.loc[board_df.position == pos, "symbol"] = char
    #Updating the is_available column
    board_df["is_available"] = board_df.symbol.isna()
    #Update center square if applicable
    if requested_pos == 5:
        center_symbol = char
    if current_turn > 8:
        is_board_full = board_df.position.isna().count() == 0:

#This function checks if a move is valid:
def is_valid_move(pos):
    return board_df.is_available.iloc[position_to_index(pos)]

#This function checks whether every position in a list is marked with a given symbol
def is_symbol(symbol,pos_list):
    for pos in pos_list:
        if board_df.symbol.iloc[position_to_index(pos)] != symbol:
            return False
    return True

def turn(turn_val):
    #bringing in global parameters
    global current_turn
    global winner
    global is_board_full
    #The current player, as well as their name and symbol, are identified based on whether the current turn is odd or even.
    if turn_val%2 == rand_val:
        player = player_x_name
        symbol = "x"
    else:
        player = player_o_name
        symbol = "o"
    #This variable tracks whether the board has been updated this turn.
    is_board_updated = False
    #Announcing whose turn it is
    print("It's your turn, "+player+"!")
    # Until the board has been updated, the turn loops through prompts to chose a position.
    while is_board_updated == False:
        print("Review the current board then enter the number of the spot you'd like to mark.")
        show_board()
        requested_pos = int(input())
        #If the requested position is valid and empty, update the board
        if is_valid_move(requested_pos):
            update_board(requested_pos, symbol)
            #Set board as updated, breaking the loop
            is_board_updated = True
        #If the requested position is not valid or empty, continue the loop
        else:
            print(str(requested_pos)+" isn't a valid empty spot. \nThe numbers associated with each available spot are shown on the board.")
    #If the game has been won, declare a winner, print a congratulations, and show the final board
    if is_game_won(requested_pos,symbol):
        winner = player
        print(player + "wins! Congratulations")
        show_board()
        return
    #If the board is full with no winner, declare a tie
    elif is_board_full == True:
        print("It's a tie!")
        show_board()
        return
    #If the game is not won, add a value to the turn counter
    else:
        current_turn +=1
        return

#This function checks if the game has been won, based on the position and symbol marked in the latest turn. I haven't tested it yet!
def is_game_won(turn_position,turn_symbol):
    #If less than five turns have been played, it is impossible for either player to have won.
    #Note, the function uses 4 because the turn counter starts at zero.
    if current_turn < 4:
        return False
    #For non-corner, non-center positions, the function checks the relevant row and column.
    elif turn_position == 2:
        if (is_symbol(turn_symbol, [1,3])) or (is_symbol(turn_symbol, [5,8])):
            return True
    elif turn_position == 4:
        if (is_symbol(turn_symbol, [5,6])) or (is_symbol(turn_symbol, [1,7])):
            return True
    elif turn_position == 6:
        if (is_symbol(turn_symbol, [4,5])) or (is_symbol(turn_symbol, [3,9])):
            return True
    elif turn_position == 8:
        if (is_symbol(turn_symbol, [7,9])) or (is_symbol(turn_symbol, [2,5])):
            return True
    #For corner positions, the function checks row, columns, and diagnols if the symbol played in the latest turn has the center spot.
    #If the symbol does not hold the center spot, only the row and column are checked.
    elif turn_position == 1:
        if center_symbol == turn_symbol:
            if (is_symbol(turn_symbol, [2,3])) or (is_symbol(turn_symbol, [4,7])) or (is_symbol(turn_symbol,[9])):
                return True
        elif (is_symbol(turn_symbol, [2,3])) or (is_symbol(turn_symbol, [4,7])):
            return True
    elif turn_position == 3:
        if center_symbol == turn_symbol:
            if (is_symbol(turn_symbol, [1,2])) or (is_symbol(turn_symbol, [6,9])) or (is_symbol(turn_symbol,[7])):
                return True
        elif (is_symbol(turn_symbol, [1,2])) or (is_symbol(turn_symbol, [6,9])):
            return True
    elif turn_position == 7:
        if center_symbol == turn_symbol:
            if (is_symbol(turn_symbol, [8,9])) or (is_symbol(turn_symbol, [1,4])) or (is_symbol(turn_symbol,[3])):
                return True
        elif (is_symbol(turn_symbol, [8,9])) or (is_symbol(turn_symbol, [1,4])):
            return True
    elif turn_position == 9:
        if center_symbol == turn_symbol:
            if (is_symbol(turn_symbol, [7,8])) or (is_symbol(turn_symbol, [3,6])) or (is_symbol(turn_symbol,[1])):
                return True
        elif (is_symbol(turn_symbol, [7,8])) or (is_symbol(turn_symbol, [3,6])):
            return True
    #If the player has just played the center spot, we check all the possible winning options.
    #This shouldn't happen too often since the center spot is usually claimed in the first five turns.
    elif turn_position == 5:
        if (is_symbol(turn_symbol, [4,6])) or (is_symbol(turn_symbol, [2,8])) or (is_symbol(turn_symbol,[1,9])) or (is_symbol(turn_symbol,[3,7])):
            return True
    #If all our checks haven't found a winning combination, return False
    else:
        return False

## INITIALIZE GAME

#Load empty board dataframe
board_df = pd.read_csv('board.csv')
#No player has marked the center square yet
center_symbol = None
#Board is not full
is_board_full = False
#No player has won yet
winner = None
#Set our turn counter at zero
current_turn = 0
#Select a random number to chose who goes first
rand_val = random.randint(0,1)

#LEARN PLAYER NAMES

#Generic names will be overwritten by player input but allow the rest of this section to be commented out while testing other areas.
player_x_name = "Player X"
player_o_name = "Player O"

#Request that players enter their names
#the first player to enter their name will play x
#print("Enter your name, player one:")
#player_x_name = input()
#print("Welcome, "+player_x_name +"!\n You will play x")

#the second player to enter their name will play y
#print("Enter your name, player two:")
#player_o_name = input()
#print("Welcome, "+player_o_name +"!\n You will play o")

# ANNOUNCE WHO WILL GO FIRST
# this section is just text and can be commented out while testing other areas.

#print("Flipping a coin...")

#decide who will go first based on random value
#if rand_val == 0:
    #print(player_x_name+ "goes first!")
#else:
    #print(player_o_name+ "goes first!")

## PLAY GAME
