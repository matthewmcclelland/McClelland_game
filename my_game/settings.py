import sys
import pygame
import time
import random
#from Game_with_seperate_files import Ball_Game NICK COMMENTED THIS OUT

class Settings():

    def __init__(self):
        super().__init__()
        pygame.init()

        #settings for all the different screens
        #self.ball_game = Ball_Game() NICK COMMENTED THIS OUT
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)


        self.screen_width = self.screen.get_rect().width #self.ball_game.screen_width # NICK COMMENTED THIS OUT
        self.screen_height = self.screen.get_rect().height #self.ball_game.screen_height # NICK COMMENTED THIS OUT

        self.screen_dimensions = (0, 0)
        self.screen_color = (255, 255, 255)

        self.restart_screen_color = (0, 255, 0)
        self.block1_won_text = 'Block 1 won!!'
        self.block2_won_text = 'block 2 won!!'

        self.difficulty_screen_color = (255, 255, 255)

        self.start_screen_color = (255, 255, 255)


        #settings for the buttons
        self.button_color = (0, 0, 0)
        self.text_color = (255, 255, 255)
        self.button_width = 250
        self.button_height = 50


        #settings for the blocks
        self.block_width = 200
        self.block_height = 20
        self.block_color = (0, 0, 0)

        #settings for the ball
        self.ball_color = (0, 0, 0)
        self.ball_radius = 15
        self.ball_width = 15
        self.ball_speed_x = 2
        self.ball_speed_y = 2
        self.original_speed_x = 2
        self.original_speed_y = 2

        self.font = pygame.font.SysFont(None, 48)


