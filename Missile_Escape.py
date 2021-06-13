import random
import time

import pygame
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Create a class for player


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("C:\\Users\\rahul\\OneDrive\\Desktop\\jet.png").convert()
        # self.surf = pygame.Surface((40,25))
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

    def update(self, press_key):             # Move the sprite based on user key presses
        if press_key[K_UP]:
            self.rect.move_ip(0, -2)             # move_ip = move in place
        if press_key[K_DOWN]:
            self.rect.move_ip(0, 2)
        if press_key[K_LEFT]:
            self.rect.move_ip(-2, 0)
        if press_key[K_RIGHT]:
            self.rect.move_ip(2, 0)
    # To keep Rectangle within the window
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("C:\\Users\\rahul\\OneDrive\\Desktop\\missile.png").convert()
        # self.surf = pygame.Surface((15, 10))
        # self.surf.fill((255, 0, 0))
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(screen_width + 20, screen_width + 100),
                random.randint(0, screen_height),
                )
            )
        self.speed = random.randint(1, 2)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:             # If enemies go out of screen in left
            self.kill()                     # It gets killed


class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("C:\\Users\\rahul\\OneDrive\\Desktop\\cloud.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(screen_width + 20, screen_width + 100),
                random.randint(0, screen_height),
            )
        )

    def update(self):
        self.rect.move_ip(-1, 0)        # Moving cloud based on constant speed
        if self.rect.right < 0:
            self.kill()


pygame.mixer.init()     # Setup for Sounds
pygame.init()
clock = pygame.time.Clock()     # Setup clock for a decent frame rate

screen_width = 800
screen_height = 650
screen = pygame.display.set_mode((screen_width, screen_height))    # Passing tuple/list as arguments

# Creating a custom event to add anew enemy in every 250 milliseconds(4 times a sec)
ADD_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADD_ENEMY, 250)
ADD_CLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADD_CLOUD, 1000)   # Wait for 1000 milli secs before creating a new cloud


player = Player()
clouds = pygame.sprite.Group()
enemies = pygame.sprite.Group()         # Group for collision detection & position updates
all_sprites = pygame.sprite.Group()     # Group for rendering
all_sprites.add(player)

# LOAD & PLAY BackGround music:
pygame.mixer.music.load("C:\\Users\\rahul\\OneDrive\\Desktop\\monkeys-bg.mp3")
pygame.mixer.music.play(loops=-1)       # For looping and never ending

# Load hit sound file:
collision_sound = pygame.mixer.Sound("C:\\Users\\rahul\\OneDrive\\Desktop\\hit-by.WAV")
collision_image = pygame.image.load("C:\\Users\\rahul\\OneDrive\\Desktop\\blast.png").convert()

running = True

while running is True:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False

        elif event.type == ADD_ENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        elif event.type == ADD_CLOUD:
            new_cloud = Cloud()
            clouds.add(new_cloud)           # Adding new_cloud to clouds & all_sprites group
            all_sprites.add(new_cloud)

    # Get the dict of key pressed
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)         # Update user pressing keys

    enemies.update()        # Update Enemy position
    clouds.update()

    screen.fill((135, 206, 250))        # Filling with sky blue

    for entity in all_sprites:                      # Everything in all_sprites will
        screen.blit(entity.surf, entity.rect)       # be drawn with every frame(player or enemy)

    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        collision_sound.play()
        time.sleep(1)

        running = False
    # screen.blit(player.surf, player.rect)   # When player.rect is used on place of surf_centre,
    #                                         # white rectangle moves to top left corner of window
    pygame.display.flip()

# screen.fill((255, 255, 255))        # Filling the screen with white
# surf = pygame.Surface((50, 50))     # Creates a surface of 50*50 size
# surf.fill((0, 0, 0))
# rect = surf.get_rect()              # Calls a rect for the screen

# surf_centre = (
#     (screen_width-surf.get_width())/2,
#     (screen_height-surf.get_height())/2
# )
# screen.blit(surf, surf_centre)    # Draw surf onto screen at centre
# pygame.display.flip()               # Forcing the display on the screen

clock.tick(90)
pygame.quit()
