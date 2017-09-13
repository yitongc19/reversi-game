"""
Yitong Chen
CS 111 Spring 2016 Final Project
This module contains the button class for the reversi game.
"""

import graphics

class Button:
    """button object for the lunar lander game"""
    
    def __init__(self, a_width, a_height, a_point, a_str, window, text_size, color):
        """
        This method is the constructor of the button class.
        
        Parameters:
        a_width (integer) - the width of the rectangular button
        a_height (integer) - the height of the rectangular button
        a_point (point) - the geometric center of the retangular button
        a_str (string) - the text that will show up on the button
        """
        self.width = a_width
        self.height = a_height
        self.cen_point = a_point
        
        # retrieve the x and y coordinates of the center point and 
        # save them as instance variables
        self.cen_point_x = a_point.getX()
        self.cen_point_y = a_point.getY()
        self.text = graphics.Text(self.cen_point, a_str)
        self.text.setSize(text_size)
        self.text.setFill(color)
        self.draw_but(window)
    
    
    def draw_but(self, window):
        """
        draws the button in the graphics window
        
        Parameter:
        window (window)- the window where the button is drawn
        """
        # draws the rectangular button
        p1 = graphics.Point(self.cen_point_x - self.width / 2, 
                            self.cen_point_y - self.height / 2)
        p2 = graphics.Point(self.cen_point_x + self.width / 2, 
                            self.cen_point_y + self.height / 2)
        self.button = graphics.Rectangle(p1, p2)
        self.button.setOutline("Orange")
        self.button.draw(window)
        
        # draws the text on the button
        self.text.draw(window)