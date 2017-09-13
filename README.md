# Reversi Game

## Program Description
* This program runs the reversi game. Reversi is a game played between two opponent players, with two kinds of tokens, black and white for each player. Traditionally, the game is played on an 8*8 uncheckeded board. In this gaming program, the user can choose from two board sizes, as will be introduced later.
* To play the game, the user lays his/her token, following the rule that s/he can only place tokens where there are and there are only opponent tokens in between the new token and an existing token of the player's on the board. By placing his token, the user can then flip the opponent tokens surrounded by his tokens. The goal is to get as many of your tokens on the board as possible when the game ends. The game ends when the whole board is occupied or there are only tokens of one side on the board.
* This gaming program features two board sizes, a small one (4 * 4) and a large one (6 * 6). A smaller board comes with an easier game since there are fewer possible places to lay the tokens.
* This gaming program also features two modes, a player-versus-player mode and a player-versus-ai mode. The user gets to choose the mode after clicking the start button on the intro page.
* For the AI mode, the game provides two levels of AIs. The easier AI places its token at a position where some opponent token will be flipped. The harder AI will prioritize its choice by placing the token at a position where the most number of opponent tokens can be flipped. 

## Deployment

To start the program, direct to the directory and run:
```
$python3 game.py
```

## Game Design

### Class organization: 
To run this program, I created five classes, each one of them is stored in an individual module (the interface module contains both a text-based interface class and a graphic-based interface class).

### Key Algorithms:
* Storing the board and the grid values: 
        The board of grids is stored as a list of dictionaries. Each of the dictionary contains information of girds in one row. 
        The index of the row dictionary in the list corresponds to the index of the row letter in the alphabet. For example, row A is stored as the first dictionary in the list, row B is stored as the second dictionary and so on.
        In each of the dictionaries, the keys are the positions of the grid and the values are initiated as "nothing". For instance, the grid "a0" would be stored as "'a0' : 'nothing'".
        Every time there is a token laid, the grid value changes correspondingly. For example, if a black token is laid on the grid a0, the grid value stored in a0 would be changed into "black".
        
* Flipping the tokens: 
        To flip the tokens, the program automatically does two things at the same time: checking if there is flippable token and flipping the flippable tokens. The rule requires flipping of tokens on the same line. Since each token will be on four lines--the row line, the column line and the two diagonal lines--the checking and flipping has to be done four times. To check and flip the tokens, take the checking and flipping of tokens in the same row as an example, the program goes through the following steps:
   * Create a list of grids in the same row as the new token. For example, if the new token is laid at position "a0", then the list will be "a0, a1, a2, a3" on a small 4 * 4 board.
   * Find the grid values of all the grids in the previous list and store these values as a list.
   * Starting from the position of the new token, first search to the left and see if there is any same color tokens to its left. create a list, named "target list", that store all the grid values from the new token to the first same color token to its left if there is a same color token; otherwise, set "target list" as an empty list.if "target list" is not empty, and there is no empty grids in the target list (since the rule says there can only be opponent tokens in between the new token and an existing token), flip all the opponent's tokens in the target list. 
   * After the first three steps are done, search to the right of the new token and do the same thing
        The method runs until all four lines have been checked and flipped.   
* The AI:
        The AI places its token, aiming to flip some opponent tokens.
        The AI would first create a list of the positions of all the existing AI tokens on the board. Then it would check them one by one until it finds an AI token that allows it to flip some opponent tokens by placing a new AI token around that existing AI token. 
        To do that, the AI first takes the position of an existing AI token. It then searches in the same row, column and diagonal lines to see if there are any opponent tokens. If a black token is detected, it then checks whether it can place a token adjacent to the oppoent token to flip it. If it can and we are on the easy AI mode, the AI would stop searching and that position just found will be returned as the new AI token position. If we are on the hard AI mode, the AI would keep a dictionary of all the possible positions to place its token. The key of that dictionary will be the possible position and the value will be the number of opponent tokens it can flip by placing a token at that position. The AI will then compare all the positions and return the one where it can flip the largest number of opponent tokens.

## Author

* **Yitong Chen** - [yitongc19](https://github.com/yitongc19)
