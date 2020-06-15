#This script will test whether the is_game_won function is working correctly.

#TESTING PLAN
#WHAT DO WE NEED TO DO?
    #calculate all possible cases (board cofigurations x latest position)
    #create pandas table that describes cases
    #create function that translates into board configuration x latest position inputs that can be inputted into is_game_won function
    #run is_won_function for each of these cases and add output to table.
    #add columns that recognize each potential winning combination (8 columns)
    #compare results
#CAVEATS
    #This may be impractical given the large number of possible cases -> consider random sampling
    #Because the bulk of the possible cases come from the case in which five board spots are filled, it may make sense not to add these configurations in when I'm just building the functions.
    #That case can be added later in full or in part. But no need to wait through the processing times until the end.

#Importing Libraries

import random
import pandas as pd
import matplotlib.pyplot as plt

#for factorials
import math
#for permutation
import itertools

# Importing from Game Script
from game_script import \
position_to_index, \
show_board, \
update_board, \
is_valid_move, \
is_symbol, \
turn, \
is_game_won, \
opening_sequence, \
load_empty_board

#FUNCTIONS FOR GENERATING TEST CASES GO HERE

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

#Generates latest position for a given board configuration
def position_generator(string_list):
    position_list = []
    for string in string_list:
        for i in range(len(string)):
            position_list.append((int(string), int(string[i])))
    return position_list

def is_digit_in_integer(digit,integer):
    for i in range(len(str(integer))):
        if str(digit) in (str(integer)):
            return True
    return False

#Generates board based on row in testing dataframe
def row_to_board(row_index, symbol = "x"):
    #Start with an empty board
    global board_df
    board_df = load_empty_board()
    #Update the board based on the positions described in testing_df
    if testing_df.is_pos_1.iloc[row_index]:
        update_board(1,symbol)
    if testing_df.is_pos_2.iloc[row_index]:
        update_board(2,symbol)
    if testing_df.is_pos_3.iloc[row_index]:
        update_board(3,symbol)
    if testing_df.is_pos_4.iloc[row_index]:
        update_board(4,symbol)
    if testing_df.is_pos_5.iloc[row_index]:
        update_board(5,symbol)
    if testing_df.is_pos_6.iloc[row_index]:
        update_board(6,symbol)
    if testing_df.is_pos_7.iloc[row_index]:
        update_board(7,symbol)
    if testing_df.is_pos_8.iloc[row_index]:
        update_board(8,symbol)
    if testing_df.is_pos_9.iloc[row_index]:
        update_board(9,symbol)

#Generates adds the result of the is_game_won function to the testing df.
#By default, assumes five turns have been played.
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

def drop_is_pos_columns(df):
    df.drop(columns = ["is_pos_1", "is_pos_2", "is_pos_3", "is_pos_4", "is_pos_5", "is_pos_6", "is_pos_7", "is_pos_8", "is_pos_9"], inplace = True)

def drop_combo_column(df):
    df.drop(columns = ["combo"], inplace = True)

def drop_win_combination_columns(df):
    df.drop(columns = ["is_win_123", "is_win_456", "is_win_789", "is_win_147", "is_win_258", "is_win_369", "is_win_159", "is_win_357"], inplace = True)

def result_validity_summary():
    summary = testing_df.is_result_valid.value_counts()
    print("\nResults Validity Summary:\n", summary)
    return summary

def error_type_summary():
    summary = invalid_df.error_type.value_counts()
    print("\nError Type Summary:\n", summary)
    return summary

def latest_position_summary():
    summary = invalid_df.latest_pos.value_counts()
    print("\nLatest Position Summary:\n",summary)
    return summary

def invalid_result_generator():
    invalid = testing_df[testing_df.is_result_valid == False].reset_index(drop = True)
    invalid["error_type"] = invalid.is_actual_win == True
    invalid.drop(columns = ["is_result_valid"], inplace = True)
    return invalid

#CALCULATING NUMBER OF TEST CASES

#board configurations
#At the end of the five move game a player can have filled any five spots, meaning we would need to test:
    #all possible board configurations with five spots five spots C(9,5) + four spots C(9,4) +three spots C(9,3).
    #two spots and one spots do not need to be tested since the is_game_won function defaults to False in these conditions.
    #the number of spots we need to generate is:

#print(combination_num(9,5) + combination_num(9,4) + combination_num(9,3))
#336 board configurations

#Once we have all the board configurations, we need to test each of them for all possible latest positions.
    #we don't need to do all nine since only the spots filled could have had a latest move.
    #the number of cases to test is:

#print(5*combination_num(9,5) + 4*combination_num(9,4) + 3*combination_num(9,3))
#1,386 test cases
    #Only 1,098 need to be tested as 288 are impossible

#POPULATING PANDAS TABLE WITH ALL TEST CASES

#list of board configurations
board_configuration_list = combination_list(3) #+ combination_list(4) + combination_list(5)
#list of test cases
test_case_list = position_generator(board_configuration_list)

#generating the dataframe
testing_df = pd.DataFrame(test_case_list, columns = ['combo', 'latest_pos'])

#New Columns Show Whether Each Position is Filled
testing_df["is_pos_1"] = testing_df.apply(lambda x: is_digit_in_integer(1,x["combo"]), axis =1)
testing_df["is_pos_2"] = testing_df.apply(lambda x: is_digit_in_integer(2,x["combo"]), axis =1)
testing_df["is_pos_3"] = testing_df.apply(lambda x: is_digit_in_integer(3,x["combo"]), axis =1)
testing_df["is_pos_4"] = testing_df.apply(lambda x: is_digit_in_integer(4,x["combo"]), axis =1)
testing_df["is_pos_5"] = testing_df.apply(lambda x: is_digit_in_integer(5,x["combo"]), axis =1)
testing_df["is_pos_6"] = testing_df.apply(lambda x: is_digit_in_integer(6,x["combo"]), axis =1)
testing_df["is_pos_7"] = testing_df.apply(lambda x: is_digit_in_integer(7,x["combo"]), axis =1)
testing_df["is_pos_8"] = testing_df.apply(lambda x: is_digit_in_integer(8,x["combo"]), axis =1)
testing_df["is_pos_9"] = testing_df.apply(lambda x: is_digit_in_integer(9,x["combo"]), axis =1)

#New Columns Test for Each Kind of Win, showing whether that board combo should have that win
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

#I want to pull out impossible situations, in which the game was won but not in the latest move.
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

#Is there a win on the board?
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

#Which valid win is on the board

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

#drop_is_pos_columns(testing_df)
#drop_win_combination_columns(testing_df)
#print(testing_df)

##GENERATING GAME RESULTS BASED ON THE TEST CASES

#game_result_generator()
#game_result_validator()

#INVESTIGATING ERRORS

#invalid_df = invalid_result_generator()
