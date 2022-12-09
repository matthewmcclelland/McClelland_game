import sys
import pygame
import time
import random
from settings import Settings

class Restart_screen():

    def __init__(self):
        super().__init__()
        pygame.init()
        self.settings = Settings()
        self.font = pygame.font.SysFont(None, 48)

        # restart screen
        self.restart_screen = pygame.display.set_mode(self.settings.screen_dimensions, pygame.FULLSCREEN)
        self.restart_screen_rect = self.restart_screen.get_rect()

        #restart screen button
        self.restart_button_rect = pygame.Rect(0, 0, self.settings.button_width, self.settings.button_height)
        self.restart_button_rect.center = self.restart_screen_rect.center
        self.restart_button_text = "play again"
        self.restart_button_msg_image = self.settings.font.render(self.restart_button_text, True, self.settings.text_color, self.settings.button_color)
        self.restart_button_msg_image_rect = self.restart_button_msg_image.get_rect()
        self.restart_button_msg_image_rect.center = self.restart_button_rect.center

    def display_restart_screen(self):
            self.restart_screen.fill(self.settings.restart_screen_color)
            self.display_restart_button()
            # print('1')
            # print(self.settings.game_score)
            pygame.display.flip()

    def display_restart_button(self):
            self.restart_screen.fill(self.settings.button_color, self.restart_button_rect)
            self.restart_screen.blit(self.restart_button_msg_image, self.restart_button_msg_image_rect)

