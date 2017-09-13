REVERSI GAME --Yitong Chen


I. PROGRAM DESCRIPTION
- This program runs the reversi game. Reversi is a game played between two opponent players, with two kinds of tokens, black and white for each player. Traditionally, the game is played on an 8*8 uncheckeded board. In this gaming program, the user can choose from two board sizes, as will be introduced later.
- To play the game, the user lays his/her token, following the rule that s/he can only place tokens where there are and there are only opponent tokens in between the new token and an existing token of the player's on the board. By placing his token, the user can then flip the opponent tokens surrounded by his tokens. The goal is to get as many of your tokens on the board as possible when the game ends. The game ends when the whole board is occupied or there are only tokens of one side on the board.
- This gaming program features two board sizes, a small one (4 * 4) and a large one (6 * 6). A smaller board comes with an easier game since there are fewer possible places to lay the tokens.
- This gaming program also features two modes, a player-versus-player mode and a player-versus-ai mode. The user gets to choose the mode after clicking the start button on the intro page.
- For the AI mode, the game provides two levels of AIs. The easier AI places its token at a position where some opponent token will be flipped. The harder AI will prioritize its choice by placing the token at a position where the most number of opponent tokens can be flipped. 



II. HOW THE PROGRAM IS CONSTRUCTED
- Class organization: 
    To run this program, I created five classes, each one of them is stored in an individual module (the interface module contains both a text-based interface class and a graphic-based interface class).

- Key Algorithms:
    - Storing the board and the grid values: 
        The board of grids is stored as a list of dictionaries. Each of the dictionary contains information of girds in one row. 
        The index of the row dictionary in the list corresponds to the index of the row letter in the alphabet. For example, row A is stored as the first dictionary in the list, row B is stored as the second dictionary and so on.
        In each of the dictionaries, the keys are the positions of the grid and the values are initiated as "nothing". For instance, the grid "a0" would be stored as "'a0' : 'nothing'".
        Every time there is a token laid, the grid value changes correspondingly. For example, if a black token is laid on the grid a0, the grid value stored in a0 would be changed into "black".
    - Flipping the tokens: 
        To flip the tokens, the program automatically does two things at the same time: checking if there is flippable token and flipping the flippable tokens. The rule requires flipping of tokens on the same line. Since each token will be on four lines--the row line, the column line and the two diagonal lines--the checking and flipping has to be done four times. To check and flip the tokens, take the checking and flipping of tokens in the same row as an example, the program goes through the following steps:
            - create a list of grids in the same row as the new token. For example, if the new token is laid at position "a0", then the list will be "a0, a1, a2, a3" on a small 4 * 4 board.
            - find the grid values of all the grids in the previous list and store these values as a list.
            - starting from the position of the new token, first search to the left and see if there is any same color tokens to its left. create a list, named "target list", that store all the grid values from the new token to the first same color token to its left if there is a same color token; otherwise, set "target list" as an empty list.if "target list" is not empty, and there is no empty grids in the target list (since the rule says there can only be opponent tokens in between the new token and an existing token), flip all the opponent's tokens in the target list. 
            - after the first three steps are done, search to the right of the new token and do the same thing
        The method runs until all four lines have been checked and flipped.   
    - the AI:
        The AI places its token, aiming to flip some opponent tokens.
        The AI would first create a list of the positions of all the existing AI tokens on the board. Then it would check them one by one until it finds an AI token that allows it to flip some opponent tokens by placing a new AI token around that existing AI token. 
        To do that, the AI first takes the position of an existing AI token. It then searches in the same row, column and diagonal lines to see if there are any opponent tokens. If a black token is detected, it then checks whether it can place a token adjacent to the oppoent token to flip it. If it can and we are on the easy AI mode, the AI would stop searching and that position just found will be returned as the new AI token position. If we are on the hard AI mode, the AI would keep a dictionary of all the possible positions to place its token. The key of that dictionary will be the possible position and the value will be the number of opponent tokens it can flip by placing a token at that position. The AI will then compare all the positions and return the one where it can flip the largest number of opponent tokens.


CURRENT STATUS
- Working: 
    The program would not run into any error and would not shut down so far I have tested. The program has two levels of runnable AIs; it actually requires some practice to win against the hard AI on the large board. In fact, as far as I'm concerned, the larger the board is, the harder it gets to win against the AI. 
    
- Not Working: 
    Right now, only the AI is strictly following the rule of "placing a new token at a position where there are and there are only opponent's token in between the new token and an existing token on the board". The users are not forced to follow that rule. The program would not run into Error if the user breaks the rule though.
    
    I didn't get to modify the program so that the user can choose size in the graphics interface without having to type.
    
    There are some duplicated codes that could be further simplified but I have not figured out a way to do it.
    
- Further Extensions:
    A more intelligent AI than the current hard AI would be able to simulate the possible situation one more step ahead and determine where to put its token based on that.
 
 
INSTRUCTIONS

The user can run the game.py module from the command line.

After calling the module, the user will be asked to type whether they want to play the game on a small board or a large board. The user can choose to quit the game at this point by typing "quit". As soon as the user gives a size input ("small" or "large"), a game window will be created. Everything after that is graphic based, i.e. no more typing, just click the mouse.

Now the user should be at the intro page. I advise the user to read the rules before playing the game. You can find out the rules of the game by clicking the "RULE" button on the intro page of the game.

If the user prefer not to read the rules, s/he can go ahead and click on start. 

Clicking start will get the user into the mode page. The user has to choose whether s/he wants to play with an AI or another player. If player-versus-player mode is chosen, a board will be created and the users can start to play the game.

If player-versus-AI mode is chosen, the user will then get into a page where s/he can choose the difficulty level of the AI. As soon as one difficulty level is chosen, a playing board will be created and the user and start to play the game.

By clicking each grid, the user will be able to lay a new token in the grid. The game will automatically finish the flipping part. Then the AI or the opponent player will take his move and so on the user and opponent would take turns laying tokens on the board until the end of the game.

As soon as the game run into an ending situation (with no empty grid for example), the game window would display the result of game and calculate the score of the user based on how many tokens the user has on board at the end of the game. Click on "NEW GAME" button if you want to start a new game; you will only be able to play with the same size board as the previous one. Click on "QUIT" to quit the game and the window will be closed.