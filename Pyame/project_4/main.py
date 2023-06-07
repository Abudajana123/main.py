import pygame
from pygame.locals import *
import sys
import random

pygame.init()

width, height = 800, 670

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Space Road')

player = pygame.image.load('resources/rocket.png')
player_rect = player.get_rect(center=(400, 630))

score = 0
score_font = pygame.font.Font(None, 36)
score_font1 = pygame.font.Font(None, 50)

press_text = score_font1.render(f"Press Here To Start!", True, (127, 163, 245))
press_rect = press_text.get_rect(center=(400, 450))

projectile = pygame.image.load('resources/projectile.png')
projectile_rect = None

obstacle = pygame.image.load('resources/astroid.png')
obstacle_rects = []

bg = pygame.image.load('resources/space.jpg')
bg = pygame.transform.scale(bg, (width, height))

rect_speed = 5
projectile_speed = 10
projectile_distance = 500
max_projectiles = 3
projectile_count = 0

scroll_speed = 1
obstacle_spawn_rate = 0.01

def reset_values():
    global score, player_rect, obstacle_rects
    score = 0
    player_rect = player.get_rect(center=(400, 630))
    obstacle_rects = []


game_active = False  # Set initial game_active state to False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if not game_active and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if press_rect.collidepoint(mouse_pos):
                game_active = True
                reset_values()

        if not game_active and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            game_active = True
            reset_values()

    if game_active:
        screen.blit(bg, (0, 0))
        screen.blit(player, player_rect)

        keys = pygame.key.get_pressed()
        if keys[K_UP]:
            player_rect.y -= rect_speed
        if keys[K_DOWN]:
            player_rect.y += rect_speed
        if keys[K_LEFT]:
            player_rect.x -= rect_speed
            if player_rect.right < 0:
                player_rect.x = width
        if keys[K_RIGHT]:
            player_rect.x += rect_speed
            if player_rect.left > width:
                player_rect.x = -player_rect.width

        if keys[K_SPACE] and projectile_rect is None and projectile_count < max_projectiles:
            projectile_rect = projectile.get_rect(midtop=(player_rect.centerx, player_rect.top))
            projectile_count += 1

        if projectile_rect is not None:
            screen.blit(projectile, projectile_rect)
            projectile_rect.y -= projectile_speed

            if projectile_rect.bottom <= 0:
                projectile_rect = None
                projectile_count -= 1

        if random.random() < obstacle_spawn_rate and len(obstacle_rects) < 10:
            obstacle_rect = obstacle.get_rect(midbottom=(random.randint(0, width), 0))
            obstacle_rects.append(obstacle_rect)

        for obstacle_rect in obstacle_rects:
            screen.blit(obstacle, obstacle_rect)
            obstacle_rect.y += scroll_speed

            if obstacle_rect.top > height:
                obstacle_rects.remove(obstacle_rect)

        player_rect.y = max(0, min(height - player_rect.height, player_rect.y))

        for obstacle_rect in obstacle_rects:
            if player_rect.colliderect(obstacle_rect):
                game_active = False

            if projectile_rect is not None and projectile_rect.colliderect(obstacle_rect):
                obstacle_rects.remove(obstacle_rect)
                projectile_rect = None
                projectile_count -= 1
                score += 1

        score_text = score_font.render(f"Score: {score}", True, (127, 163, 245))
        screen.blit(score_text, (400, 10))

    else:
        screen.blit(bg, (0, 0))
        score_text1 = score_font1.render(f"Score: {score}", True, (127, 163, 245))
        score_rect = score_text1.get_rect(center=(400, 350))
        screen.blit(score_text1, score_rect)
        screen.blit(press_text, press_rect)

    pygame.display.flip()