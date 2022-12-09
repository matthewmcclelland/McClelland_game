import sys
import pygame
import time
import random
from settings import *
from start_screen import Start_screen
from restart_screen import Restart_screen
from difficulty_screen import Difficulty_screen

class Ball_Game():

    def __init__(self):
        super().__init__()
        pygame.init()
        pygame.mixer.init()

        self.background_sound = pygame.mixer.Sound('bensound-summer_ogg_music.ogg')

        self.font = pygame.font.SysFont(None, 48)

        # screen and screen settings
        self.settings = Settings()
        self.restart_screen = Restart_screen()
        self.difficulty_screen = Difficulty_screen()
        self.start_screen = Start_screen()

        self.screen = pygame.display.set_mode(self.settings.screen_dimensions, pygame.FULLSCREEN)
        pygame.display.set_caption('my game')
        self.screen_width = self.screen.get_rect().width
        self.screen_height = self.screen.get_rect().height

        # create blocks
        self.block1 = pygame.Rect(255, 255, self.settings.block_width, self.settings.block_height)
        self.block2 = pygame.Rect(255, 255, self.settings.block_width, self.settings.block_height)

        #ball position
        self.ball_x = self.settings.screen_width/2
        self.ball_y = self.settings.screen_height/2
        self.ball_pos = [self.ball_x, self.ball_y]

        #block1 position
        self.block1.x = 0
        self.block1.y = 0

        #block2 position
        self.block2.x = 0
        self.block2.y = self.settings.screen_height - 20

        #derermine if the block is moving
        self.block1_right = False
        self.block1_left = False

        self.block2_right = False
        self.block2_left = False

        self.block1_boundary = False
        self.block2_boundary = False

        # let's program know if blocks have been hit
        self.block1_hit = False
        self.block2_hit = False

        # which block is allowed to hit the ball
        self.block1_turn = False
        self.block2_turn = True

        # let's program know who loss the game
        self.block1_loss = False
        self.block2_loss = False

        # number of times that each block has been hit
        self.block1_times_hit = 0
        self.block2_times_hit = 0

        # block speed
        self.block_speed = 2

        # control what screen you are on
        self.start_screen_condition = True
        self.restart_screen_condition = False
        self.game_on = False
        self.difficulty_screen_condition = False

        # controls the difficulty chosen
        self.easy_game = False
        self.medium_game = False
        self.hard_game = False

        #controls the state of the buttons
        self.single_player_button_clicked = False
        self.multiplayer_button_clicked = False
        self.restart_button_clicked = False

        # controls which type of mode you are playing
        self.multiplayer = False
        self.single_player = False

        # condition to control the starting timer
        self.timer_condition = True

        #computer block
        self.computer_block_x = 0
        self.computer_block_speed = 1
        self.computer_block_location_to_get_to = 0
        self.computer_block_right = False
        self.computer_block_left = False
        self.computer_losses_condition = False
        self.slow_computer_down = 0

        self.ball_speed_x_increase = False
        self.ball_speed_x_decrease = False
        self.control_increase_decrease_time = 0

        self.game_score = 0
        self.high_score = 0
        self.game_score_text = ''

        self.easy_button_rect = pygame.Rect(0, 0, self.settings.button_width, self.settings.button_height)
        self.easy_button_rect.midleft = (self.settings.screen_width/2 - self.settings.button_width*2, self.settings.screen_height/2)
        self.easy_button_text = "Easy"
        self.easy_button_msg_image = self.font.render(self.easy_button_text, True, self.settings.text_color, self.settings.button_color)
        self.easy_button_msg_image_rect = self.easy_button_msg_image.get_rect()
        self.easy_button_msg_image_rect.center = self.easy_button_rect.center


        #Nick Zolovick Helped
        #Juan Ortiz

    def run_game(self):
        self.background_sound.play()
        while True:
            if not self.game_on and self.start_screen_condition == True:
                self.start_screen.display_start_screen()
                self.check_events()

            if self.difficulty_screen_condition == True:
                self.difficulty_screen.display_difficulty_screen()
                self.check_events()

            if self.game_on:
                self.check_events()
                self.check_collision_with_blocks()
                self.bounce_ball_of_blocks()
                self.cause_ball_variability()
                self.check_boundaries()
                self.check_ball_boundaries()
                self.move_blocks()
                self.set_hits_to_false()
                self.check_if_game_loss()
                self.timer()

            if not self.game_on and self.restart_screen_condition == True:
                self.restart_screen.display_restart_screen()
                self.check_events()

    def timer(self):

        if self.timer_condition:
            time.sleep(2)
            self.timer_condition = False

    def draw_blocks_and_ball(self):
        self.screen.fill(self.settings.screen_color)
        self.move_ball()
        pygame.draw.circle(self.screen, self.settings.ball_color, self.ball_pos, self.settings.ball_radius, self.settings.ball_width)
        pygame.draw.rect(self.screen, self.settings.block_color, self.block1)
        pygame.draw.rect(self.screen, self.settings.block_color, self.block2)
        pygame.display.flip()

    def move_blocks(self):
        if self.single_player:
            if self.computer_losses_condition == False:
                self.move_computer_block()
            self.slow_computer_down += 1
            if self.slow_computer_down % 3 == 0 and self.computer_losses_condition == True and self.easy_game:
                self.move_computer_block()
            if self.slow_computer_down % 2 == 0 and self.computer_losses_condition == True and self.medium_game:
                self.move_computer_block()
            if self.slow_computer_down % 2 == 0 and self.computer_losses_condition == True and self.hard_game:
                self.move_computer_block()

        if self.block1_right and self.multiplayer:
            self.block1.x += 1*self.block_speed
        if self.block1_left and self.multiplayer:
            self.block1.x += -1*self.block_speed
        if self.block2_right:
            self.block2.x += 1*self.block_speed
        if self.block2_left:
            self.block2.x += -1*self.block_speed
        self.draw_blocks_and_ball()

    def check_events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self.check_keydown(event)
            if event.type == pygame.KEYUP:
                self.check_keyup(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self.check_if_easy_button_clicked(mouse_pos)
                self.check_if_medium_button_clicked(mouse_pos)
                self.check_if_hard_button_clicked(mouse_pos)
                self.check_if_restart_button_clicked(mouse_pos)
                self.check_if_single_player_button_clicked(mouse_pos)
                self.check_if_multiplayer_button_clicked(mouse_pos)


    def check_if_multiplayer_button_clicked(self, mouse_pos):
        self.multiplayer_button_clicked = self.start_screen.multiplayer_button_rect.collidepoint(mouse_pos)
        # set all variables back to their original settings and change game on condition

        if self.multiplayer_button_clicked and self.game_on == False and self.start_screen_condition == True:
            self.initialize_game_var()
            self.multiplayer = True
            self.multiplayer_button_clicked = False
            self.single_player = False
            self.difficulty_screen_condition = True

    def initialize_game_var(self):
        self.block1_times_hit = 0
        self.block2_times_hit = 0
        self.ball_x = self.screen_width / 2
        self.ball_y = self.screen_height / 2
        self.ball_pos = [self.ball_x, self.ball_y]
        self.block1.x = self.screen_width / 2 - self.settings.block_width / 2
        self.block1.y = 0
        self.block2.x = self.screen_width / 2 - self.settings.block_width / 2
        self.block2.y = self.screen_height - 20
        self.start_screen_condition = False
        self.timer_condition = True
        self.computer_block_left = False
        self.computer_block_right = False
        self.medium_game = False
        self.hard_game = False
        self.easy_game = False
        self.computer_losses_condition = False
        self.block1_turn = False
        self.block2_turn = True
        self.game_score = 0

    def check_if_single_player_button_clicked(self, mouse_pos):
        self.single_player_button_clicked = self.start_screen.single_player_button_rect.collidepoint(mouse_pos)
        # set all variables back to their original settings and change game on condition
        if self.single_player_button_clicked and self.game_on == False and self.start_screen_condition == True:
            self.initialize_game_var()
            self.single_player = True
            self.single_player_button_clicked = False
            self.multiplayer = False
            self.difficulty_screen_condition = True

    def check_if_restart_button_clicked(self, mouse_pos):
        self.restart_button_clicked = self.restart_screen.restart_button_rect.collidepoint(mouse_pos)
        if self.restart_button_clicked and self.game_on == False and self.restart_screen_condition == True:
            self.start_screen_condition = True
            self.restart_button_clicked = False
            self.single_player_button_clicked = False
            self.restart_screen_condition = False
            self.single_player = False
            self.multiplayer = False
            self.easy_button_clicked = False
            self.difficulty_screen_condition = False

    def check_if_easy_button_clicked(self, mouse_pos):
        self.easy_button_clicked = self.difficulty_screen.easy_button_rect.collidepoint(mouse_pos)
        if self.easy_button_clicked and self.difficulty_screen_condition == True and self.start_screen_condition == False:
            self.ball_speed_x = 1
            self.ball_speed_y = 1
            self.difficulty_screen_condition = False
            self.single_player_button_clicked = False
            self.easy_button_clicked = False
            self.game_on = True
            self.easy_game = True

    def check_if_medium_button_clicked(self, mouse_pos):
        self.medium_button_clicked = self.difficulty_screen.medium_button_rect.collidepoint(mouse_pos)
        if self.medium_button_clicked and self.difficulty_screen_condition == True:
            self.ball_speed_x = 2
            self.ball_speed_y = 2
            self.difficulty_screen_condition = False
            self.single_player_button_clicked = False
            self.medium_button_clicked = False
            self.game_on = True
            self.medium_game = True

    def check_if_hard_button_clicked(self, mouse_pos):
        self.hard_button_clicked = self.difficulty_screen.hard_button_rect.collidepoint(mouse_pos)
        if self.hard_button_clicked and self.difficulty_screen_condition == True:
            self.ball_speed_x = 3
            self.ball_speed_y = 3
            self.block_speed = 3
            self.computer_block_speed = 4
            self.difficulty_screen_condition = False
            self.single_player_button_clicked = False
            self.game_on = True
            self.hard_button_clicked = False
            self.hard_game = True




    def check_keydown(self, event):

        if event.key == pygame.K_RIGHT:
            self.block1_right = True
        if event.key == pygame.K_LEFT:
            self.block1_left = True
        if event.key == pygame.K_d:
            self.block2_right = True
        if event.key == pygame.K_a:
            self.block2_left = True
        if event.key == pygame.K_ESCAPE:
            sys.exit()

    def check_keyup(self, event):

        if event.key == pygame.K_RIGHT:
            self.block1_right = False
        if event.key == pygame.K_LEFT:
            self.block1_left = False
        if event.key == pygame.K_d:
            self.block2_right = False
        if event.key == pygame.K_a:
            self.block2_left = False

    def check_boundaries(self):
        if self.block1.x >= self.settings.screen_width - self.settings.block_width:
            self.block1_boundary = True
            self.block1.x = self.settings.screen_width - self.settings.block_width
        if self.block1.x <= -1:
            self.block1_boundary = True
            self.block1.x = 0
        if self.block2.x >= self.settings.screen_width - self.settings.block_width:
            self.block2_boundary = True
            self.block2.x = self.settings.screen_width - self.settings.block_width
        if self.block2.x <= -1:
            self.block2_boundary = True
            self.block2.x = 0

    def move_ball(self):
        if not self.ball_speed_x_decrease or not self.ball_speed_x_increase and self.control_increase_decrease_time % 50 == 0 :
            self.ball_x = self.ball_x + self.ball_speed_x
            self.ball_y = self.ball_y + self.ball_speed_y
            self.ball_pos = [self.ball_x, self.ball_y]
        if self.ball_speed_x_increase:
            self.ball_y = self.ball_y + self.ball_speed_y
            self.ball_x = self.ball_x + self.ball_speed_x*2
            self.control_increase_decrease_time += 1
            self.ball_pos = [self.ball_x, self.ball_y]
            if self.control_increase_decrease_time % 50 == 0:
                self.ball_speed_x_increase = False
        if self.ball_speed_x_decrease:
            self.ball_x = self.ball_x + self.ball_speed_x*2
            self.ball_y = self.ball_y + self.ball_speed_y
            self.control_increase_decrease_time += 1
            self.ball_pos = [self.ball_x, self.ball_y]
            if self.control_increase_decrease_time % 50 == 0:
                self.ball_speed_x_decrease = False

    def check_ball_boundaries(self):
        if self.ball_x >= self.settings.screen_width:
            self.ball_speed_x = self.ball_speed_x*-1
        if self.block2_hit:
            self.ball_speed_y = self.ball_speed_y*-1
        if self.ball_x <= 0:
            self.ball_speed_x = self.ball_speed_x*-1
        if self.block2_hit:
            self.ball_speed_y = self.ball_speed_y*-1

    def bounce_ball_of_blocks(self):
        if self.block1_hit:
            self.ball_speed_y = self.ball_speed_y * -1
        if self.block2_hit:
            self.ball_speed_y = self.ball_speed_y * -1

    def check_collision_with_blocks(self):
        if self.ball_x >= self.block1.x and self.ball_x <= self.block1.x + self.settings.block_width:
            if self.ball_y <= self.block1.y + self.settings.block_height and self.block1_turn:
                self.block1_hit = True
                self.block1_times_hit += 1
                self.block1_turn = False
                self.block2_turn = True

        if self.ball_x >= self.block2.x and self.ball_x <= self.block2.x + self.settings.block_width:
            if self.ball_y >= self.block2.y - self.settings.block_height and self.block2_turn:
                self.block2_hit = True
                self.block2_times_hit += 1
                self.block2_turn = False
                self.block1_turn = True
                self.cause_computer_to_loss()

    def set_hits_to_false(self):
        self.block1_hit = False
        self.block2_hit = False

    def check_if_game_loss(self):
        if self.ball_y < 0:
            self.block1_loss = True
            self.game_on = False
            self.restart_screen_condition = True
        if self.ball_y > self.screen_height:
            self.block2_loss = True
            self.game_on = False
            self.restart_screen_condition = True

    def computer_controlled_block(self):
        keep_moving_left = False
        keep_moving_right = False
        if self.ball_x < self.block1.x + self.settings.block_width/2:
            keep_moving_right = True
        if self.ball_x > self.block1.x + self.settings.block_width/2:
            keep_moving_left = True

        if self.ball_speed_x > 0 and keep_moving_left:
            self.computer_block_left = True
        if self.ball_speed_x < 0 and keep_moving_right:
            self.computer_block_right = True

    def move_computer_block(self):
        self.computer_controlled_block()
        if self.computer_block_left:
            self.block1.x += 1 * self.block_speed
            self.computer_block_left = False
        if self.computer_block_right:
            self.block1.x += -1 * self.block_speed
            self.computer_block_right = False

    def cause_computer_to_loss(self):
        value = random.randint(0, 100)
        if value < 6 and self.hard_game == True:
            self.computer_losses_condition = True
        if value < 15 and self.medium_game == True:
            self.computer_losses_condition = True
        if value < 0 and self.easy_game == True:
            self.computer_losses_condition = True

    def cause_ball_variability(self):
        if self.block1_hit and self.block1_right:
            self.ball_speed_x_increase = True
        if self.block1_hit and self.block1_left:
            self.ball_speed_x_decrease = True
        if self.block2_hit and self.block2_right:
            self.ball_speed_x_increase = True
        if self.block2_hit and self.block2_left:
            self.ball_speed_x_decrease = True

    def display_game_score(self):
        self.game_score = self.block2_times_hit
        


game = Ball_Game()
game.run_game()

