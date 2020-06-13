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

#importing functions needed

import random
import pandas as pd
import matplotlib.pyplot as plt

#for factorials
import math
#for permutation
import itertools

from game_script import \
position_to_index, \
show_board, \
update_board, \
is_valid_move, \
is_symbol, \
turn, \
is_game_won, \
opening_sequence, \
board_df

#Functions go here

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

#POPULATING PANDAS TABLE WITH ALL TEST CASES

#list of board configurations
board_configuration_list = combination_list(3) #+ combination_list(4) + combination_list(5)
#list of test cases
test_case_list = position_generator(board_configuration_list)

#generating the dataframe
testing_df = pd.DataFrame(test_case_list, columns = ['combo', 'latest_pos'])

#populating columns for each symbol
testing_df["is_pos_1"] = testing_df.apply(lambda x: is_digit_in_integer(1,x["combo"]), axis =1)
testing_df["is_pos_2"] = testing_df.apply(lambda x: is_digit_in_integer(2,x["combo"]), axis =1)
testing_df["is_pos_3"] = testing_df.apply(lambda x: is_digit_in_integer(3,x["combo"]), axis =1)
testing_df["is_pos_4"] = testing_df.apply(lambda x: is_digit_in_integer(4,x["combo"]), axis =1)
testing_df["is_pos_5"] = testing_df.apply(lambda x: is_digit_in_integer(5,x["combo"]), axis =1)
testing_df["is_pos_6"] = testing_df.apply(lambda x: is_digit_in_integer(6,x["combo"]), axis =1)
testing_df["is_pos_7"] = testing_df.apply(lambda x: is_digit_in_integer(7,x["combo"]), axis =1)
testing_df["is_pos_8"] = testing_df.apply(lambda x: is_digit_in_integer(8,x["combo"]), axis =1)
testing_df["is_pos_9"] = testing_df.apply(lambda x: is_digit_in_integer(9,x["combo"]), axis =1)

print(testing_df.head(10))
print(testing_df.tail(10))
