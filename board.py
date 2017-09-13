"""
Yitong Chen
CS 111 Spring 2016 Final Project
This module contains the board class
"""
import graphics

class Board:
    
    def __init__(self, side_length, win):
        """
        This is the init function for the board class.
        
        Parameters:
        side_length (integer) - side_length of the board
        """
        self.side_length = side_length
        self.side_grid = side_length // 100
        self.win = win
        self.board = self.board_grid()
        self.draw_board()
        
        
    def board_grid(self):
        """
        This method creates a list of dictionaries to represent the grids on the board.
        Each of the dictionaries represent a row of grids.
        The key in the dictionary is the coordinate of the grid in the form of "letter+number"
        (e.g. "a0").
        The default value of the entries are "nothing"
        """
        
        grid_list = []
    
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        alpha = alphabet[:self.side_grid]
        
        for letter in alpha:
            row_dic = {}
            row = letter
            for col in range(self.side_grid):
                row_dic[row + str(col)] = "nothing"
            grid_list.append(row_dic)
    
            
        return grid_list
        
        
    def get_sideLength(self):
        """
        This method retrieves the side_length of the board.
        """
        return self.side_length
    
    
    def get_sideGrid(self):
        """
        This method retrieves the number of grids on the side.
        """
        return self.side_grid
    
   
    def get_board(self):
        """
        This method retrieves the board (a dictionary object) for the user.
        """
        return self.board
    
    
    def retrieve_grid(self, pos):
        """
        This method retrieves the value of a grid.
        """
        pos_row = pos[0]
    
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        row_index = alphabet.index(pos_row)
        
        return self.board[row_index][pos]
        
        
    def draw_board(self):
        """
        This method draws the board and the grids on the board.
        """
        board_rec = graphics.Rectangle(graphics.Point(0, 0),
                                      graphics.Point(self.side_length, self.side_length))
        
        background = graphics.Image(graphics.Point(self.side_length // 2, self.side_length // 2),
                                "background.gif")
        
        background.draw(self.win)
        
        board_rec.draw(self.win)
        
        for i in range(100, self.side_length + 100, 100):
            hline = graphics.Line(graphics.Point(0, i), graphics.Point(self.side_length, i))
            hline.draw(self.win)
            vline = graphics.Line(graphics.Point(i, 0), graphics.Point(i, self.side_length))
            vline.draw(self.win)      