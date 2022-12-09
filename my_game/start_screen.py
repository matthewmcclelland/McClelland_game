import sys
import pygame
import time
import random
from settings import Settings

class Start_screen():

    def __init__(self):
        super().__init__()
        pygame.init()

        self.settings = Settings()
        self.start_screen = pygame.display.set_mode(self.settings.screen_dimensions, pygame.FULLSCREEN)
        self.start_screen_rect = self.start_screen.get_rect()
        self.font = pygame.font.SysFont(None, 48)

        self.multiplayer_button_rect = pygame.Rect(0, 0, self.settings.button_width, self.settings.button_height)
        self.multiplayer_button_rect.midright = (self.settings.screen_width - 200, self.settings.screen_height/2)
        self.multiplayer_text = "Multiplayer"
        self.multiplayer_button_msg_image = self.settings.font.render(self.multiplayer_text, True, self.settings.text_color, self.settings.button_color)
        self.multiplayer_button_msg_image_rect = self.multiplayer_button_msg_image.get_rect()
        self.multiplayer_button_msg_image_rect.center = self.multiplayer_button_rect.center

        self.single_player_button_rect = pygame.Rect(0, 0, self.settings.button_width, self.settings.button_height)
        self.single_player_button_rect.midleft = (200, self.settings.screen_height/2)
        self.single_player_text = "Single Player"
        self.single_player_button_msg_image = self.settings.font.render(self.single_player_text, True, self.settings.text_color, self.settings.button_color)
        self.single_player_button_msg_image_rect = self.single_player_button_msg_image.get_rect()
        self.single_player_button_msg_image_rect.center = self.single_player_button_rect.center

    def display_start_screen(self):
        self.start_screen.fill(self.settings.start_screen_color)
        self.display_multiplayer_button()
        self.display_single_player_button()
        pygame.display.flip()

    def display_multiplayer_button(self):
        self.start_screen.fill(self.settings.button_color, self.multiplayer_button_rect)
        self.start_screen.blit(self.multiplayer_button_msg_image, self.multiplayer_button_msg_image_rect)

    def display_single_player_button(self):
        self.start_screen.fill(self.settings.button_color, self.single_player_button_rect)
        self.start_screen.blit(self.single_player_button_msg_image, self.single_player_button_msg_image_rect)