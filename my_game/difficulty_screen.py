import sys
import pygame
import time
import random
from settings import Settings

class Difficulty_screen():

    def __init__(self):
        super().__init__()
        pygame.init()
        self.settings = Settings()
        # difficulty screen
        self.difficulty_screen = pygame.display.set_mode(self.settings.screen_dimensions, pygame.FULLSCREEN)
        self.difficulty_screen_rect = self.difficulty_screen.get_rect()
        self.font = pygame.font.SysFont(None, 48)

        # creating the easy button
        self.easy_button_rect = pygame.Rect(0, 0, self.settings.button_width, self.settings.button_height)
        self.easy_button_rect.midleft = (self.settings.screen_width/2 - self.settings.button_width*2, self.settings.screen_height/2)
        self.easy_button_text = "Easy"
        self.easy_button_msg_image = self.settings.font.render(self.easy_button_text, True, self.settings.text_color, self.settings.button_color)
        self.easy_button_msg_image_rect = self.easy_button_msg_image.get_rect()
        self.easy_button_msg_image_rect.center = self.easy_button_rect.center

        #creating the medium button
        self.medium_button_rect = pygame.Rect(0, 0, self.settings.button_width, self.settings.button_height)
        self.medium_button_rect.center = self.difficulty_screen_rect.center
        self.medium_button_text = "Medium"
        self.medium_button_msg_image = self.settings.font.render(self.medium_button_text, True, self.settings.text_color, self.settings.button_color)
        self.medium_button_msg_image_rect = self.medium_button_msg_image.get_rect()
        self.medium_button_msg_image_rect.center = self.medium_button_rect.center

        #creating the hard button
        self.hard_button_rect = pygame.Rect(0, 0, self.settings.button_width, self.settings.button_height)
        self.hard_button_rect.midright = (self.settings.screen_width/2 + self.settings.button_width*2, self.settings.screen_height/2)
        self.hard_button_text = "Hard"
        self.hard_button_msg_image = self.settings.font.render(self.hard_button_text, True, self.settings.text_color, self.settings.button_color)
        self.hard_button_msg_image_rect = self.hard_button_msg_image.get_rect()
        self.hard_button_msg_image_rect.center = self.hard_button_rect.center

    def display_difficulty_screen(self):
            self.difficulty_screen.fill(self.settings.difficulty_screen_color)
            self.display_hard_button()
            self.display_medium_button()
            self.display_easy_button()
            pygame.display.flip()

    def display_hard_button(self):
            self.difficulty_screen.fill(self.settings.button_color, self.hard_button_rect)
            self.difficulty_screen.blit(self.hard_button_msg_image, self.hard_button_msg_image_rect)

    def display_medium_button(self):
            self.difficulty_screen.fill(self.settings.button_color, self.medium_button_rect)
            self.difficulty_screen.blit(self.medium_button_msg_image, self.medium_button_msg_image_rect)

    def display_easy_button(self):
            self.difficulty_screen.fill(self.settings.button_color, self.easy_button_rect)
            self.difficulty_screen.blit(self.easy_button_msg_image, self.easy_button_msg_image_rect)
