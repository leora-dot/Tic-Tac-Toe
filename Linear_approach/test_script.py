##TO DO
    #REDEFINE game_result_generator
    #clean up all the documentation from the old test script.
    #figure out new df based on move orders

##PART 1: IMPORT LIBRARIES & IMPORT CLASSES & FUNCTIONS

#Importing Libraries

import random
import pandas as pd
import numpy as np
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
point_to_position, \
point_list, \
player_x

#player_x = Player("x")
#player_o = Player("o")

## PART 2: FUNCTIONS

#Factorial Function (just a wrapper)
def factorial(val):
    return math.factorial(val)

#Generates number of combinations (used for calculatin number of board configurations)
def combination_num(n,r):
    return factorial(n)/((factorial(r)*factorial(n-r)))

def permutation_num(n,r):
    return factorial(n)/factorial(n-r)

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

def permutation_list(k, n = 10):
    #this generates a list of lists
    perms_list = list(itertools.permutations(list(range(1,n)),k))
    #generating strings with each item
    perms_strings = []
    for perm in perms_list:
        string = ""
        for i in range(len(perm)):
            string += str(perm[i])
        perms_strings.append(string)
    return perms_strings

# FUNCTIONS FOR GENERATING GAME RESULTS

#Generates adds the result of the is_game_won function to the testing df.

def game_result_generator(player = player_x):
    testing_df["is_actual_win"] = ""
    #for each row, create a new test board and identify the combo
    for row_index in list(range(testing_df.is_valid_win.count())):
        test_board = Board(point_list)
        combo = testing_df.combo.iloc[row_index]
        #for each item in the combo, update the board
        for i in list(range(len(combo))):
            test_board.update_board(player, position_to_point(combo[i]))
        #after the board has been updatd, check for wins
        test_board.check_for_win(player)
        testing_df.at[row_index,"is_actual_win"] = test_board.is_game_won

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
    #1-2 x on the board: these cases are irrelevant. The is_game_won returns false until the players have had the opportunity to fill three positions.
    #3 x's on the board: P(9,3) possibilities.
    #4 x's on the board: P(9,4) possibilities.
    #5 x's on the board: P(9,5) possibilities.
    #6+ x's on the board: these cases are impossible. No character can occupy more than five positions on the board.

#print(permutation_num(9,5) + permutation_num(9,4) + permutation_num(9,3))
    #18,648 test scenarios
        #12,600 need to be tested
        #6,048 are impossible and can be removed
    #See how long it takes - you might have to take a sample.

#GENERATING A DATAFRAME THAT DESCRIBES ALL THE POSSIBLE COMBINATIONS

#list of board configurations
board_configuration_list = permutation_list(3) + permutation_list(4) + permutation_list(5)

#generating the dataframe
testing_df = pd.DataFrame(board_configuration_list, columns = ['combo'])

#testing_df["latest_pos"] = type(testing_df["combo"])

testing_df["latest_pos"] = testing_df["combo"].astype(str).str[-1].astype(np.int64)

#New Columns Show Whether Each Position is Filled

def is_digit_in_integer(digit,integer):
    for i in range(len(str(integer))):
        if str(digit) in (str(integer)):
            return True
    return False

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

#print(testing_df)

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

testing_df.drop(columns = ["is_pos_1", "is_pos_2", "is_pos_3", "is_pos_4", "is_pos_5", "is_pos_6", "is_pos_7", "is_pos_8", "is_pos_9"], inplace = True)
testing_df.drop(columns = ["is_win_123", "is_win_456", "is_win_789", "is_win_147", "is_win_258", "is_win_369", "is_win_159", "is_win_357"], inplace = True)

#print(testing_df)

#RUNNING THE GAME FOR EACH SCENARIO DESCRIBED IN THE TESTING SCENARIO & EVALUATING WHETHER RESULTS ARE CORRECT.

game_result_generator()
game_result_validator()

result_validity_summary()

#print(testing_df)

#INVESTIGATING ERRORS

#invalid_df = invalid_result_generator()

#drop_is_pos_columns(invalid_df)
#drop_win_combination_columns(invalid_df)
#print(invalid_df)


#error_type_summary()
#latest_position_summary()
#valid_win_location_summary()
