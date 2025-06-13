"""
Remember: `pip install pygame`

Starter tasks:
- Change the image from an alien to something else
- Change the background color
- Increase the speed of the player

Extra: For each increase of 5 points the player gets, the coins should fall faster, and the player's controls should flip!
"""

import pygame
import random
import sys

# --- constants ---
WIDTH, HEIGHT = 400, 600
FPS = 60
PLAYER_SPEED = 6
BASE_SPEED = 2
MAX_MISSES = 3

# --- init ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Coin Collector")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# --- load images ---
player_img_orig = pygame.image.load("Jack/images/dirt.png").convert_alpha()
coin_img_orig = pygame.image.load("MWT/coin.png").convert_alpha()
player_img = pygame.transform.scale(player_img_orig, (150, 150))
coin_img = pygame.transform.scale(coin_img_orig, (50, 50))

# --- game state ---
player = player_img.get_rect(midbottom=(WIDTH // 2, HEIGHT - 10))
coin = coin_img.get_rect(center=(random.randint(40, WIDTH - 40), -50))

score = 0
missed = 0

# --- game loop ---
running = True
while running:
    dt = clock.tick(FPS) / 1000  # Time in seconds since last frame

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT]:
        player.x += PLAYER_SPEED
    player.x = max(0, min(player.x, WIDTH - player.width))

    if missed < MAX_MISSES:
        speed = BASE_SPEED + score // 5
        coin.y += speed

        if coin.y > HEIGHT + 40:
            missed += 1
            coin.center = (random.randint(40, WIDTH - 40), -50)

        if player.colliderect(coin):
            score += 1
            coin.center = (random.randint(40, WIDTH - 40), -50)

    # --- draw ---
    screen.fill((30, 144, 255))
    screen.blit(player_img, player)
    screen.blit(coin_img, coin)

    score_surf = font.render(f"Score: {score}", True, (255, 255, 255))
    missed_surf = font.render(f"Missed: {missed}", True, (255, 255, 0))
    screen.blit(score_surf, (10, 10))
    screen.blit(missed_surf, (10, 50))

    if missed >= MAX_MISSES:
        over_surf = font.render("Game Over!", True, (255, 0, 0))
        screen.blit(over_surf, over_surf.get_rect(center=(WIDTH//2, HEIGHT//2)))

    pygame.display.flip()

pygame.quit()
sys.exit()