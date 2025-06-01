import pygame
import json
import sys

pygame.init()

WIDTH, HEIGHT = 800, 448
TILE = 32
LEVEL_WIDTH = 3392
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Level Editor")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)

# Load images
platform_img = pygame.transform.scale(pygame.image.load("Jack/images/dirt.png").convert_alpha(), (TILE, TILE))
flag_img = pygame.transform.scale(pygame.image.load("Jack/images/flag.png").convert_alpha(), (TILE, TILE * 2))
powerup_img = pygame.transform.scale(pygame.image.load("Jack/images/armour polish.png").convert_alpha(), (TILE, TILE))
grass_img = pygame.transform.scale(pygame.image.load("Jack/images/deco_grass.png").convert_alpha(), (TILE, TILE))
stone_img = pygame.transform.scale(pygame.image.load("Jack/images/deco_stone.png").convert_alpha(), (TILE, TILE))

# Data
tiles = []
decorations = []
enemies = []
powerups = []
flag = None

camera_x = 0
mode = 'tile'  # tile, grass, stone, enemy, powerup, flag, delete

def draw_grid():
    for x in range(0, LEVEL_WIDTH, TILE):
        pygame.draw.line(screen, (200, 200, 200), (x - camera_x, 0), (x - camera_x, HEIGHT))
    for y in range(0, HEIGHT, TILE):
        pygame.draw.line(screen, (200, 200, 200), (0, y), (WIDTH, y))

def draw_toolbar():
    modes = ["tile", "grass", "stone", "enemy", "powerup", "flag", "delete"]
    for i, m in enumerate(modes):
        color = (255, 255, 0) if m == mode else (255, 255, 255)
        label = font.render(m, True, color)
        screen.blit(label, (10 + i * 100, HEIGHT - 30))

def save_level(filename='Jack/level1.json'):
    data = {
        "tiles": [{"x": r.x, "y": r.y, "width": r.width, "height": r.height} for r in tiles],
        "decorations": [{"x": d["x"], "y": d["y"], "width": TILE, "height": TILE, "type": d["type"]} for d in decorations],
        "enemies": [{"x": e["x"], "y": e["y"], "left_bound": e["x"] - 64, "right_bound": e["x"] + 64} for e in enemies],
        "powerups": [{"x": p["x"], "y": p["y"]} for p in powerups],
        "flag": {"x": flag.x if flag else 0, "y": flag.y if flag else 0, "width": TILE, "height": TILE * 2}
    }
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    print("Level saved to", filename)

running = True
while running:
    screen.fill((50, 50, 80))
    draw_grid()
    draw_toolbar()

    for rect in tiles:
        screen.blit(platform_img, (rect.x - camera_x, rect.y))
    for d in decorations:
        img = grass_img if d["type"] == "grass" else stone_img
        screen.blit(img, (d["x"] - camera_x, d["y"]))
    for e in enemies:
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(e["x"] - camera_x, e["y"], TILE, TILE * 2))
    for p in powerups:
        screen.blit(powerup_img, (p["x"] - camera_x, p["y"]))
    if flag:
        screen.blit(flag_img, (flag.x - camera_x, flag.y))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                save_level()
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_1:
                mode = 'tile'
            if event.key == pygame.K_2:
                mode = 'grass'
            if event.key == pygame.K_3:
                mode = 'stone'
            if event.key == pygame.K_4:
                mode = 'enemy'
            if event.key == pygame.K_5:
                mode = 'powerup'
            if event.key == pygame.K_6:
                mode = 'flag'
            if event.key == pygame.K_7:
                mode = 'delete'
            if event.key == pygame.K_LEFT:
                camera_x = max(0, camera_x - 64)
            if event.key == pygame.K_RIGHT:
                camera_x = min(LEVEL_WIDTH - WIDTH, camera_x + 64)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            wx = mx + camera_x
            grid_x = wx // TILE * TILE
            grid_y = my // TILE * TILE

            if mode == "delete":
                tiles = [r for r in tiles if not r.collidepoint(wx, grid_y)]
                decorations = [d for d in decorations if not (d["x"] == grid_x and d["y"] == grid_y + 8)]
                enemies = [e for e in enemies if not (e["x"] == grid_x and e["y"] == grid_y)]
                powerups = [p for p in powerups if not (p["x"] == grid_x and p["y"] == grid_y)]
                if flag and flag.collidepoint(wx, grid_y):
                    flag = None
            else:
                if event.button == 1:  # Left click - add
                    if mode == "tile":
                        tiles.append(pygame.Rect(grid_x, grid_y, TILE, TILE))
                    elif mode == "grass":
                        decorations.append({"x": grid_x, "y": grid_y, "type": "grass"})
                    elif mode == "stone":
                        decorations.append({"x": grid_x, "y": grid_y, "type": "stone"})
                    elif mode == "enemy":
                        enemies.append({"x": grid_x, "y": grid_y})
                    elif mode == "powerup":
                        powerups.append({"x": grid_x, "y": grid_y})
                    elif mode == "flag":
                        flag = pygame.Rect(grid_x, grid_y, TILE, TILE * 2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()