"""
Yitong Chen
CS 111 Spring 2016
This module includes two interface classes, a text based one and a graphic based one.
"""
import board
import graphics
import token
import random
import button
import game
import time

class TextBasedInterface:
    """ This is the class of the text-based interface class"""
    
    def __init__(self, side_length):
        """
        This is the constructor method of the textBasedInterface class.
        
        Parameter:
        side_length (integer) - this determines the size of the board.
        """
        self.side_length = side_length
        self.win = graphics.GraphWin("Reversi Game", side_length, side_length)
        self.win.setCoords(0, 0 , side_length, side_length)
        self.board = board.Board(side_length, self.win)
        
    
    def get_pos(self):
        """
        This method asks the user for a position where he 
        wants to place his token
        
        Return:
        a position in the form of "letter" + "number"
        """
        token_pos = input("Where do you want to place your token? ")
        return token_pos
    
    
    def check_pos(self, pos):
        """
        This method checks whether the position is within the range of the 
        current board.
        
        returns:
        True if the position is valid
        False if the position is not valid
        """
        my_board = self.board.get_board()
        
        # initialize a list of boolean values
        tf_list = []
        
        for dic in my_board:
            for key in dic:
                tf_list.append(key == pos)
                
        return (True in tf_list)
    
    
    def ai_play(self):
        """
        This method is the ai method, returns a random empty position on the board
        """
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        alp = alphabet[:self.side_length // 100]
        
        row_index = random.randrange(0, self.side_length // 100, 1)
        col = random.randrange(0, self.side_length // 100, 1)
        row = alp[row_index]
        ai_pos = row + str(col)
        grid_value = self.board.get_board()[row_index][ai_pos]
        
        while grid_value != "nothing":
            row_index = random.randrange(0, self.side_length // 100, 1)
            col = random.randrange(0, self.side_length // 100, 1)
            row = alp[row_index]
            ai_pos = row + str(col)
            grid_value = self.board.get_board()[row_index][ai_pos]
        
        #print(ai_pos)
        return ai_pos    
        
    
    def flip(self, pos, color):
        """
        This is the method that flips all the tokens.
        
        Parameter:
        pos (string) - the position of the new token
        color (string) - the color of the new token
        """
        my_board = self.board.get_board()
        pos_row = pos[0]
        pos_col = int(pos[1])
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        alp = alphabet[:self.side_length // 100]
        row_index = alp.index(pos_row)        
        
        # flip the flippable tokens in the same row, column and on the same diagonal lines
        self.flip_row(my_board, row_index, pos_row, pos_col, color)
        self.flip_col(my_board, row_index, pos_row, pos_col, color, alp)
        
        self.flip_dia1(my_board, row_index, pos_row, pos_col, color, alp, pos)
        self.flip_dia2(my_board, row_index, pos_row, pos_col, color, alp, pos)
        
        
    def flip_dia2(self, my_board, row_index, pos_row, pos_col, color, alp, pos):
        """
        This method flips the tokens on the top_left to bot_right diagonal line.
        Start from creating a list of the grid value of all the grids on the same 
        diagonal line.
        
        Parameters:
        my_board (list) - the list of dictionaries where the grid values are stored
        row_index (number) - the index number of the row
        pos_row (string) - the row letter of the new token
        pos_col (number) - the column number of the new token
        color (string) - the color of the new token
        alp (string) - the string of all the row letters
        pos (string) - the position of the new token
        """
        
        diagonal_difference = abs(pos_col - row_index)
        key_list = []
        
        if row_index <= pos_col:
            #print(diagonal_difference)
            
            for col in range(self.side_length // 100 - 1, diagonal_difference - 1, -1):
                key = alp[col - diagonal_difference] + str(col)
                key_list.append(key)
            key_list.reverse()
        else:
            for col in range(0, self.side_length // 100 - diagonal_difference, 1):
                key = alp[col + diagonal_difference] + str(col)
                key_list.append(key)
        
        dia_list = []
        index = 0
        row = 0
        
        while row < len(alp) and index < len(key_list):
            row_dic = my_board[row]
            cur_key = key_list[index]
            if cur_key in row_dic:
                index += 1
                dia_list.append(row_dic[cur_key])
            row += 1
                 
        self.comparison_dia(alp, dia_list, row_index, pos_col, pos_row, color, key_list, pos)
        
        
    def flip_dia1(self, my_board, row_index, pos_row, pos_col, color, alp, pos):
        """This method flips the tokens on the bot_left to top_right diagonal line
        For the details of how the algorithm works, see the comment on method "flip_dia2".
        
        Parameters:
        my_board (list) - the list of dictionaries where the grid values are stored
        row_index (number) - the index number of the row
        pos_row (string) - the row letter of the new token
        pos_col (number) - the column number of the new token
        color (string) - the color of the new token
        alp (string) - the string of all the row letters
        pos (string) - the position of the new token
        """
        diagonal_sum = row_index + pos_col
        key_list = []    
        
        if diagonal_sum < len(alp):
            for i in range(0, diagonal_sum + 1):
                key = alp[i] + str(diagonal_sum - i)
                key_list.append(key)
        else:
            for i in range(diagonal_sum - (len(alp) - 1),len(alp)):
                key = alp[i] + str(diagonal_sum - i)
                key_list.append(key)
        
        # creates a list of value of the grids on the bot-left to up-right diagonal
        dia_list = []
        row = 0
        index = 0
        while row < len(alp) and index < len(key_list):
            row_dic = my_board[row]
            if key_list[index] in row_dic:
                dia_list.append(row_dic[key_list[index]])
                index += 1
            row += 1
            
        # print(dia_list)
        
        self.comparison_dia(alp, dia_list, row_index, pos_col, pos_row, color, key_list, pos)
        
        
    def flip_col(self, my_board, row_index, pos_row, pos_col, color, alp):
        """
        This method flips the token in the same column.
        
        Parameters:
        my_board (dictionary) - the dictionary of the board object
        row_index (integer) - the corresponding index of the row letter
        pos_row (string) - the row letter
        pos_col (integer) - the index of the column number
        color (string) - color of the new token
        alp (string) - the string of all the row letters
        """
        
        # create a list of the target grids(grids in the same column)
        key_list = []
        for ch in alp:
            key = ch + str(pos_col)
            key_list.append(key)
        
        # creates a list of the value of the grids in the same column
        col_list = []
        row = 0
        while row < len(alp):
            row_dic = my_board[row]
            col_list.append(row_dic[key_list[row]])
            row += 1       
        
        self.comparison_col(alp, col_list, row_index, pos_col, pos_row, color)
        
        
    def flip_row(self, my_board, row_index, pos_row, pos_col, color):
        """
        This method flips all the tokens in the same row according to the rule.
        
        Parameters:
        my_board (dictionary) - the dictionary of the board object
        row_index (integer) - the corresponding index of the row letter
        pos_row (string) - the row letter
        pos_col (integer) - the index of the column number
        color (string) - color of the new token
        """
        # check row, we could probably make this a function
        row_dic = my_board[row_index]
        # construct a key
        cur_col = 0 
        row_list = []
        
        # creates an ordered list of values of grids in this row
        while cur_col < len(row_dic):
            key = pos_row + str(cur_col)
            row_list.append(row_dic[key])
            cur_col += 1
        
        self.comparison_row(row_list, row_index, pos_col, pos_row, color)
                
        
    def comparison_col(self, alp, col_list, row_index, pos_col, pos_row, color):
        """
        This method checks whether there is an appropriate sub_list 
        in the same column and if there is, this method flips all the appropriate tokens 
        in that sublist.
        
        Parameters:
        row_index (integer) - the corresponding index of the row letter
        pos_row (string) - the row letter
        pos_col (integer) - the index of the column number
        color (string) - color of the new token
        alp (string) - the string of all the row letters
        col_list (list) - the list of grid values of grids in the same column
        """
        # checks upward
        if row_index - 1 >= 0:
            cur_row = row_index - 1
        else:
            cur_row = row_index
            
        while cur_row > 0 and col_list[cur_row] != color:
            cur_row -= 1
            
        if col_list[cur_row] == color:
            target_list = col_list[cur_row + 1: row_index]
        else:
            target_list = []
            
        if target_list != [] and "nothing" not in target_list:
            for row in range(cur_row + 1, row_index):
                key = alp[row] + str(pos_col)
                self.board.get_board()[row][key] = color
                
        # checks downward
        if row_index + 1 < len(col_list):
            cur_row = row_index + 1
        else:
            cur_row = row_index
        
        while cur_row < len(col_list) - 1 and col_list[cur_row] != color:
            cur_row += 1
        
        if col_list[cur_row] == color:
            target_list = col_list[row_index + 1: cur_row]
        else:
            target_list = []
            
        if target_list != [] and "nothing" not in target_list:
            for row in range(row_index + 1, cur_row):
                key = alp[row] + str(pos_col)
                self.board.get_board()[row][key] = color               
                
                
    def comparison_dia(self, alp, dia_list, row_index, pos_col, pos_row, color, key_list, pos):
        """
        This method checks whether there is an appropriate sub_list 
        in the same diagonal line and if there is, this method flips all the appropriate tokens 
        in that sublist.
        
        Parameters:
        row_index (integer) - the corresponding index of the row letter
        pos_row (string) - the row letter
        pos_col (integer) - the index of the column number
        color (string) - color of the new token
        alp (string) - the string of all the row letters
        dia_list (list) - a list of grid values of grids on the same diagonal line
        key_list (lsit) - a list of the coordinates of grids on the same diagonal line
        pos (string) - the position of the current token
        """
        pos_in_list = key_list.index(pos)
        
        if pos_in_list - 1 >= 0:
            cur_pos_in_list = pos_in_list - 1
        else:
            cur_pos_in_list = pos_in_list
            
        while cur_pos_in_list > 0 and dia_list[cur_pos_in_list] != color:
            cur_pos_in_list -= 1
        
        if dia_list[cur_pos_in_list] == color:
            target_list = dia_list[cur_pos_in_list + 1: pos_in_list]
        else:
            target_list = []
            
        if target_list != [] and "nothing" not in target_list:
            for pos in range(cur_pos_in_list + 1, pos_in_list):
                key = key_list[pos]
                row = alp.index(key[0])
                self.board.get_board()[row][key] = color
                
        if pos_in_list + 1 < len(dia_list):
            cur_pos_in_list = pos_in_list + 1
        else:
            cur_pos_in_list = pos_in_list
            
        while cur_pos_in_list < len(dia_list) and dia_list[cur_pos_in_list] != color:
            cur_pos_in_list += 1
            
        if dia_list[cur_pos_in_list] == color:
            
            target_list = dia_list[pos_in_list + 1: cur_pos_in_list]
        else:
            target_list = []
            
        if target_list != [] and "nothing" not in target_list:
            for pos in range(pos_in_list + 1, cur_pos_in_list):
                key = key_list[pos]
                row = alp.index(key[0])
                self.board.get_board()[row][key] = color
                
        
    def comparison_row(self, row_list, row_index, pos_col, pos_row, color):
        """
        This method checks whether there is an appropriate sub_list 
        in the same row and if there is, this method flips all the appropriate tokens 
        in that sublist.
        
        Parameters:
        row_index (integer) - the corresponding index of the row letter
        pos_row (string) - the row letter
        pos_col (integer) - the index of the column number
        color (string) - color of the new token
        alp (string) - the string of all the row letters
        row_list (list) - the list of grid values of grids in the same row
        """
        # look to the left of the new token and see if we can flip some tokens
        if pos_col - 1 >= 0:
            cur_col = pos_col - 1
        else:
            cur_col = pos_col
            
        while cur_col > 0 and row_list[cur_col] != color:
            cur_col -= 1
            
        # check whether while loop stops because it reaches the end or hits a same-color token
        # takes the range between two same_color tokens and make it a list
        if row_list[cur_col] == color:
            target_list = row_list[cur_col + 1: pos_col]
        else:
            target_list = []
        
        # check if there is empty grid in the list
        if target_list != [] and "nothing" not in target_list:
            for col in range(cur_col + 1, pos_col):
                key = pos_row + str(col)
                self.board.get_board()[row_index][key] = color
        
            
        # look to the right of the new token and see if we can flip some tokens
        if pos_col + 1 < len(row_list):
            cur_col = pos_col + 1
        else:
            cur_col = pos_col
        
        while cur_col < len(row_list) - 1 and row_list[cur_col] != color:
            cur_col += 1
        
        # check whether while loop stops because it reaches the end or hits a same-color token
        # takes the range between two same_color tokens and make it a list
        if row_list[cur_col] == color:
            target_list = row_list[pos_col + 1: cur_col]
        else:
            target_list = []
        
        # check if there is empty grid in the list
        if target_list != [] and "nothing" not in target_list:
            for col in range(pos_col + 1, cur_col):
                key = pos_row + str(col)
                self.board.get_board()[row_index][key] = color     
        
        
    def show_result(self):
        """
        This method calculates and shows the result to the user
        """
        my_board = self.board.get_board()
        
        num_user = 0
        num_ai = 0
        
        for dic in my_board:
            for key in dic:
                value = dic[key]
                if value == "black":
                    num_user += 1
                else:
                    num_ai += 1
                    
        score = 100 * num_user // (num_user + num_ai)
                    
        print("The board is fully occupied!")
        print("You have %d tokens on the board. \nYour opponent has %d tokens on the board."
             % (num_user, num_ai))
        
        if num_user > num_ai:
            print("Congratulations! You win!!")
        elif num_user == num_ai:
            print("It's a draw!")
        else:
            print("I'm sorry you lose :(")
            
        print("Your score is %d" %(score))
    
    
    def close(self):
        """
        This method closes the interface
        """
        print("Goodbye")

    
class GraphicBasedInterface:
    
    def __init__(self, win_side_length):
        """This is the constructor method for the graphic-based interface. It initializes a 
        number of instance variables and calls the intro_page and mode_page method
        to display these two pages on the user's request (mouse click)
        
        Parameters:
        win_side_length (integer) - the side length of the window
        """
        self.win = graphics.GraphWin("Reversi Game", win_side_length, win_side_length)
        self.win.setCoords(0, 0, win_side_length, win_side_length)
        self.win_side_length = win_side_length
        self.side_length = win_side_length
        self.mode = None
        
        self.intro_page()
        
        pclick = self.win.getMouse()
        x_pclick = pclick.getX()
        y_pclick = pclick.getY()
        
        if (self.win_side_length // 2 - 50 <= x_pclick <= self.win_side_length // 2 + 50
            and self.win_side_length // 3 - 70 <= y_pclick <= self.win_side_length // 3 - 30):
            self.show_rule()
        
        pclick = self.win.getMouse()
        x_pclick = pclick.getX()
        y_pclick = pclick.getY()
        
        while (self.win_side_length // 2 - 50 > x_pclick
               or x_pclick > self.win_side_length // 2 + 50
               or self.win_side_length // 3 - 20 > y_pclick 
               or y_pclick > self.win_side_length // 3 + 20):
            pclick = self.win.getMouse()
            x_pclick = pclick.getX()
            y_pclick = pclick.getY()
            
        self.mode_page()
        
        self.level = None
        
        if self.mode == "ai":
            self.level_page()
            
        self.board = board.Board(self.win_side_length, self.win)
        
    
    def level_page(self):
        """
        This method creates a page that allows the user to choose an AI opponent 
        of different levels of intelligence.
        """
        level_back = graphics.Image(graphics.Point(self.win_side_length // 2, 
                                                   self.win_side_length // 2),
                                "intro_background.gif")
        level_back.draw(self.win)
        
        text = graphics.Text(graphics.Point(self.win_side_length / 2,
                                            self.win_side_length / 2 + 100 ),
                            "Please choose a difficulty level: ")
        text.setSize(26)
        text.setFill("orange")
        text.draw(self.win)
        
        pvp_but = button.Button(80, 30, graphics.Point(self.win_side_length / 2,
                                                       self.win_side_length / 2),
                               "HARD", self.win, 22, "Orange")
        pva_but = button.Button(80, 30, graphics.Point(self.win_side_length / 2,
                                                       self.win_side_length / 2 - 80),
                               "EASY", self.win, 22, "Orange")
        
        pclick = self.win.getMouse()
        xclick = pclick.getX()
        yclick = pclick.getY()
        
        while (xclick < self.win_side_length / 2 - 40 or
              xclick > self.win_side_length / 2 + 40 or
              yclick < self.win_side_length / 2 - 15 or 
              yclick > self.win_side_length / 2 + 15):
            
            if (self.win_side_length / 2 - 40 <= xclick <= self.win_side_length / 2 + 40
                and self.win_side_length / 2 - 95 <= yclick <= self.win_side_length / 2 - 65):
                self.level = "easy"
                return
            
            else:
                pclick = self.win.getMouse()
                xclick = pclick.getX()
                yclick = pclick.getY()
            
        self.level = "hard"

        return
        
    
    def mode_page(self):
        """
        This method displays a page where the user can choose whether 
        they want a player versus player mode or a player versus ai mode.
        
        The instance variable "mode" is set to a value based on the user's mouse click
        """
        mode_back = graphics.Image(graphics.Point(self.win_side_length // 2, 
                                                   self.win_side_length // 2),
                                "intro_background.gif")
        mode_back.draw(self.win)
        
        text = graphics.Text(graphics.Point(self.win_side_length / 2,
                                            self.win_side_length / 2 + 100 ),
                            "Please choose a mode: ")
        text.setSize(26)
        text.setFill("orange")
        text.draw(self.win)
        
        pvp_but = button.Button(180, 30, graphics.Point(self.win_side_length / 2,
                                                       self.win_side_length / 2),
                               "Player VS Player", self.win, 22, "Orange")
        pva_but = button.Button(180, 30, graphics.Point(self.win_side_length / 2,
                                                       self.win_side_length / 2 - 80),
                               "Player VS AI", self.win, 22, "Orange")
        
        pclick = self.win.getMouse()
        xclick = pclick.getX()
        yclick = pclick.getY()
        
        while (xclick < self.win_side_length / 2 - 90 or
              xclick > self.win_side_length / 2 + 90 or
              yclick < self.win_side_length / 2 - 15 or 
              yclick > self.win_side_length / 2 + 15):
            
            if (self.win_side_length / 2 - 90 <= xclick <= self.win_side_length / 2 + 90
                and self.win_side_length / 2 - 95 <= yclick <= self.win_side_length / 2 - 65):
                self.mode = "ai"
                return
            
            else:
                pclick = self.win.getMouse()
                xclick = pclick.getX()
                yclick = pclick.getY()
            
        self.mode = "pp"

        return
        
        
    def intro_page(self):
        """
        This image is the introduction page, waits for the user to choose a 
        board size and a difficulty level and start the game
        
        returns the side_length based on how large the user wants the board
        to be. 
        """
        intro_back = graphics.Image(graphics.Point(self.win_side_length // 2, 
                                                   self.win_side_length // 2),
                                "intro_background.gif")
        intro = graphics.Image(graphics.Point(self.win_side_length // 2, 
                                              self.win_side_length // 2 + 100),
                                "reversi.gif")
        
        intro_back.draw(self.win)
        intro.draw(self.win)
        
        start_button = button.Button(100, 40, graphics.Point(self.win_side_length // 2, 
                                                           self.win_side_length // 3),
                                    "START", self.win, 26, "Orange")
        rule_button = button.Button(100, 40, graphics.Point(self.win_side_length // 2, 
                                                           self.win_side_length // 3 - 50),
                                    "RULE", self.win, 26, "Orange")
        
        
    def show_rule(self):
        """
        This method shows the rule of the reversi game on the user's request (mouse click)
        """
        text = (" YOU ARE BLACK!!!" + 
                "\n The game begins with four tokens placed in a square" +
                "\n in the middle of the grid, two facing white side up," +
                "\n two pieces with the black side up, with same-colored" +
                "\n tokens on a diagonal with each other." +
                "\n In the game, the user can only place token where there" +
                "\n is one or more opponent tokens in between the new token" +
                "\n and an existing user's token. By placing the new token," +
                "\n the user can flip all the opponent’s tokens in between into user’s token." +
                "\n The user can choose to play with an AI or another player." +
                "\n When playing with an AI, if the AI has no place to put a token, " +
                "\n the user can make one more move. The game ends when the board " +
                "\n is fully occupied with tokens or only one side has tokens on the board." +
                "\n In order to win the game,the user need to arrange his tokens" +
                "\n in such a way that he ends up with more tokens on the board" +
                "\n than the opponent.")
        
        rule = graphics.Text(graphics.Point(self.win_side_length // 2, self.win_side_length // 2),
                             text)
        
        if self.win_side_length == 600:
            rule.setSize(17)
        else:
            rule.setSize(12)
            
        rule_box = graphics.Rectangle(graphics.Point(5, self.win_side_length * 3 / 4 + 17),
                                     graphics.Point(self.win_side_length, self.win_side_length / 4 - 50))
        rule_box.setFill("Orange")
        rule_box.draw(self.win)
        
        rule.draw(self.win)
        
        close_but = button.Button(70, 20, graphics.Point(self.win_side_length // 2,
                                                        self.win_side_length / 4 - 25),
                                 "Close", self.win, 21, "Black")
        
        pclick = self.win.getMouse()
        x_pclick = pclick.getX()
        y_pclick = pclick.getY()
        
        while (self.win_side_length // 2 - 35 > x_pclick
               or x_pclick > self.win_side_length // 2 + 35
               or self.win_side_length / 4 - 35 > y_pclick 
               or y_pclick > self.win_side_length / 4 - 15 ):
            pclick = self.win.getMouse()
            x_pclick = pclick.getX()
            y_pclick = pclick.getY()
        
        rule.undraw()
        rule_box.undraw()
        close_but.button.undraw()
        close_but.text.undraw()
                        
        
    def get_pos(self):
        """
        This method gets the position of the user's click and determines 
        which grid the user clicks based on that.
        
        return:
        name of that grid
        """
        pclick = self.win.getMouse()
        xclick = pclick.getX()
        yclick = pclick.getY()
        
        for x in range(100, self.side_length + 100, 100):
            for y in range(100, self.side_length + 100, 100):
                if x - 100 < xclick < x and y - 100 < yclick < y:
                    token_pos_tup = (x // 100 - 1, y // 100)
                else: 
                    pass
                    
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        token_pos_row = alphabet[self.side_length // 100 - token_pos_tup[1]]
        token_pos_col = token_pos_tup[0]
        
        token_pos = token_pos_row + str(token_pos_col)
             
        return token_pos    
    
    
    def check_pos(self, pos):
        """
        This method checks whether the position is within the range of the 
        current board.
        """
        my_board = self.board.get_board()
        # a list of boolean values
        tf_list = []
        
        for dic in my_board:
            for key in dic:
                tf_list.append(key == pos)
                
        return (True in tf_list)
        
    
    def ai_play(self, color, level):
        """
        This method allows the ai to choose a position to lay its token; 
        the ai would lay a token at 
        a random position where some user tokens will be flipped.
        
        Parameter:
        color (string) - the color of the ai token
        
        returns:
        if a position meeting the criteria exists, the program returns a position 
        if none of the empty positions on board meets the criteria, the program returns
        ai_pos = "not exist"
        """
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        alp = alphabet[:self.side_length // 100]
        
        my_board = self.board.get_board()
        
        white_pos_list = []
        
        for dic in my_board:
            for key in dic:
                if dic[key] == color:
                    white_pos_list.append(key)
                    
        white_index = 0
        
        old_token_pos = white_pos_list[white_index]
        old_token_col = int(old_token_pos[1])
        old_token_row = old_token_pos[0]
        old_token_row_index = alp.index(old_token_row)
        
        black_exist = False
        
        if level == "easy":
            ai_pos, black_exist = self.check_flippable_easy(alp, my_board, old_token_pos, 
                                                        old_token_col, old_token_row, 
                                                        old_token_row_index, black_exist)
        elif level == "hard":
            ai_pos, black_exist = self.check_flippable_hard(alp, my_board, old_token_pos, 
                                                        old_token_col, old_token_row, 
                                                        old_token_row_index, black_exist)
        
        while black_exist == False and white_index + 1 < len(white_pos_list):
            white_index += 1
            old_token_pos = white_pos_list[white_index]
            old_token_col = int(old_token_pos[1])
            old_token_row = old_token_pos[0]
            old_token_row_index = alp.index(old_token_row)
        
            if level == "easy":
                ai_pos, black_exist = self.check_flippable_easy(alp, my_board, old_token_pos, 
                                                       old_token_col, old_token_row, 
                                                       old_token_row_index, black_exist)
            elif level == "hard":
                ai_pos, black_exist = self.check_flippable_hard(alp, my_board, old_token_pos, 
                                                        old_token_col, old_token_row, 
                                                        old_token_row_index, black_exist)
        return ai_pos
        
        
    def check_flippable_hard(self, alp, my_board, old_token_pos, old_token_col, old_token_row, 
                       old_token_row_index, black_exist):
        """This method is a helper method for the AI to play the game.
        The method checks whether there are tokens flippable in the same row, column or on 
        the same diagonal line. If there is, the ai would take down the number of black tokens it 
        can flip at that position. The ai then would place a token at the position where it can
        flip the most user's tokens.
        
        Returns:
        ai_pos (string) - a position if some flippable opponent tokens exist
                          "not exist" otherwise
        """ 
        pos_dic = {}
                # check if there is any adjacent black token in the same row
        row_dic = my_board[alp.index(old_token_row)]
        
        # check to the left of the old white token, if there is black token flippable,
        # return the position as the new ai token position
        if old_token_col - 1 < 0:
            cur_token_col = old_token_col
        else:
            cur_token_col = old_token_col - 1
            
        key = old_token_row + str(cur_token_col)
        cur_token_value = row_dic[key]
        
        while cur_token_value == "balck" and cur_token_col - 1 >= 0:
            cur_token_col -= 1
            key = old_token_row + str(cur_token_col)
            cur_token_value = row_dic[key] 
            
        num_left = old_token_col - cur_token_col
            
        if num_left >= 2 and cur_token_value == "nothing":
            black_exist = True
            pos_dic[key] = num_left
            
        # if there is no black token flippable to the left, check to the right
        if old_token_col + 1 >= len(row_dic):
            cur_token_col = old_token_col
        else:
            cur_token_col = old_token_col + 1
                
        key = old_token_row + str(cur_token_col)
        cur_token_value = row_dic[key]

        while cur_token_value == "black" and cur_token_col + 1 < len(row_dic):
            cur_token_col += 1
            key = old_token_row + str(cur_token_col)
            cur_token_value = row_dic[key] 
            
        num_right = old_token_col - cur_token_col

        if num_right >= 2 and cur_token_value == "nothing":
            black_exist = True
            pos_dic[key] = num_right
        
        # check if there is any adjacent token in the same column if there is 
        # no black tokens flippable in the same column
            # check upward
        if old_token_row_index - 1 < 0:
            cur_token_row_index = old_token_row_index
        else:
            cur_token_row_index = old_token_row_index - 1

        key = alp[cur_token_row_index] + str(old_token_col)
        row_dic = my_board[cur_token_row_index]
        cur_token_value = row_dic[key]

        while cur_token_value == "black" and cur_token_row_index - 1 >= 0:
            cur_token_row_index -= 1
            key = alp[cur_token_row_index] + str(old_token_col)
            row_dic = my_board[cur_token_row_index]
            cur_token_value = row_dic[key]
        
        num_up = old_token_row_index - cur_token_row_index
        
        if old_token_row_index - cur_token_row_index >= 2 and cur_token_value == "nothing":
            black_exist = True
            pos_dic[key] = num_up
            
            # check downward
        if old_token_row_index + 1 >= len(alp):
            cur_token_row_index = old_token_row_index
        else:
            cur_token_row_index = old_token_row_index + 1
                
        key = alp[cur_token_row_index] + str(old_token_col)
        row_dic = my_board[cur_token_row_index]
        cur_token_value = row_dic[key]
            
        while cur_token_value == "black" and cur_token_row_index + 1 < self.side_length // 100:
            cur_token_row_index += 1
            key = alp[cur_token_row_index] + str(old_token_col)
            row_dic = my_board[cur_token_row_index]
            cur_token_value = row_dic[key]
            
        if cur_token_row_index - old_token_row_index >= 2 and cur_token_value == "nothing":
            black_exist = True
            pos_dic[key] = cur_token_row_index - old_token_row_index        
        
        # if there is no black token flippable in the same row and the 
        # the same column, check the two diagonals
        # check the top-left to bot-right diagonal
        # check to the top_left
        if old_token_row_index - 1 >= 0 and old_token_col - 1 >= 0:
            cur_token_row_index = old_token_row_index - 1
            cur_token_col = old_token_col - 1
            key = alp[cur_token_row_index] + str(cur_token_col)
            row_dic = my_board[cur_token_row_index]
            cur_token_value = row_dic[key]
                
            while (cur_token_value == "black" and 
                    cur_token_row_index - 1 >= 0 and cur_token_col - 1 >= 0):
                cur_token_row_index -= 1
                cur_token_col -= 1
                key = alp[cur_token_row_index] + str(cur_token_col)
                row_dic = my_board[cur_token_row_index]
                cur_token_value = row_dic[key]
                    
            if old_token_col - cur_token_col >= 2 and cur_token_value == "nothing":
                black_exist = True
                pos_dic[key] = old_token_col - cur_token_col
                    
            # check to the bot_right

            if (old_token_row_index + 1 < self.side_length// 100
                and old_token_col + 1 < self.side_length// 100):
                cur_token_row_index = old_token_row_index + 1
                cur_token_col = old_token_col + 1
                key = alp[cur_token_row_index] + str(cur_token_col)
                row_dic = my_board[cur_token_row_index]
                cur_token_value = row_dic[key]
                
            while (cur_token_value == "black" and 
                    cur_token_row_index + 1 < self.side_length// 100
                    and cur_token_col + 1 < self.side_length// 100):
                cur_token_row_index += 1
                cur_token_col += 1
                key = alp[cur_token_row_index] + str(cur_token_col)
                row_dic = my_board[cur_token_row_index]
                cur_token_value = row_dic[key]
                    
            if cur_token_col - old_token_col >= 2 and cur_token_value == "nothing":
                black_exist = True
                pos_dic[key] = cur_token_col - old_token_col
        
        # check the top_right to bot_left diagonal if there isn't 
        # flippable token in the previous three conditions
        # check to the top_right
        if old_token_row_index - 1 >= 0 and old_token_col + 1 < self.side_length// 100:
            cur_token_row_index = old_token_row_index - 1
            cur_token_col = old_token_col + 1
            key = alp[cur_token_row_index] + str(cur_token_col)
            row_dic = my_board[cur_token_row_index]
            cur_token_value = row_dic[key]
                
            while (cur_token_value == "black" and 
                   cur_token_row_index - 1 >= 0 and 
                   cur_token_col + 1 < self.side_length// 100):
                cur_token_row_index -= 1
                cur_token_col += 1
                key = alp[cur_token_row_index] + str(cur_token_col)
                row_dic = my_board[cur_token_row_index]
                cur_token_value = row_dic[key]
                    
            if cur_token_col - old_token_col >= 2 and cur_token_value == "nothing":
                black_exist = True
                pos_dic[key] = cur_token_col - old_token_col
                    
            # check to the bot_left
            if (old_token_row_index + 1 < self.side_length// 100
                and old_token_col - 1 >= 0):
                cur_token_row_index = old_token_row_index + 1
                cur_token_col = old_token_col - 1
                key = alp[cur_token_row_index] + str(cur_token_col)
                row_dic = my_board[cur_token_row_index]
                cur_token_value = row_dic[key]
                
            while (cur_token_value == "black" and 
                   cur_token_row_index + 1 < self.side_length// 100 and cur_token_col - 1 >= 0):
                cur_token_row_index += 1
                cur_token_col -= 1
                key = alp[cur_token_row_index] + str(cur_token_col)
                row_dic = my_board[cur_token_row_index]
                cur_token_value = row_dic[key]
                    
            if old_token_col - cur_token_col >= 2 and cur_token_value == "nothing":
                black_exist = True
                pos_dic[key] = old_token_col - cur_token_col
                
        for key in pos_dic:
            large = pos_dic[key]
            if pos_dic[key] >= large:
                ai_pos = key
                    
        if black_exist == False:
            ai_pos = "not exist"
        
        return ai_pos, black_exist
        
        
        
        
        
    def check_flippable_easy(self, alp, my_board, old_token_pos, old_token_col, old_token_row, 
                       old_token_row_index, black_exist):
        """This method is a helper method for the AI to play the game.
        The method checks whether there are tokens flippable in the same row, column or on 
        the same diagonal line. If there is, the ai would place its token at that 
        corresponding position where it can flip some tokens.
        
        Returns:
        ai_pos (string) - a position if some flippable opponent tokens exist
                          "not exist" otherwise
                          """
        
        # check if there is any adjacent black token in the same row
        row_dic = my_board[alp.index(old_token_row)]
        
        # check to the left of the old white token, if there is black token flippable,
        # return the position as the new ai token position
        if old_token_col - 1 < 0:
            cur_token_col = old_token_col
        else:
            cur_token_col = old_token_col - 1
            
        key = old_token_row + str(cur_token_col)
        cur_token_value = row_dic[key]
        
        while cur_token_value == "balck" and cur_token_col - 1 >= 0:
            cur_token_col -= 1
            key = old_token_row + str(cur_token_col)
            cur_token_value = row_dic[key] 
            
        if old_token_col - cur_token_col >= 2 and cur_token_value == "nothing":
            black_exist = True
            ai_pos = key
            
        # if there is no black token flippable to the left, check to the right
        if black_exist == False: 
            
            if old_token_col + 1 >= len(row_dic):
                cur_token_col = old_token_col
            else:
                cur_token_col = old_token_col + 1
                
            key = old_token_row + str(cur_token_col)
            cur_token_value = row_dic[key]

            while cur_token_value == "black" and cur_token_col + 1 < len(row_dic):
                cur_token_col += 1
                key = old_token_row + str(cur_token_col)
                cur_token_value = row_dic[key] 

            if cur_token_col - old_token_col >= 2 and cur_token_value == "nothing":
                black_exist = True
                ai_pos = key
        
        # check if there is any adjacent token in the same column if there is 
        # no black tokens flippable in the same column
        if black_exist == False:
            # check upward
            if old_token_row_index - 1 < 0:
                cur_token_row_index = old_token_row_index
            else:
                cur_token_row_index = old_token_row_index - 1

            key = alp[cur_token_row_index] + str(old_token_col)
            row_dic = my_board[cur_token_row_index]
            cur_token_value = row_dic[key]

            while cur_token_value == "black" and cur_token_row_index - 1 >= 0:
                cur_token_row_index -= 1
                key = alp[cur_token_row_index] + str(old_token_col)
                row_dic = my_board[cur_token_row_index]
                cur_token_value = row_dic[key]
            
            if old_token_row_index - cur_token_row_index >= 2 and cur_token_value == "nothing":
                black_exist = True
                ai_pos = key
            
            # check downward
            if old_token_row_index + 1 >= len(alp):
                cur_token_row_index = old_token_row_index
            else:
                cur_token_row_index = old_token_row_index + 1
                
            key = alp[cur_token_row_index] + str(old_token_col)
            row_dic = my_board[cur_token_row_index]
            cur_token_value = row_dic[key]
            
            while cur_token_value == "black" and cur_token_row_index + 1 < self.side_length // 100:
                cur_token_row_index += 1
                key = alp[cur_token_row_index] + str(old_token_col)
                row_dic = my_board[cur_token_row_index]
                cur_token_value = row_dic[key]
            
            if cur_token_row_index - old_token_row_index >= 2 and cur_token_value == "nothing":
                black_exist = True
                ai_pos = key       
        
        # if there is no black token flippable in the same row and the 
        # the same column, check the two diagonals
        if black_exist == False:
            # check the top-left to bot-right diagonal
            # check to the top_left
            if old_token_row_index - 1 >= 0 and old_token_col - 1 >= 0:
                cur_token_row_index = old_token_row_index - 1
                cur_token_col = old_token_col - 1
                key = alp[cur_token_row_index] + str(cur_token_col)
                row_dic = my_board[cur_token_row_index]
                cur_token_value = row_dic[key]
                
                while (cur_token_value == "black" and 
                       cur_token_row_index - 1 >= 0 and cur_token_col - 1 >= 0):
                    cur_token_row_index -= 1
                    cur_token_col -= 1
                    key = alp[cur_token_row_index] + str(cur_token_col)
                    row_dic = my_board[cur_token_row_index]
                    cur_token_value = row_dic[key]
                    
                if old_token_col - cur_token_col >= 2 and cur_token_value == "nothing":
                    black_exist = True
                    ai_pos = key
                    
            # check to the bot_right
            if black_exist == False:
                if (old_token_row_index + 1 < self.side_length// 100
                    and old_token_col + 1 < self.side_length// 100):
                    cur_token_row_index = old_token_row_index + 1
                    cur_token_col = old_token_col + 1
                    key = alp[cur_token_row_index] + str(cur_token_col)
                    row_dic = my_board[cur_token_row_index]
                    cur_token_value = row_dic[key]
                
                while (cur_token_value == "black" and 
                       cur_token_row_index + 1 < self.side_length// 100
                       and cur_token_col + 1 < self.side_length// 100):
                    cur_token_row_index += 1
                    cur_token_col += 1
                    key = alp[cur_token_row_index] + str(cur_token_col)
                    row_dic = my_board[cur_token_row_index]
                    cur_token_value = row_dic[key]
                    
                if cur_token_col - old_token_col >= 2 and cur_token_value == "nothing":
                    black_exist = True
                    ai_pos = key
        
        # check the top_right to bot_left diagonal if there isn't 
        # flippable token in the previous three conditions
        if black_exist == False:
            # check to the top_right
            if old_token_row_index - 1 >= 0 and old_token_col + 1 < self.side_length// 100:
                cur_token_row_index = old_token_row_index - 1
                cur_token_col = old_token_col + 1
                key = alp[cur_token_row_index] + str(cur_token_col)
                row_dic = my_board[cur_token_row_index]
                cur_token_value = row_dic[key]
                
                while (cur_token_value == "black" and 
                       cur_token_row_index - 1 >= 0 and 
                       cur_token_col + 1 < self.side_length// 100):
                    cur_token_row_index -= 1
                    cur_token_col += 1
                    key = alp[cur_token_row_index] + str(cur_token_col)
                    row_dic = my_board[cur_token_row_index]
                    cur_token_value = row_dic[key]
                    
                if cur_token_col - old_token_col >= 2 and cur_token_value == "nothing":
                    black_exist = True
                    ai_pos = key
                    
            # check to the bot_left
            if black_exist == False:
                if (old_token_row_index + 1 < self.side_length// 100
                    and old_token_col - 1 >= 0):
                    cur_token_row_index = old_token_row_index + 1
                    cur_token_col = old_token_col - 1
                    key = alp[cur_token_row_index] + str(cur_token_col)
                    row_dic = my_board[cur_token_row_index]
                    cur_token_value = row_dic[key]
                
                while (cur_token_value == "black" and 
                       cur_token_row_index + 1 < self.side_length// 100
                       and cur_token_col - 1 >= 0):
                    cur_token_row_index += 1
                    cur_token_col -= 1
                    key = alp[cur_token_row_index] + str(cur_token_col)
                    row_dic = my_board[cur_token_row_index]
                    cur_token_value = row_dic[key]
                    
                if old_token_col - cur_token_col >= 2 and cur_token_value == "nothing":
                    black_exist = True
                    ai_pos = key
                    
        if black_exist == False:
            ai_pos = "not exist"
        
        return ai_pos, black_exist
    
    
    def flip(self, pos, color, my_board):
        """
        This is the method that flips all the tokens.
        
        Parameter:
        pos (string) - the position of the new token
        color (string) - the color of the new token
        """
        pos_row = pos[0]
        pos_col = int(pos[1])
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        alp = alphabet[:self.side_length // 100]
        row_index = alp.index(pos_row)
        
        self.flip_row(my_board, row_index, pos_row, pos_col, color)
        self.flip_col(my_board, row_index, pos_row, pos_col, color, alp)
        
        self.flip_dia1(my_board, row_index, pos_row, pos_col, color, alp, pos)
        self.flip_dia2(my_board, row_index, pos_row, pos_col, color, alp, pos)
        
        # print(my_board)
        
        
    def flip_dia2(self, my_board, row_index, pos_row, pos_col, color, alp, pos):
        """
        This method flips the tokens on the top_left to bot_right diagonal line.
        Start from creating a list of the grid value of all the grids on the same 
        diagonal line.
        
        Parameters:
        my_board (list) - the list of dictionaries where the grid values are stored
        row_index (number) - the index number of the row
        pos_row (string) - the row letter of the new token
        pos_col (number) - the column number of the new token
        color (string) - the color of the new token
        alp (string) - the string of all the row letters
        pos (string) - the position of the new token
        """
        
        diagonal_difference = abs(pos_col - row_index)
        key_list = []
        
        if row_index <= pos_col:            
            for col in range(self.side_length // 100 - 1, diagonal_difference - 1, -1):
                key = alp[col - diagonal_difference] + str(col)
                key_list.append(key)
            key_list.reverse()
        else:
            for col in range(0, self.side_length // 100 - diagonal_difference, 1):
                key = alp[col + diagonal_difference] + str(col)
                key_list.append(key)
                
        
        dia_list = []
        index = 0
        row = 0
        
        while row < len(alp) and index < len(key_list):
            row_dic = my_board[row]
            cur_key = key_list[index]
            if cur_key in row_dic:
                index += 1
                dia_list.append(row_dic[cur_key])
            row += 1
                
        #print(dia_list)
        
        self.comparison_dia(alp, dia_list, row_index, pos_col, pos_row, color, key_list, pos)
        
        
    def flip_dia1(self, my_board, row_index, pos_row, pos_col, color, alp, pos):
        """This method flips the tokens on the bot_left to top_right diagonal line
        For the details of how the algorithm works, see the comment on method "flip_dia2".
        
        Parameters:
        my_board (list) - the list of dictionaries where the grid values are stored
        row_index (number) - the index number of the row
        pos_row (string) - the row letter of the new token
        pos_col (number) - the column number of the new token
        color (string) - the color of the new token
        alp (string) - the string of all the row letters
        pos (string) - the position of the new token
        """
        diagonal_sum = row_index + pos_col
        key_list = []    
        
        if diagonal_sum < len(alp):
            for i in range(0, diagonal_sum + 1):
                key = alp[i] + str(diagonal_sum - i)
                key_list.append(key)
        else:
            for i in range(diagonal_sum - (len(alp) - 1),len(alp)):
                key = alp[i] + str(diagonal_sum - i)
                key_list.append(key)
        
        # creates a list of value of the grids on the bot-left to up-right diagonal
        dia_list = []
        row = 0
        index = 0
        while row < len(alp) and index < len(key_list):
            row_dic = my_board[row]
            if key_list[index] in row_dic:
                dia_list.append(row_dic[key_list[index]])
                index += 1
            row += 1
        
        self.comparison_dia(alp, dia_list, row_index, pos_col, pos_row, color, key_list, pos)
        
        
    def flip_col(self, my_board, row_index, pos_row, pos_col, color, alp):
        """
        This method flips the token in the same column.
        
        Parameters:
        my_board (dictionary) - the dictionary of the board object
        row_index (integer) - the corresponding index of the row letter
        pos_row (string) - the row letter
        pos_col (integer) - the index of the column number
        color (string) - color of the new token
        alp (string) - the string of all the row letters
        """
        
        # create a list of the target grids(grids in the same column)
        key_list = []
        for ch in alp:
            key = ch + str(pos_col)
            key_list.append(key)
        
        # creates a list of the value of the grids in the same column
        col_list = []
        row = 0
        while row < len(alp):
            row_dic = my_board[row]
            col_list.append(row_dic[key_list[row]])
            row += 1       
        
        self.comparison_col(alp, col_list, row_index, pos_col, pos_row, color)
        
        
    def flip_row(self, my_board, row_index, pos_row, pos_col, color):
        """
        This method flips all the tokens in the same row according to the rule.
        
        Parameters:
        my_board (dictionary) - the dictionary of the board object
        row_index (integer) - the corresponding index of the row letter
        pos_row (string) - the row letter
        pos_col (integer) - the index of the column number
        color (string) - color of the new token
        """
        # check row, we could probably make this a function
        row_dic = my_board[row_index]
        # construct a key
        cur_col = 0 
        row_list = []
        
        # creates an ordered list of values of grids in this row
        while cur_col < len(row_dic):
            key = pos_row + str(cur_col)
            row_list.append(row_dic[key])
            cur_col += 1
        
        self.comparison_row(row_list, row_index, pos_col, pos_row, color)
                
        
    def comparison_col(self, alp, col_list, row_index, pos_col, pos_row, color):
        """
        This method checks whether there is an appropriate sub_list 
        in the same column and if there is, this method flips all the appropriate tokens 
        in that sublist.
        
        Parameters:
        row_index (integer) - the corresponding index of the row letter
        pos_row (string) - the row letter
        pos_col (integer) - the index of the column number
        color (string) - color of the new token
        alp (string) - the string of all the row letters
        col_list (list) - the list of grid values of grids in the same column
        """
        # checks upward
        if row_index - 1 >= 0:
            cur_row = row_index - 1
        else:
            cur_row = row_index
            
        while cur_row > 0 and col_list[cur_row] != color:
            cur_row -= 1
            
        if col_list[cur_row] == color:
            target_list = col_list[cur_row + 1: row_index]
        else:
            target_list = []
            
        if target_list != [] and "nothing" not in target_list:
            for row in range(cur_row + 1, row_index):
                key = alp[row] + str(pos_col)
                self.board.get_board()[row][key] = color
                new_token = token.Token(key, color)
                new_token.create_token(self.board)
                
        # checks downward
        if row_index + 1 < len(col_list):
            cur_row = row_index + 1
        else:
            cur_row = row_index
        
        while cur_row < len(col_list) - 1 and col_list[cur_row] != color:
            cur_row += 1
        
        if col_list[cur_row] == color:
            target_list = col_list[row_index + 1: cur_row]
        else:
            target_list = []
            
        if target_list != [] and "nothing" not in target_list:
            for row in range(row_index + 1, cur_row):
                key = alp[row] + str(pos_col)
                self.board.get_board()[row][key] = color
                new_token = token.Token(key, color)
                new_token.create_token(self.board)
                
                
    def comparison_dia(self, alp, dia_list, row_index, pos_col, pos_row, color, key_list, pos):
        """
        This method checks whether there is an appropriate sub_list 
        in the same diagonal line and if there is, this method flips all the appropriate tokens 
        in that sublist.
        
        Parameters:
        row_index (integer) - the corresponding index of the row letter
        pos_row (string) - the row letter
        pos_col (integer) - the index of the column number
        color (string) - color of the new token
        alp (string) - the string of all the row letters
        dia_list (list) - a list of grid values of grids on the same diagonal line
        key_list (lsit) - a list of the coordinates of grids on the same diagonal line
        pos (string) - the position of the current token
        """
        pos_in_list = key_list.index(pos)
        
        if pos_in_list - 1 >= 0:
            cur_pos_in_list = pos_in_list - 1
        else:
            cur_pos_in_list = pos_in_list
            
        while cur_pos_in_list > 0 and dia_list[cur_pos_in_list] != color:
            cur_pos_in_list -= 1
        
        if dia_list[cur_pos_in_list] == color:
            target_list = dia_list[cur_pos_in_list + 1: pos_in_list]
        else:
            target_list = []
            
        if target_list != [] and "nothing" not in target_list:
            for pos in range(cur_pos_in_list + 1, pos_in_list):
                key = key_list[pos]
                row = alp.index(key[0])
                self.board.get_board()[row][key] = color
                new_token = token.Token(key, color)
                new_token.create_token(self.board)
                
        if pos_in_list + 1 < len(dia_list):
            cur_pos_in_list = pos_in_list + 1
        else:
            cur_pos_in_list = pos_in_list        
            
        while cur_pos_in_list < len(dia_list) - 1 and dia_list[cur_pos_in_list] != color:
            cur_pos_in_list += 1
            
            
        if dia_list[cur_pos_in_list] == color:
            target_list = dia_list[pos_in_list + 1: cur_pos_in_list]
        else:
            target_list = []
            
        if target_list != [] and "nothing" not in target_list:
            for pos in range(pos_in_list + 1, cur_pos_in_list):
                key = key_list[pos]
                row = alp.index(key[0])
                self.board.get_board()[row][key] = color
                new_token = token.Token(key, color)
                new_token.create_token(self.board)
                
        
    def comparison_row(self, row_list, row_index, pos_col, pos_row, color):
        """
        This method checks whether there is an appropriate sub_list 
        in the same row and if there is, this method flips all the appropriate tokens 
        in that sublist.
        
        Parameters:
        row_index (integer) - the corresponding index of the row letter
        pos_row (string) - the row letter
        pos_col (integer) - the index of the column number
        color (string) - color of the new token
        alp (string) - the string of all the row letters
        row_list (list) - the list of grid values of grids in the same row
        """
        # look to the left of the new token and see if we can flip some tokens
        if pos_col - 1 >= 0:
            cur_col = pos_col - 1
        else:
            cur_col = pos_col
            
        while cur_col > 0 and row_list[cur_col] != color:
            cur_col -= 1
            
        # check whether while loop stops because it reaches the end or hits a same-color token
        # takes the range between two same_color tokens and make it a list
        if row_list[cur_col] == color:
            target_list = row_list[cur_col + 1: pos_col]
        else:
            target_list = []
        
        # check if there is empty grid in the list
        if target_list != [] and "nothing" not in target_list:
            for col in range(cur_col + 1, pos_col):
                key = pos_row + str(col)
                self.board.get_board()[row_index][key] = color
                new_token = token.Token(key, color)
                new_token.create_token(self.board)
        
            
        # look to the right of the new token and see if we can flip some tokens
        if pos_col + 1 < len(row_list):
            cur_col = pos_col + 1
        else:
            cur_col = pos_col
        
        while cur_col < len(row_list) - 1 and row_list[cur_col] != color:
            cur_col += 1
        
        # check whether while loop stops because it reaches the end or hits a same-color token
        # takes the range between two same_color tokens and make it a list
        if row_list[cur_col] == color:
            target_list = row_list[pos_col + 1: cur_col]
        else:
            target_list = []
        
        # check if there is empty grid in the list
        if target_list != [] and "nothing" not in target_list:
            for col in range(pos_col + 1, cur_col):
                key = pos_row + str(col)
                self.board.get_board()[row_index][key] = color  
                new_token = token.Token(key, color)
                new_token.create_token(self.board)
                
                
    def pause(self, gap):
        time0 = time.time()
        time1 = time.time()
        while time1 - time0 < gap:
            time1 = time.time()
                
        
    def show_result(self):
        """
        This method calculates and displays the result to the user
        """
        self.pause(1)
        my_board = self.board.get_board()
        
        num_user = 0
        num_ai = 0
        
        back = graphics.Image(graphics.Point(self.win_side_length / 2, self.win_side_length / 2),
                              "intro_background.gif")
        back.draw(self.win)
        
        for dic in my_board:
            for key in dic:
                value = dic[key]
                if value == "black":
                    num_user += 1
                elif value == "white":
                    num_ai += 1
                    
        score = 100 * num_user // (num_user + num_ai)
        
        status = graphics.Text(graphics.Point(self.side_length / 2, self.side_length / 2 + 50),
                              "The board is fully occupied!"
                             + "\nBLACK has %d tokens on the board."%(num_user)
                             + "\nWHITE has %d tokens on the board."%(num_ai),)
        status.setFill("orange")
        status.setFace("courier")
        status.setStyle("bold")
        status.setSize(18)
        status.draw(self.win)
                    
        
        if num_user > num_ai:
            result = graphics.Text(graphics.Point(self.side_length / 2, self.side_length / 2 - 50),
                                  "Congratulations! BLACK win!!")
        elif num_user == num_ai:
            result = graphics.Text(graphics.Point(self.side_length / 2, self.side_length / 2 - 50),
                                  "It's a draw!")
        else:
            result = graphics.Text(graphics.Point(self.side_length / 2, self.side_length / 2 - 50),
                                  "I'm sorry BLACK lose :(")
        result.setFill("orange")
        result.setSize(21)
        result.setFace("courier")
        result.setStyle("bold")
        result.draw(self.win)
        
        score = graphics.Text(graphics.Point(self.side_length / 2, self.side_length / 2 - 100),
                             "BLACK's score is %d" %(score))
        score.setFill("orange")
        score.setSize(21)
        score.setFace("courier")
        score.setStyle("bold")
        score.draw(self.win)
        
        
    def end_page(self):
        """
        This method draws two buttons on the result screen. The restart button allows the 
        user to create a new game window and plays the game how many times he wants. The
        quit button allows the user to quit the game and close the window.
        """
        quit_but = button.Button(65, 25, graphics.Point(self.win_side_length / 2, 40),
                                "QUIT", self.win, 22, "orange")
        
        restart_but = button.Button(130, 25, graphics.Point(self.win_side_length / 2, 70),
                                   "NEW GAME", self.win, 22, "orange")
        p_click = self.win.getMouse()
        xclick = p_click.getX()
        yclick = p_click.getY()
        
        while (self.win_side_length / 2 - 32.5 > xclick 
               or xclick > self.win_side_length / 2 + 32.5 
               or 27.5 > yclick or yclick > 52.5):
            if (self.win_side_length / 2 - 65 <= xclick <= self.win_side_length / 2 + 65
                and 57.5 <= yclick <= 82.5):
                self.win.close()
                new_game = game.Game(self.win_side_length)
                new_game.play()
            else:
                p_click = self.win.getMouse()
                xclick = p_click.getX()
                yclick = p_click.getY()

        