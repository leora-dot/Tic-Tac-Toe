##TO DO
    #REDEFINE game_result_generator
    #clean up all the documentation from the old test script.

##PART 1: IMPORT LIBRARIES & IMPORT CLASSES & FUNCTIONS

#Importing Libraries

import random
import pandas as pd
import matplotlib.pyplot as plt

import math
import itertools

#Importing Game Functions

from game_script import \
point_list, \
Board, \
Visualize_Board, \
Player, \
TurnLoop, \
previous_points_combination_generator, \
position_to_point, \
point_to_position

player_x = Player("x")
player_o = Player("o")

## PART 2: FUNCTIONS

#FACTORIAL & COMBINATION FUNCTIONS

#Factorial Function (just a wrapper)
def factorial(val):
    return math.factorial(val)

#Generates number of combinations (used for calculatin number of board configurations)
def combination_num(n,r):
    return factorial(n)/((factorial(r)*factorial(n-r)))

#Generates combinations for n choose k.
#n defaults to ten since we will ultimately be chosing k positions out of 9 positions.
def combination_list(k, n = 10):
    #this generates a list of lists
    combs_list = list(itertools.combinations(list(range(1,n)),k))
    #generating strings with each item
    combs_strings = []
    for comb in combs_list:
        string = ""
        for i in range(len(comb)):
            string += str(comb[i])
        combs_strings.append(string)
    return combs_strings

#EDITING FUNCTIONS & BASIC CHECKS

def is_digit_in_integer(digit,integer):
    for i in range(len(str(integer))):
        if str(digit) in (str(integer)):
            return True
    return False

def drop_is_pos_columns(df):
    df.drop(columns = ["is_pos_1", "is_pos_2", "is_pos_3", "is_pos_4", "is_pos_5", "is_pos_6", "is_pos_7", "is_pos_8", "is_pos_9"], inplace = True)

def drop_combo_column(df):
    df.drop(columns = ["combo"], inplace = True)

def drop_win_combination_columns(df):
    df.drop(columns = ["is_win_123", "is_win_456", "is_win_789", "is_win_147", "is_win_258", "is_win_369", "is_win_159", "is_win_357"], inplace = True)

#FUNCTIONS FOR GENERATING THE TESTING_DF

#Generates latest position for a given board configuration
def position_generator(string_list):
    position_list = []
    for string in string_list:
        for i in range(len(string)):
            position_list.append((int(string), int(string[i])))
    return position_list

#generates columns for each position, showing whether it has been filled
def is_pos_generator():
    testing_df["is_pos_1"] = testing_df.apply(lambda x: is_digit_in_integer(1,x["combo"]), axis =1)
    testing_df["is_pos_2"] = testing_df.apply(lambda x: is_digit_in_integer(2,x["combo"]), axis =1)
    testing_df["is_pos_3"] = testing_df.apply(lambda x: is_digit_in_integer(3,x["combo"]), axis =1)
    testing_df["is_pos_4"] = testing_df.apply(lambda x: is_digit_in_integer(4,x["combo"]), axis =1)
    testing_df["is_pos_5"] = testing_df.apply(lambda x: is_digit_in_integer(5,x["combo"]), axis =1)
    testing_df["is_pos_6"] = testing_df.apply(lambda x: is_digit_in_integer(6,x["combo"]), axis =1)
    testing_df["is_pos_7"] = testing_df.apply(lambda x: is_digit_in_integer(7,x["combo"]), axis =1)
    testing_df["is_pos_8"] = testing_df.apply(lambda x: is_digit_in_integer(8,x["combo"]), axis =1)
    testing_df["is_pos_9"] = testing_df.apply(lambda x: is_digit_in_integer(9,x["combo"]), axis =1)

#Generates board based on row in testing dataframe
def row_to_board(row_index, player = player_x):
    #Start with an empty board)
    test_board = Board()
    #Update the board based on the positions described in testing_df
    if testing_df.is_pos_1.iloc[row_index]:
        test_board.update_board(player, position_to_point(1))
    if testing_df.is_pos_2.iloc[row_index]:
        test_board.update_board(player, position_to_point(2))
    if testing_df.is_pos_3.iloc[row_index]:
        test_board.update_board(player, position_to_point(3))
    if testing_df.is_pos_4.iloc[row_index]:
        test_board.update_board(player, position_to_point(4))
    if testing_df.is_pos_5.iloc[row_index]:
        test_board.update_board(player, position_to_point(5))
    if testing_df.is_pos_6.iloc[row_index]:
        test_board.update_board(player, position_to_point(6))
    if testing_df.is_pos_7.iloc[row_index]:
        test_board.update_board(player, position_to_point(7))
    if testing_df.is_pos_8.iloc[row_index]:
        test_board.update_board(player, position_to_point(8))
    if testing_df.is_pos_9.iloc[row_index]:
        test_board.update_board(player, position_to_point(9))

# FUNCTIONS FOR GENERATING GAME RESULTS

#Generates adds the result of the is_game_won function to the testing df.
#By default, assumes 6 turns have been played.

def game_result_generator(symbol = "x", turn_count = 6):
    testing_df["is_actual_win"] = ""
    #Adding game results based on each row in counter.
    for row_index in range(testing_df.is_valid_win.count()):
        #create the board
        row_to_board(row_index, symbol)
        #generate game result - this isn't working right.
        game_result = is_game_won(testing_df.latest_pos.iloc[row_index],symbol,turn_count)
        testing_df.at[row_index,"is_actual_win"] = game_result

def game_result_validator():
    testing_df["is_result_valid"] = testing_df.is_actual_win == testing_df.is_valid_win

#FUNCTIONS FOR GENERATING THE INVALID DF

def invalid_result_generator():
    #selecting rows with invalid results
    invalid = testing_df[testing_df.is_result_valid == False].reset_index(drop = True)
    invalid.drop(columns = ["is_result_valid"], inplace = True)
    return invalid

#FUNCTIONS FOR SUMARIZING THE INVALID DF

def result_validity_summary():
    summary = testing_df.is_result_valid.value_counts()
    print("\nResults Validity Summary:\n", summary)
    return summary

def error_type_summary():
    summary = testing_df.groupby(["is_valid_win", "is_actual_win"]).latest_pos.count().reset_index()
    print("\nError Type Summary:\n", summary)
    return summary

def latest_position_summary():
    summary = invalid_df.latest_pos.value_counts()
    summary.sort_values(inplace = True)
    print("\nLatest Position Summary:\n",summary)
    return summary

def valid_win_location_summary():
    summary = invalid_df.valid_win_location.value_counts()
    print("\nValid Win Location Summary:\n", summary)
    return summary

##PART 3: IDENTIFYING TEST CASES

#WHAT CASES DO WE NEED TO TEST IN ORDER TO BE SATISFIED THAT THE GAME IS WORKING CORRECTLY?

#Because the is_game_won function looks only at one symbol, I am going to focus on the spots occupied by x only.
#How many different ways can the board be filled with x's?
    #1-2 x on the board: these cases are irrelevant. The is_game_won function returns false until the players have had the opportunity to fill three positions.
    #3 x's on the board: C(9,3) possibilities.
    #4 x's on the board: C(9,4) possibilities.
    #5 x's on the board: C(9,5) possibilities.
    #6+ x's on the board: these cases are impossible. No character can occupy more than five positions on the board.

#print(combination_num(9,5) + combination_num(9,4) + combination_num(9,3))
#336 board configurations

#Because the is_game_won function depends on the most recent move played, we need to test each of the above board configurations with each possible latest played position.

#print(5*combination_num(9,5) + 4*combination_num(9,4) + 3*combination_num(9,3))
#1,386 test cases
    #Only 1,098 need to be tested as 288 are impossible (ie, moves were placed on the board after the game was already won) if the possible 1,098 cases are evaluated correctly.

#GENERATING A DATAFRAME THAT DESCRIBES ALL THE POSSIBLE COMBINATIONS

#list of board configurations
board_configuration_list = combination_list(3) + combination_list(4) + combination_list(5)
#list of test cases
test_case_list = position_generator(board_configuration_list)

#generating the dataframe
testing_df = pd.DataFrame(test_case_list, columns = ['combo', 'latest_pos'])

#New Columns Show Whether Each Position is Filled

is_pos_generator()

#Adding to the dataframe whether each scenario should have resulted in a win.
#winning by row
testing_df["is_win_123"] = testing_df.apply(lambda x: (x["is_pos_1"] == True) and (x["is_pos_2"] == True) and (x["is_pos_3"] == True), axis =1)
testing_df["is_win_456"] = testing_df.apply(lambda x: (x["is_pos_4"] == True) and (x["is_pos_5"] == True) and (x["is_pos_6"] == True), axis =1)
testing_df["is_win_789"] = testing_df.apply(lambda x: (x["is_pos_7"] == True) and (x["is_pos_8"] == True) and (x["is_pos_9"] == True), axis =1)
#winning by column
testing_df["is_win_147"] = testing_df.apply(lambda x: (x["is_pos_1"] == True) and (x["is_pos_4"] == True) and (x["is_pos_7"] == True), axis =1)
testing_df["is_win_258"] = testing_df.apply(lambda x: (x["is_pos_2"] == True) and (x["is_pos_5"] == True) and (x["is_pos_8"] == True), axis =1)
testing_df["is_win_369"] = testing_df.apply(lambda x: (x["is_pos_3"] == True) and (x["is_pos_6"] == True) and (x["is_pos_9"] == True), axis =1)
#winning by diagnal
testing_df["is_win_159"] = testing_df.apply(lambda x: (x["is_pos_1"] == True) and (x["is_pos_5"] == True) and (x["is_pos_9"] == True), axis =1)
testing_df["is_win_357"] = testing_df.apply(lambda x: (x["is_pos_3"] == True) and (x["is_pos_5"] == True) and (x["is_pos_7"] == True), axis =1)

#I want to pull out impossible situations, in which the game was won and then additional moves were played.
#The is_game_won function will work incorrectly in these cases, but if it is working correctly, these cases will never occur.

testing_df["is_impossible"] = testing_df.apply(lambda x: \
((x["is_win_123"] == True) and x["latest_pos"] not in [1,2,3]) or \
((x["is_win_456"] == True) and x["latest_pos"] not in [4,5,6]) or \
((x["is_win_789"] == True) and x["latest_pos"] not in [7,8,9]) or \
((x["is_win_147"] == True) and x["latest_pos"] not in [1,4,7]) or \
((x["is_win_258"] == True) and x["latest_pos"] not in [2,5,8]) or \
((x["is_win_369"] == True) and x["latest_pos"] not in [3,6,9]) or \
((x["is_win_159"] == True) and x["latest_pos"] not in [1,5,9]) or \
((x["is_win_357"] == True) and x["latest_pos"] not in [3,5,7]),
axis =1)

#possibility_table = testing_df.groupby("is_impossible").combo.count()
#print(possibility_table)

testing_df = testing_df[testing_df.is_impossible == False].reset_index(drop = True)
testing_df.drop(columns = ["is_impossible"], inplace = True)

#Adding to the table whether there is a win on the board.
testing_df["is_valid_win"] = testing_df.apply(lambda x: \
(x["is_win_123"] == True) or \
(x["is_win_456"] == True) or \
(x["is_win_789"] == True) or \
(x["is_win_147"] == True) or \
(x["is_win_258"] == True) or \
(x["is_win_369"] == True) or \
(x["is_win_159"] == True) or \
(x["is_win_357"] == True),
axis =1)

#I really do not want all these columns. Creating a single column that shows how the board has been won.

testing_df["valid_win_location"] = ""

for row_index in range(testing_df.is_valid_win.count()):
    win = None
    if testing_df.is_win_123.iloc[row_index]:
        win = 123
    elif testing_df.is_win_456.iloc[row_index]:
        win = 456
    elif testing_df.is_win_789.iloc[row_index]:
        win = 789
    elif testing_df.is_win_147.iloc[row_index]:
        win = 147
    elif testing_df.is_win_258.iloc[row_index]:
        win = 258
    elif testing_df.is_win_369.iloc[row_index]:
        win = 369
    elif testing_df.is_win_159.iloc[row_index]:
        win = 159
    elif testing_df.is_win_357.iloc[row_index]:
        win = 357
    testing_df.at[row_index,"valid_win_location"] = win

#print(testing_df)

#RUNNING THE GAME FOR EACH SCENARIO DESCRIBED IN THE TESTING SCENARIO & EVALUATING WHETHER RESULTS ARE CORRECT.

#game_result_generator()
#game_result_validator()

#INVESTIGATING ERRORS

#invalid_df = invalid_result_generator()

#drop_is_pos_columns(invalid_df)
#drop_win_combination_columns(invalid_df)
#print(invalid_df)

#result_validity_summary()
#error_type_summary()
#latest_position_summary()
#valid_win_location_summary()
