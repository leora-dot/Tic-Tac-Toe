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
    #Because the bulk of the possible cases come from the case in which five board spots are filled, I will ignore that case when building out testing script.
    #That case can be added later in full or in part. But no need to wait through the processing times until the end.

#importing functions needed

import random
import pandas as pd
import matplotlib.pyplot as plt

#for factorials
import math

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

#Factorial function, just a wrapper so I don't have to type.
def factorial(val):
    return math.factorial(val)

#Permutation calculator
def permutation(n,k):
    return factorial(n)/factorial((n-k))

#CALCULATING NUMBER OF TEST CASES
#At the end of the five move game a player can have filled any five spots, meaning we would need to test:
    #all possible board configurations with five spots five spots P(9,5) + four spots P(9,4) +three spots P(9,3).
    #two spots and one spots do not need to be tested since the is_game_won function defaults to False in these conditions.
    #the number of spots we need to generate is:

#print(permutation(9,5) + permutation(9,4) + permutation(9,3))
#18,648 board configurations

#Once we have all the combinations, we need to test each of them for all possible latest positions.
    #we don't need to do all nine since only the spots filled could have had a latest move.
    #In that case we have five spots (5 x 5! = 600), four spots (4 x 4! = 96), three spots (3 x 3! = 18)
    #the number of cases to test is:

#print(5*permutation(9,5) + 4*permutation(9,4) + 3*permutation(9,3))
#89,208 test cases.

#POPULATING PANDAS TABLE WITH ALL TEST CASES

testing_df = pd.read_csv('test_is_game_won.csv')
