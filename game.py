"""
Yitong Chen
CS 111 Spring 2016 Final Project
This module contains the Game class and the main function to play the reversi game.
"""
import board
import interface
import graphics
import token


class Game:
    """The reversi game object"""
    
    def __init__(self, side_length):
        """
        This method is the constructor method of the Game class.
        
        Parameter:
        side_length (integer) - side_length of the game board and the game window
        """
        self.interface = interface.GraphicBasedInterface(side_length)
        self.side_length = side_length
        
        
    def initiator(self):
        """
        This method initializes four tokens in the middle of the board.
        Two for the player, two for the opponent, arranged on the two diagonal lines.
        """
        
        half_length = self.side_length // 2 // 100
        alp = "abcdefghijklmnopqrstuvwxyz"
        row_index = half_length
        interface = self.interface
        game_board = interface.board
        
        # creates the four token object
        token1 = token.Token(alp[row_index] + str(half_length), "black")
        token2 = token.Token(alp[row_index - 1] + str(half_length - 1), "black")
        token3 = token.Token(alp[row_index - 1] + str(half_length), "white")
        token4 = token.Token(alp[row_index] + str(half_length - 1), "white")
        
        # draws the tokens on the board
        token1.create_token(game_board)
        token2.create_token(game_board)
        token3.create_token(game_board)
        token4.create_token(game_board)
        
        
    def play(self):
        """
        This method does all the work of playing the game. The user and the opponent 
        can take turns laying their tokens on the board. The program will automatically
        flip the tokens in between according to the rule. 
        The game ends when there is no empty grid on the board or there are only tokens of 
        one side on the board.
        When the game ends, the user can choose whether to quit or to start a new game.
        """
        interface = self.interface
        game_board = interface.board
        
        # initializes the number of empty grids
        num_empty_grid = (game_board.get_sideGrid()) ** 2 - 4
        
        # calls the initiator method to lay the initial four tokens on the board
        self.initiator()
        
        # the game continues when there is still empty grids on the board
        while num_empty_grid > 0:
            # wait for the user to choose where to lay his token, 
            # get the grid where the user click his mouse
            token_pos = interface.get_pos()
            
            # check if the position is a valid position on the board
            check_pos = interface.check_pos(token_pos)
            
            # keep asking user until get a valid position on the board
            while check_pos != True:
                print("Please enter a valid position!")
                token_pos = interface.get_pos()
                check_pos = interface.check_pos(token_pos)
                
            while game_board.retrieve_grid(token_pos) != "nothing":
                print("The grid is occupied!")
                token_pos = interface.get_pos()
        
            # creates a user token at the position the user chooses
            # pause for 0.3 seconds before it updates the board by flipping 
            # some opponent tokens according to the rules
            new_token = token.Token(token_pos, "black")
            new_token.create_token(game_board)
            interface.flip(token_pos, "black", game_board.get_board())
            
            # update the number of empty grids on the board
            num_empty_grid -= 1
            
            # check whether the game can still continue
            if num_empty_grid > 0:
                
                # runs the following code if the user chooses to play against an AI
                if interface.mode == "ai":
                    
                    # pause for one second so that the user can see what the board looks like
                    # before the opponent places its token
                    interface.pause(.7)
        
                    # the ai runs a bunch of algorithms and returns a position where
                    # it chooses to place its token
                    ai_pos = interface.ai_play("white", interface.level)
                    
                    # if the ai finds no appropriate position to place its token,
                    # it allows the user to operate one more step
                    while ai_pos == "not exist" and num_empty_grid > 0:
                        token_pos = interface.get_pos()
                        # check if the position is a valid position in the board
                        check_pos = interface.check_pos(token_pos)

                        # keep asking user until get a valid input
                        while check_pos != True:
                            print("Please enter a valid position!")
                            token_pos = interface.get_pos()
                            check_pos = interface.check_pos(token_pos)

                        while game_board.retrieve_grid(token_pos) != "nothing":
                            print("The grid is occupied!")
                            token_pos = interface.get_pos()

                        # update the board after the player puts his token
                        new_token = token.Token(token_pos, "black")
                        new_token.create_token(game_board)
                        interface.flip(token_pos, "black", game_board.get_board())
                        
                        # update the number of empty grids
                        num_empty_grid -= 1
                        
                        # the ai would try again and see whether there is a place to put its 
                        # token at this point
                        ai_pos = interface.ai_play("white", interface.level)
                    
                    # check at this point whether there is still empty grid on the board
                    # if there is no empty grid, display the result and the ending page
                    if num_empty_grid == 0:
                        interface.show_result()
                        interface.end_page()

                    # if the game continues, update the board according to where
                    # the ai places its token
                    ai_token = token.Token(ai_pos, "white")
                    ai_token.create_token(game_board)
                    interface.flip(ai_pos, "white", game_board.get_board())
                    
                    # keep track of the number of empty grids
                    num_empty_grid -= 1
                
                # if the user chooses the "player versus player" mode of the game,
                # run the following codes
                elif interface.mode == "pp":
                    # gets the position where the second use rwants to place his token
                    token_pos = interface.get_pos()
                    # check if the position is a valid position in the board
                    check_pos = interface.check_pos(token_pos)

                    # keep asking second user until get a valid input
                    while check_pos != True:
                        print("Please enter a valid position!")
                        token_pos = interface.get_pos()
                        check_pos = interface.check_pos(token_pos)

                    while game_board.retrieve_grid(token_pos) != "nothing":
                        print("The grid is occupied!")
                        token_pos = interface.get_pos()

                    # update the board after the second user puts his token
                    new_token = token.Token(token_pos, "white")
                    new_token.create_token(game_board)
                    interface.flip(token_pos, "white", game_board.get_board())
                    
                    # keep track of the number of empty grid on the board
                    num_empty_grid -= 1
                    
                    # terminate the game if the board is fully occupied at this point
                    if num_empty_grid == 0:
                        interface.show_result()
                        interface.end_page()
                    
                # after both sides finished their moves, check whether there still are two 
                # kinds of tokens on the board. If there is only one kind of token on the board,
                # terminates the game and display the results
                black_exist = False
                white_exist = False
                    
                for dic in interface.board.get_board():
                    for key in dic:
                        if dic[key] == "black":
                            black_exist = True
                        elif dic[key] == "white":
                            white_exist = True
                            
                if black_exist == False:
                    interface.show_result()
                    interface.end_page()
                elif white_exist == False:
                    interface.show_result()
                    interface.end_page()
            
        interface.show_result()
        
        interface.end_page()  

        
def main():
    # ask the user to whether s/he wants to start with a large board or a small board
    size = input("Do you want a small board or large board? ")
    
    # keep asking the user until getting a valid input
    while size != "small" and size != "large":
        if size == "quit":
            return
        print("Please enter 'small' or 'large'!")
        size = input("Do you want a small board or large board? ")
    
    # set the side length accordingly
    if size == "small":
        side_length = 400
    else:
        side_length = 600
    
    # creates a game instance and play the game
    game = Game(side_length)
    
    game.play()

# allows the game to be runnable from the command line
if __name__ == "__main__":
    main()
        