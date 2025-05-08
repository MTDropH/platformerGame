"""
Warm‑up tasks
--------------------------------------
☐ 1. Display the player’s score on screen.
☐ 2. Increase the obstacle fall speed every 10 seconds.
☐ 3. Add lives (e.g. start with 3; lose one on collision, then reset player).
☐ 4. Replace the coloured rectangles with sprite images.

Extra:
Add a power‑up that freezes obstacles for 3 seconds.

===============================================================================
"""

import sys
import random
import pygame

# ────────────────── CONSTANTS ────────────────── #
WIDTH, HEIGHT = 800, 450
FPS = 60

PLAYER_W, PLAYER_H = 50, 30
PLAYER_SPEED = 5

OBSTACLE_SIZE = 30
OBSTACLE_SPEED = 3
SPAWN_INTERVAL = 800          # ms between spawns

BG     = (40, 44, 52)
PLAYER = ( 0,150,255)
OBST   = (255, 60, 60)
TEXT   = (240,240,240)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DODGE!")
clock = pygame.time.Clock()
font  = pygame.font.SysFont(None, 24)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_W, PLAYER_H))
        self.image.fill(PLAYER)
        self.rect = self.image.get_rect(midbottom=(WIDTH//2, HEIGHT-10))

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED
        # keep on screen
        self.rect.clamp_ip(screen.get_rect())

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((OBSTACLE_SIZE, OBSTACLE_SIZE))
        self.image.fill(OBST)
        x = random.randint(0, WIDTH - OBSTACLE_SIZE)
        self.rect = self.image.get_rect(topleft=(x, -OBSTACLE_SIZE))

    def update(self):
        self.rect.y += OBSTACLE_SPEED
        if self.rect.top > HEIGHT:
            self.kill()                     # remove if it goes off‑screen

player   = Player()
player_grp = pygame.sprite.GroupSingle(player)
obstacles  = pygame.sprite.Group()

SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_EVENT, SPAWN_INTERVAL)

running = True
while running:
    dt = clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == SPAWN_EVENT:
            obstacles.add(Obstacle())

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        running = False

    player_grp.update(keys)
    obstacles.update()

    if pygame.sprite.spritecollideany(player, obstacles):
        running = False

    screen.fill(BG)
    player_grp.draw(screen)
    obstacles.draw(screen)

    pygame.display.update()

pygame.quit()
sys.exit()
