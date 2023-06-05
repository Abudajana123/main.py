from pygame.locals import *
import pygame
import random
import sys

pygame.init()

width, height = 1100, 500

score = 0

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Simple Pygame Example")

obstacle = pygame.image.load('resources/astroid.png')
obstacle = obstacle.convert_alpha()
obstacle_width, obstacle_height = obstacle.get_size()

clock = pygame.time.Clock()

score_font = pygame.font.Font(None, 36)
score_font1 = pygame.font.Font(None, 50)

score_text = score_font.render(f"Score: {score}", True, (127, 163, 245))
score_rect = score_text.get_rect(center=(550, 10))

score_rect1 = score_text.get_rect(center=(550, 200))

press_text = score_font1.render(f"Press Here To Start!", True, (127, 163, 245))
press_rect = press_text.get_rect(center=(550, 250))

def reset_values():
    global score
    score = 0

def generate_obstacles(num_obstacles, spacing):
    obstacle_rects = []
    collision_rects = []
    x = width

    for _ in range(num_obstacles):
        y = random.randint(0, height - obstacle_height)
        obstacle_rect = pygame.Rect(x, y, obstacle_width, obstacle_height)
        obstacle_rects.append(obstacle_rect)
        collision_rect = pygame.Rect(x + 40, y + 40, obstacle_width - 80, obstacle_height - 80)
        collision_rects.append(collision_rect)
        x -= obstacle_width + spacing

    return obstacle_rects, collision_rects


num_obstacles = 5
spacing = 100
obstacle_rects, collision_rects = generate_obstacles(num_obstacles, spacing)

rect_speed = 5

bg = pygame.image.load('resources/sky.jpg')
bg = pygame.transform.scale(bg, (width, height))

player = pygame.image.load('resources/player.png')
player1 = pygame.transform.scale(player, (player.get_width() * 2, player.get_height() * 2))
player_rect = player.get_rect(center=(60, 300))
player_rect1 = player.get_rect(center=(500, 100))
game_active = True

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
            pygame.quit()
            sys.exit()

    if game_active:

        pygame.mouse.set_visible(False)

        keys = pygame.key.get_pressed()
        if keys[K_UP]:
            player_rect.y -= rect_speed
        if keys[K_DOWN]:
            player_rect.y += rect_speed

        mouse_x, mouse_y = pygame.mouse.get_pos()

        screen.blit(bg, (0, 0))
        screen.blit(player, player_rect)
        screen.blit(score_text, score_rect)

        for i in range(len(obstacle_rects)):
            obstacle_rects[i].x -= rect_speed
            screen.blit(obstacle, obstacle_rects[i].topleft)

            if player_rect.colliderect(collision_rects[i]):
                game_active = False

            if obstacle_rects[i].right < 0:
                obstacle_rects[i].x = width
                obstacle_rects[i].y = random.randint(0, height - obstacle_height)
                score += 1

            if player_rect.x > obstacle_rects[i].right:
                score_text = score_font.render(f"Score: {score}", True, (255, 255, 255))
                score_rect = score_text.get_rect(center=(550, 10))

        player_rect.center = (mouse_x, mouse_y)

        for i in range(len(obstacle_rects)):
            if player_rect.colliderect(obstacle_rects[i]):
                game_active = False

    else:
        screen.blit(bg, (0, 0))
        screen.blit(press_text, press_rect)
        screen.blit(score_text, score_rect1)
        screen.blit(player1,player_rect1)
        pygame.mouse.set_visible(True)

        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            game_active = True
            reset_values()
            obstacle_rects, collision_rects = generate_obstacles(num_obstacles, spacing)

    pygame.display.flip()
    clock.tick(60)