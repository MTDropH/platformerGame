import pygame
import random

# Initialize Pygame
pygame.init()

# Game Settings
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Create window
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Donkey Kong")

clock = pygame.time.Clock()

# Player settings
player_width, player_height = 40, 60
player_x, player_y = 50, HEIGHT - player_height - 10
TILE = 100
player_run_frames = [
    pygame.transform.scale(pygame.image.load("Hodgehegs/Mario1.png").convert_alpha(), (TILE, int(TILE * 2))),
    pygame.transform.scale(pygame.image.load("Hodgehegs/Mariorun1.png").convert_alpha(), (TILE, int(TILE * 2)))]
player_vel = 5
player_jump = -15
gravity = 1

# Barrel settings
barrel_width, barrel_height = 30, 30
barrel_speed = 4

# Platform list
platforms = [
    pygame.Rect(0, HEIGHT - 20, WIDTH, 20),
    pygame.Rect(100, 500, 600, 20),
    pygame.Rect(0, 400, 600, 20),
    pygame.Rect(100, 300, 600, 20),
    pygame.Rect(0, 200, 600, 20)
]

# Goal
goal = pygame.Rect(WIDTH - 60, 150, 50, 50)

# Game state
barrels = []
is_jumping = False
y_velocity = 0
score = 0

# Player rect
player = pygame.Rect(player_x, player_y, player_width, player_height)

def spawn_barrel():
    barrels.append(pygame.Rect(random.randint(0, WIDTH - barrel_width), 0, barrel_width, barrel_height))

def draw_window():
    win.fill(WHITE)
    pygame.draw.rect(win, RED, player)

    for plat in platforms:
        pygame.draw.rect(win, (0, 0, 255), plat)

    for barrel in barrels:
        pygame.draw.rect(win, (139, 69, 19), barrel)

    pygame.draw.rect(win, (0, 255, 0), goal)

    pygame.display.update()

def handle_collision(player, barrels):
    for barrel in barrels:
        if player.colliderect(barrel):
            return True
    return False

def check_platform_collision(rect, dy):
    rect.y += dy
    for plat in platforms:
        if rect.colliderect(plat):
            rect.y -= dy
            return True
    rect.y -= dy
    return False

# Main loop
running = True
barrel_timer = 0

while running:
    clock.tick(FPS)
    barrel_timer += 1
    if barrel_timer > 120:
        spawn_barrel()
        barrel_timer = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= player_vel
    if keys[pygame.K_RIGHT]:
        player.x += player_vel
    if keys[pygame.K_SPACE] and not is_jumping:
        is_jumping = True
        y_velocity = player_jump

    # Gravity
    y_velocity += gravity
    if not check_platform_collision(player, y_velocity):
        player.y += y_velocity
    else:
        is_jumping = False
        y_velocity = 0

    # Barrel movement
    for barrel in barrels:
        barrel.y += barrel_speed
    barrels = [b for b in barrels if b.y < HEIGHT]

    # Collision check
    if handle_collision(player, barrels):
        print("Game Over!")
        running = False

    # Goal reached
    if player.colliderect(goal):
        print("You Win!")
        running = False

    draw_window()

pygame.quit()
 