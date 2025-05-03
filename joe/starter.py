"""
Warm-Up Tasks:
-----------------
1. Change the player color
2. Make the enemy move faster
3. Add a second enemy that follows you
4. Add a score that goes up every second
5. Add a Game Over message when the enemy touches you

Bonus: Make the player leave a trail (like a snake)
"""


import pygame
import sys

# --- Setup ---
WIDTH, HEIGHT = 640, 480
FPS = 60
PLAYER_SPEED = 5
ENEMY_SPEED = 4
ENIMY2_SPEED =3

score = 0


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chase Starter Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PLAYER_C = (0, 100, 190)
ENEMY_C = (255, 0, 0)

player = pygame.Rect(WIDTH // 2, HEIGHT // 2, 32, 32)
enemy = pygame.Rect(100, 100, 32, 32)
score = 0
start_ticks = pygame.time.get_ticks()

running = True
game_over = False

while running:
    dt = clock.tick(FPS) / 1000
    score +=1
    print(score)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if not game_over:
        if keys[pygame.K_LEFT]:
            player.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            player.x += PLAYER_SPEED
        if keys[pygame.K_UP]:
            player.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN]:
            player.y += PLAYER_SPEED

        player.clamp_ip(screen.get_rect())

        if enemy.x < player.x:
            enemy.x += ENEMY_SPEED
        if enemy.x > player.x:
            enemy.x -= ENEMY_SPEED
        if enemy.y < player.y:
            enemy.y += ENEMY_SPEED
        if enemy.y > player.y:
            enemy.y -= ENEMY_SPEED

        score = (pygame.time.get_ticks() - start_ticks) // 1000

    screen.fill(BLACK)
    pygame.draw.rect(screen, PLAYER_C, player)
    pygame.draw.rect(screen, ENEMY_C, enemy)

    pygame.display.flip()

pygame.quit()
sys.exit()
