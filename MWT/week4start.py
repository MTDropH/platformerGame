"""
🎯 Warm-Up Tasks:
-----------------
1. Change the player color or size
2. Make the obstacle move faster
3. Add a score that increases every jump over an enemy
4. Add a second type of obstacle
5. Add a win condition if you survive 30 seconds

"""

import pygame
import sys

# --- Setup ---
WIDTH, HEIGHT = 640, 480
FPS = 60
GRAVITY = 100
JUMP_VELOCITY = -100
OBSTACLE_SPEED = 100

pygame.init()

pygame.mixer.init()
pygame.mixer.music.load("MWT/sounds/807184__logicmoon__mirrors.wav")
pygame.mixer.music.play(-1)

jump_sound = pygame.mixer.Sound("MWT/sounds/686523__xupr_e3__mixkit-arcade-game-jump-coin-216.wav")


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jump Dodge Starter Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PLAYER_C = (0, 255, 128)
OBSTACLE_C = (255, 0, 0)

# --- Game State ---
player = pygame.Rect(100, HEIGHT - 60, 40, 40)
player_vel_y = 0
on_ground = True

obstacle = pygame.Rect(WIDTH, HEIGHT - 60, 40, 40)
score = 0
start_ticks = pygame.time.get_ticks()
game_over = False

# --- Main Loop ---
running = True
while running:
    dt = clock.tick(FPS) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if not game_over:
        if keys[pygame.K_SPACE] and on_ground:
            player_vel_y = JUMP_VELOCITY
            on_ground = False
            score += 1
            jump_sound.play()

        # Gravity and jump
        player_vel_y += GRAVITY
        player.y += int(player_vel_y)

        # Ground collision
        if player.bottom >= HEIGHT - 20:
            player.bottom = HEIGHT - 20
            player_vel_y = 0
            on_ground = True

        # Obstacle movement
        obstacle.x -= OBSTACLE_SPEED
        if obstacle.right < 0:
            obstacle.left = WIDTH

        # Collision
        if player.colliderect(obstacle):
            game_over = True

    # --- Draw ---
    screen.fill(BLACK)
    pygame.draw.rect(screen, PLAYER_C, player)
    pygame.draw.rect(screen, OBSTACLE_C, obstacle)
    screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))

    if game_over:
        msg = font.render("Game Over!", True, WHITE)
        screen.blit(msg, msg.get_rect(center=(WIDTH//2, HEIGHT//2)))

    pygame.display.flip()

pygame.quit()
sys.exit()
