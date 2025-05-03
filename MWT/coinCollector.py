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
PLAYER_SPEED = 4
BASE_SPEED = 2
MAX_MISSES = 3

# --- init ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Coin Collector")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# --- load images ---
player_img = pygame.image.load("MWT/alien.png").convert_alpha()
coin_img_orig = pygame.image.load("MWT/coin.png").convert_alpha()
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


# Here!

# import pygame
# import sys

# # --- Setup ---
# WIDTH, HEIGHT = 640, 480
# FPS = 60
# PLAYER_SPEED = 5
# ENEMY_SPEED = 2

# pygame.init()
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("Chase Starter Game")
# clock = pygame.time.Clock()
# font = pygame.font.SysFont(None, 36)

# # --- Colors ---
# WHITE = (255, 255, 255)
# BLACK = (0, 0, 0)
# PLAYER_C = (0, 200, 255)
# ENEMY_C = (255, 0, 0)

# # --- Game Objects ---
# player = pygame.Rect(WIDTH // 2, HEIGHT // 2, 32, 32)
# enemy = pygame.Rect(100, 100, 32, 32)
# score = 0
# start_ticks = pygame.time.get_ticks()
# game_over = False

# # --- Main Loop ---
# running = True
# while running:
#     dt = clock.tick(FPS) / 1000

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     keys = pygame.key.get_pressed()
#     if not game_over:
#         if keys[pygame.K_LEFT]:
#             player.x -= PLAYER_SPEED
#         if keys[pygame.K_RIGHT]:
#             player.x += PLAYER_SPEED
#         if keys[pygame.K_UP]:
#             player.y -= PLAYER_SPEED
#         if keys[pygame.K_DOWN]:
#             player.y += PLAYER_SPEED

#         # Clamp to screen
#         player.clamp_ip(screen.get_rect())

#         # Enemy chases player
#         if enemy.x < player.x:
#             enemy.x += ENEMY_SPEED
#         if enemy.x > player.x:
#             enemy.x -= ENEMY_SPEED
#         if enemy.y < player.y:
#             enemy.y += ENEMY_SPEED
#         if enemy.y > player.y:
#             enemy.y -= ENEMY_SPEED

#         # Collision
#         if player.colliderect(enemy):
#             game_over = True

#         # Score timer
#         score = (pygame.time.get_ticks() - start_ticks) // 1000

#     # --- Draw ---
#     screen.fill(BLACK)
#     pygame.draw.rect(screen, PLAYER_C, player)
#     pygame.draw.rect(screen, ENEMY_C, enemy)
#     screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))

#     if game_over:
#         msg = font.render("Game Over!", True, WHITE)
#         screen.blit(msg, msg.get_rect(center=(WIDTH//2, HEIGHT//2)))

#     pygame.display.flip()

# pygame.quit()
# sys.exit()
