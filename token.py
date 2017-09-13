"""
Yitong Chen
CS 111 Spring 2016 Final Project
This module contains the token class for the reversi game.
"""

import graphics
import board


class Token:
    
    def __init__(self, position, color):
        """
        This is the initiator for the token class.
        
        Parameters:
        position (string) - the position of the token, represented in the 
                            format of "letter" + "number"; for example, "a1".
        color (string) - the color of the token. In this game, we assume that 
                         the user's token color is black and the AI's token 
                         color is white.
        """
        self.position = position
        self.pos_row = position[0]
        self.pos_col = position[1]
        self.color = color
        
        
    def get_color(self):
        """
        This method retrieves the color of the token.
        
        Return:
        the instance value of color of the given token object.
        """
        return self.color
    
    
    def get_position(self):
        """
        This method retrieves the position of the token.
        
        Return:
        the instance value of position of the given token object
        """
        return self.position
    
    
    def create_token(self, board):
        """
        This method creates a token by changing the value of the grid stored 
        in the board grid list into the color of the token and 
        draws a token on the board displayed to the user.
        """
        # retrieves the board list and set the grid value
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        row_index = alphabet.index(self.pos_row)
        my_board = board.get_board()
        my_board[row_index][self.position] = self.color
        
        # draws the token on the board
        token_pos_x = 100 * int(self.pos_col) + 50
        token_pos_y = board.side_length - 50 - 100 * row_index
        token = graphics.Circle(graphics.Point(token_pos_x, token_pos_y), 40)
        token.setFill(self.color)
        token.draw(board.win)