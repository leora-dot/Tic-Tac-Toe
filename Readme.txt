There are two versions of tic-tac-toe because I learned a lot from building it the first time, and I wanted to implement some of what I learned. 

The dataframe_approach folder contains the first version. 
	It uses a dataframe to track the board and was basically death by global variables. 
	It assesses whether the game has been won by checking each possible row/column/diagnol to see if they are all populated with the same character.

The linear_approach folder contains the second version:
	It uses objects for the board, the players, and visualization and the turn functionalities. 
	Rather than check specific rows/columns/diagnols, it assesses whether the game has been won by using linear algebra. First time I have used algebra?