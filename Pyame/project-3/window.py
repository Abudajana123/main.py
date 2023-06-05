import pygame
from sys import exit
from random import randint,choice

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
		player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
		self.player_walk = [player_walk_1,player_walk_2]
		self.player_index = 0
		self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

		self.image = self.player_walk[self.player_index]
		self.rect = self.image.get_rect(midbottom = (80,300))
		self.gravity = 0

		self.jump_sound = pygame.mixer.Sound('audios/audio_jump.mp3')
		self.jump_sound.set_volume(0.5)

	def player_input(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
			self.gravity = -20
			self.jump_sound.play()

	def apply_gravity(self):
		self.gravity += 1
		self.rect.y += self.gravity
		if self.rect.bottom >= 300:
			self.rect.bottom = 300

	def animation_state(self):
		if self.rect.bottom < 300: 
			self.image = self.player_jump
		else:
			self.player_index += 0.1
			if self.player_index >= len(self.player_walk):self.player_index = 0
			self.image = self.player_walk[int(self.player_index)]

	def update(self):
		self.player_input()
		self.apply_gravity()
		self.animation_state()

class obstacle(pygame.sprite.Sprite):
	def __init__(self,type):
		super().__init__()
		
		if type == 'fly':
			fly_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
			fly_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
			self.frames = [fly_1,fly_2]
			y_pos = 210
		else:
			snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
			snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
			self.frames = [snail_1,snail_2]
			y_pos  = 300

		self.animation_index = 0
		self.image = self.frames[self.animation_index]
		self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))

	def animation_state(self):
		self.animation_index += 0.1 
		if self.animation_index >= len(self.frames): self.animation_index = 0
		self.image = self.frames[int(self.animation_index)]

	def update(self):
		self.animation_state()
		self.rect.x -= 6
		self.destroy()

	def destroy(self):
		if self.rect.x <= -100: 
			self.kill()

def display_score():
    current_time = int(pygame.time.get_ticks() /1000- start_time)
    score_surface = test_font.render(f'score: {current_time}',False,'#646464')
    score_rectangle = score_surface.get_rect(center= (400,50))
    screen.blit(score_surface,score_rectangle)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 300: screen.blit(snail_surface,obstacle_rect)
            else: screen.blit(fly_surface,obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else: return []

def collisions(player,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
    return True

def collision_sprite():
	if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
		obstacle_group.empty()
		return False
	else: return True
        
def player_animations():
     global player_surface, player_index

     if player_rectangle.bottom > 300:
         player_surface= player_jump
     else:
         player_index += 0.1
         if player_index >= len(player_walk): player_index = 0 
         player_surface = player_walk[int(player_index)]


pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font\Pixeltype (1).ttf', 50)
game_active = False
start_time=0
score = 0
bg_music = pygame.mixer.Sound('audios/music.wav')
bg_music.play(loops = -1)

player = pygame.sprite.GroupSingle()
player.add(Player())

sky_surface = pygame.image.load('graphics\sky.png').convert_alpha()
ground_surface = pygame.image.load('graphics\ground.png').convert_alpha()
obstacle_group = pygame.sprite.Group()

snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha
snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha
snail_frames = [snail_frame_1,snail_frame_2]
snail_frame_index = 0
snail_surface = snail_frames[snail_frame_index]

fly_frame_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha
fly_frame_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha
fly_frames = [fly_frame_1,fly_frame_2]
fly_frame_index = 0
fly_surface = fly_frames[fly_frame_index]

snail_x_pos = 600

obstacle_rect_list = []

player_walk_1 = pygame.image.load('graphics\player\player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics\player\player_walk_2.png').convert_alpha()
player_jump = pygame.image.load('graphics\player\jump.png')
player_walk = [player_walk_1,player_walk_2]
player_index = 0
player_surface = player_walk[player_index]
player_rectangle = player_walk_1.get_rect(midbottom = (80,300))
player_gravity = 0
#intro screen
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rectangle = player_stand.get_rect(center = (400,200))

game_title_surface = test_font.render('Pixel Runner',False,(111,196,169))
game_title_rectangle = game_title_surface.get_rect(center = (400,70))

press_surface = test_font.render('Press here to Start',False,(111,196,169))
press_rectangle = press_surface.get_rect(center=(400,320))

#Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer,500)

fly_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(fly_animation_timer,200)


while True:
    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if player_rectangle.bottom == 300:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    player_gravity = -20
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active=True
                start_time = pygame.time.get_ticks() / 1000
        
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(obstacle(choice(['fly','snail','snail','snail'])))
                
        if event.type == snail_animation_timer:
            if snail_frame_index == 0: snail_frame_index = 1
            else: snail_frame_index = 0
            snail_surface = snail_frames[snail_frame_index]
        
        if event.type == fly_animation_timer:
            if fly_frame_index == 0: fly_frame_index = 1
            else: fly_frame_index = 0
            fly_surface = fly_frames[fly_frame_index]
    
    
    if game_active:
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))
        #pygame.draw.rect(screen,'#c0e8ec',score_rectangle)
        #pygame.draw.rect(screen,'#c0e8ec',score_rectangle,10,5)
        #screen.blit(score_surface,score_rectangle)
        score = display_score()
        

        #SNAIL
        #snail_rectangle.x -=4
        #if snail_rectangle.right <=0:
            #snail_rectangle.left = 800
        #screen.blit(snail_surface,snail_rectangle)

        #PLAYER
        #player_gravity += 1
        #player_rectangle.y +=player_gravity
        #if player_rectangle.bottom >= 300 :player_rectangle.bottom=300
        #player_animations()
        #screen.blit(player_surface,player_rectangle)
        player.draw(screen)
        player.update()
        obstacle_group.draw(screen)
        obstacle_group.update()
        game_active = collision_sprite()

        #OBSTACLE MOVEMENT
        #obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        #collision
        #game_active = collisions(player_rectangle,obstacle_rect_list)
    else:
        screen.fill((94,129,162))
        screen.blit(player_stand,player_stand_rectangle)
        obstacle_rect_list.clear()
        player_rectangle.midbottom = (80,300)
        player_gravity = 0
        screen.blit(game_title_surface,game_title_rectangle)

        score_message = test_font.render(f'Your score: {score}',False,(111,196,169))
        score_message_rect = score_message.get_rect(center = (400,330))
        if score == 0:
            screen.blit(press_surface,press_rectangle)
        else:
            screen.blit(score_message,score_message_rect)
        
    pygame.display.update()
    clock.tick(60)
