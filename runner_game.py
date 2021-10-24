import pygame
import sys
from random import randint, choice

class Player(pygame.sprite.Sprite):
    '''Overall class to manage player attributes and resources.'''
    def __init__(self):
        '''Initialises player attributes and loads animation images.'''
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1,player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()


        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (200,300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.wav')
        self.jump_sound.set_volume(0.5)

    def player_input(self):
        '''Makes the player jump if user has pressed the spacebar.'''
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        '''Creates a lookalike gravity affect for the player.'''
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        '''Makes the player image switch back and forth creating an animated effect.'''
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        '''Calls all methods for the Player class.'''
        self.player_input()
        self.apply_gravity()
        self.animation_state()


class Obstacle(pygame.sprite.Sprite):
    '''Overall class to manage obstacle attributes and resources.'''
    def __init__(self,type):
        '''Check whether obstacle is a fly or snail and initialises their attributes and loads images.'''
        super().__init__()

        if type == 'fly':
            fly_frame_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
            fly_frame_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [fly_frame_1,fly_frame_2]
            y_pos = 210
        else:
            snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_frame_1,snail_frame_2]   
            y_pos = 300       

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100), y_pos))
        self.type = type

    def animation_state(self):
        '''Makes the obstacle image switch back and forth creating an animated effect.'''
        if self.type == 'fly':self.animation_index += 0.3
        else:self.animation_index += 0.1

        if self.animation_index >= len(self.frames):self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        '''Calls all methods for the Obstacle class and gets obstacles to move left across the screen.'''
        self.animation_state()
        self.rect.x -= 6
        self.destroy()
    
    def destroy(self):
        '''Deletes obstacle sprite once it has left the screen.'''
        if self.rect.x <= -100:
            self.kill()


def display_score():
    '''Function that gets game time and displays at the top of the screen.'''
    current_time = (pygame.time.get_ticks() // 1000) - start_time
    score_surface = test_font.render(f'{current_time}', False, (64,64,64))
    score_rect = score_surface.get_rect(center=(400,50))
    pygame.draw.rect(screen, '#c0e8ec', score_rect, 10)
    screen.blit(score_surface,score_rect)
    return current_time

def collision_sprite():
    '''Function that checks for collisions between player and obstacles.'''
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
        obstacle_group.empty()
        return False
    else: return True

def intro_screen():
    '''Function that displays intro screen and game over screen depending on game state.'''
    player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
    player_stand = pygame.transform.rotozoom(player_stand,0,2)
    player_stand_rect = player_stand.get_rect(center=(400,200))

    game_title_surface = game_title_font.render('Pixel Runner',True,'#6FC4A9')
    game_title_surface_rect = game_title_surface.get_rect(center=(415,50))

    continue_surface = test_font.render('Press Enter to Continue:', True, '#6FC4A9')
    continue_surface_rect = continue_surface.get_rect(center=(415,350))
    screen.fill((94,129,162))
    screen.blit(player_stand,player_stand_rect)
    screen.blit(game_title_surface,game_title_surface_rect)

    final_score = test_font.render(f'Final Score: {score}',True,'White')
    final_score_rect = final_score.get_rect(center=(405,350))

    if score == 0:
        screen.blit(continue_surface,continue_surface_rect)
    else:
        screen.blit(final_score,final_score_rect)

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Pixel Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_title_font = pygame.font.Font('font/Pixeltype.ttf', 100)
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.set_volume(0.2)
bg_music.play(loops = -1)

# Groups.
player = pygame.sprite.GroupSingle()
player.add(Player())
obstacle_group = pygame.sprite.Group()

# Load background graphics and get their rectangles.
sky_surface = pygame.image.load('graphics/sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

# Timer.
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

# Main game loop.
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly','snail','snail','snail'])))

    if game_active:
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))
        score = display_score()
        player.draw(screen)
        player.update()
        obstacle_group.draw(screen)
        obstacle_group.update()
        #Collisions.
        game_active = collision_sprite()

    else:
        # Game state if the game is no longer active.
        intro_screen()
        # Start game again.
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            game_active = True
            start_time = pygame.time.get_ticks() // 1000

    pygame.display.update()
    clock.tick(60)