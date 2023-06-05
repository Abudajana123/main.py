import pygame
from sys import exit
from random import randint, choice, randrange
import numpy as np
import time
import button
from pygame.locals import *
import pygame_gui

pygame.init()
screen_width = 700
screen_height = 1000
player_pos = (350, 700)
screen = pygame.display.set_mode((screen_width, screen_height))
manager = pygame_gui.UIManager((640, 480))
pygame.display.set_caption('doodle jump')
clock = pygame.time.Clock()
player_y = 700
test_font = pygame.font.Font('font/Pixeltype (1).ttf', 50)
test_font1 = pygame.font.Font('font/Pixeltype (1).ttf', 100)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PLATFORM_WIDTH = 100
PLATFORM_HEIGHT = 20
PLATFORM_SPEED = 0.1
PLATFORM_TIMER_MAX = 1

current_time = 0

start_platform = pygame.image.load('graphics/shapes/line.png')
start_platform_rect = start_platform.get_rect(midbottom=(350, 700))

game_title_surface = test_font.render('Doodle brain', False, (111, 196, 169))
game_title_rectangle = game_title_surface.get_rect(center=(400, 70))
start_time = 0
scroll_speed = 0
display_current_tiles = True
platform_width = 50
platform_height = 10
platform_list = [[randint(0, screen_width - PLATFORM_WIDTH), i * 150] for i in range(5)]
platform_max_distance = 2999
key_pressed= None
player_fall = 10

class Button():
	def __init__(self, x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self, surface):
		action = False
		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button on screen
		surface.blit(self.image, (self.rect.x, self.rect.y))

		return action


start_img = pygame.image.load('graphics/buttons/start_btn.png').convert_alpha()
exit_img = pygame.image.load('graphics/buttons/exit_btn.png').convert_alpha()

start_button = Button(100, 700, start_img, 0.8)
exit_button = Button(450, 700, exit_img, 0.8)


player = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_res = pygame.transform.scale2x(player)
player_rect1 = player_res.get_rect(midbottom=(370,600))
player_rect = player.get_rect(midbottom=(player_pos[0],player_pos[1]))

num_platforms = 16
TILE_DISPLAY_TIME = 3000
next_tile_time = pygame.time.get_ticks() + TILE_DISPLAY_TIME

sky_surface = pygame.image.load('graphics/sky_new.png').convert_alpha()
sky_surface = pygame.transform.rotozoom(sky_surface, 0, 4)
game_active = True

player_speed_y = 18
press_surface = test_font1.render('Doodle Jump', False, (111, 196, 169))
press_rectangle = press_surface.get_rect(midbottom=(370, 300))
scroll_y = 5
score = 0


player_jump = False
player_jump_speed = 10
player_speed = 1
player_rect.bottomleft = player_pos

button_text = "Start Game"
button_font = pygame.font.SysFont("Arial", 32)
button_color = pygame.Color("dodgerblue")
button_rect = pygame.Rect(200, 200, 200, 50)

platforms = pygame.image.load('graphics/shapes/line.png')
platforms = platforms.convert_alpha() 


def toggle_game_active():
    global game_active
    game_active = not game_active

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000 - start_time)
    score_surface = test_font.render(f'score: {current_time}', False, '#646464')
    score_rectangle = score_surface.get_rect(center=(400, 50))
    screen.blit(score_surface, score_rectangle)

    return current_time

score_message = test_font.render(f'Your score: {current_time}',False,(111,196,169))
score_message_rect = score_message.get_rect(midbottom = (370,400))

def update_player():
        if game_active == True:
            player_rect.bottom += player_fall
        else:
            player_rect.bottom = start_platform_rect.top
            player_rect.bottom = platform_rect.top

def rect_overlap(rect1, rect2):
    """Check if two pygame.Rect objects overlap."""
    x_overlap = rect1.left < rect2.right and rect1.right > rect2.left
    y_overlap = rect1.top < rect2.bottom and rect1.bottom > rect2.top
    return x_overlap and y_overlap

def draw_tile(x, y):
    platform_rect = pygame.Rect(x, y, platform_width, platform_height)
    pygame.draw.rect(screen, BLACK, platform_rect, 2, 3)
    return platform_rect

for i in range(num_platforms):
    x = randrange(0, screen_width - platform_width + 1, 1)
    y = np.random.randint(player_y - platform_max_distance - platform_height, player_y - platform_height + 1, size=1)[0]
platform_rect = pygame.Rect(x,y,PLATFORM_WIDTH,platform_height)
for platform in platform_list:
    if platform is not None and len(platform) >= 4:
        platform_rect = pygame.Rect(platform[0], platform[1], platform[2], platform[3])

def create_platforms(num_platforms, screen_width, platform_width, platform_height, platform_max_distance, player_pos):
    global platform_list
    platform_list = []

    # Create the first platform near the player
    x = randint(0, screen_width - platform_width)
    y = player_pos[1] + platform_height
    platform_rect = pygame.Rect(x, y, platform_width, platform_height)
    platform_list.append(platform_rect)

    # Create the remaining platforms
    for i in range(num_platforms-1):
        while True:
            x = randint(0, screen_width - platform_width)
            y = randint(-platform_max_distance, 0)
            platform_rect = pygame.Rect(x, y, platform_width, platform_height)
            overlap = False
            for existing_platform in platform_list:
                if platform_rect.colliderect(existing_platform):
                    overlap = True
                    break
            if not overlap:
                platform_list.append(platform_rect)
                break

def handle_platform_collision(player_rect, platform_list):
    PLATFORM_WIDTH = 80
    player_y = 0  # Define a default value for player_y
    for platform in platform_list:
        screen.blit(platforms, (platform[0], platform[1]))
        if player_rect.colliderect(platform):
            if player_rect.bottom >= platform[1] and player_rect.bottom <= platform[1] + 10 and player_rect.right >= platform[0] and player_rect.left <= platform[0] + PLATFORM_WIDTH:
                player_rect.bottom = platform[1]
                player_y = player_rect.bottom - player_rect.height
    return player_rect, player_y

def check_collision():
    for platform_rect in platform_list:
        if player_rect.colliderect(platform_rect):
            if player_rect.bottom >= platform_rect.top and player_rect.bottom <= platform_rect.top + player_jump_speed:
                player_rect.bottom = platform_rect.top
                return True
    if player_rect.top <= 0:
        player_rect.top = 0
        return True
    return False

def update_platforms():
    global platform_list
    new_platform_list = []
    if not platform_list:
        return  
    for platform_rect in platform_list:
        if not isinstance(platform_rect, pygame.Rect):
            continue  
        platform_rect.y += scroll_y
        if platform_rect.y >= screen_height:
            platform_rect.y = -platform_height
            platform_rect.x = randint(0, screen_width - platform_width)
        
        new_platform_list.append(platform_rect)
    
    platform_list = new_platform_list

def reset_values():
    global platform_list, player_rect, player_y, scroll_speed, start_platform_rect, game_active,score,current_time
    platform_list = [[randint(0, screen_width - PLATFORM_WIDTH), i * 150] for i in range(5)]
    player_rect.bottomleft = player_pos
    player_y = player_pos[1]
    scroll_speed = 0
    current_time = 0
    start_platform_rect.bottom = player_pos[1]
    game_active = False
    score = 0
    create_platforms(num_platforms,screen_width,platform_width,platform_height,platform_max_distance,player_pos)

create_platforms(num_platforms,screen_width,platform_width,platform_height,platform_max_distance,player_pos)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN and not game_active:
            game_active = True
        elif event.type == pygame.KEYDOWN and game_active:
            if event.type == pygame.K_LEFT:
                player_rect.x -= 10
            elif event.type == pygame.K_RIGHT:
                player_rect.x += 10
            elif event.type == pygame.K_UP:
                player_rect.y -= 30
        elif event.type == pygame.KEYDOWN:
            game_started = True
            key_pressed = True
        elif event.type == pygame.KEYUP:
            key_pressed = False

    screen.blit(sky_surface, (0, 0))
    screen.blit(player, player_rect)
    
    if game_active:
        scroll_speed += 0.01
        player_fall += 0.0001
        scroll_y = int(scroll_speed)
        update_platforms()
        update_player()
        for platform in platform_list:
            screen.blit(platforms, (platform[0], platform[1]))
            if player_rect.colliderect(platform):
                if player_rect.bottom >= platform[1] and player_rect.bottom <= platform[1] + 10 and player_rect.right >= platform[0] and player_rect.left <= platform[0] + PLATFORM_WIDTH:
                    player_rect.bottom = platform[1]
                    player_y = player_rect.bottom - player_rect.height


        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_rect.left > 0:
            player_rect.move_ip(-5, 0)
        if keys[pygame.K_RIGHT] and player_rect.right < screen_width:
            player_rect.move_ip(5, 0)
        if keys[pygame.K_UP]:
            player_rect.top -= 20

        for platform in platform_list:
            if player_rect.colliderect(platform_rect):
                player_rect.bottom == player_rect.top

        if player_rect.top > screen_height:
            game_over = True
        elif check_collision():
            player_speed = 0

        if player_rect.bottom != platform_rect.top and start_platform_rect:
            pass

        score = display_score()

        if player_rect.right >= screen_width:
            player_rect.left = 0
        elif player_rect.left <= 0:
            player_rect.right = screen_width

        if player_rect.bottom > 1000:
            game_active = False

        if player_rect.bottom > screen_height:
            reset_values()


    else:
        screen.blit(sky_surface, (0, 0))
        screen.blit(press_surface,press_rectangle)
        screen.blit(score_message,score_message_rect)
        screen.blit(player_res,player_rect1)

        if start_button.draw(screen):
            game_active = True

        if exit_button.draw(screen):
            pygame.quit()
            exit()

    pygame.display.flip()
    pygame.display.update()
    clock.tick(60)