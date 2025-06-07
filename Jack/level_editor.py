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

# --- Load Level 1 + Level 2 Images ---
def load_images_for_level(level):
    if level == 1:
        return {
            "platform": pygame.transform.scale(pygame.image.load("Jack/images/dirt.png").convert_alpha(), (TILE, TILE)),
            "stone_dirt": pygame.transform.scale(pygame.image.load("Jack/images/stone_dirt.png").convert_alpha(), (TILE, TILE)),
            "flag": pygame.transform.scale(pygame.image.load("Jack/images/flag.png").convert_alpha(), (TILE * 1, TILE * 2)),
            "powerup": pygame.transform.scale(pygame.image.load("Jack/images/armour polish.png").convert_alpha(), (TILE, TILE)),
            "bow_powerup": pygame.transform.scale(pygame.image.load("Jack/images/bow_power_up.png").convert_alpha(), (TILE, TILE)),
            "grass": pygame.transform.scale(pygame.image.load("Jack/images/deco_grass.png").convert_alpha(), (TILE, TILE)),
            "stone": pygame.transform.scale(pygame.image.load("Jack/images/deco_stone.png").convert_alpha(), (TILE, TILE)),
        }
    elif level == 2:
        return {
            "platform": pygame.transform.scale(pygame.image.load("Jack/images/level_2_dirt.png").convert_alpha(), (TILE, TILE)),
            "stone_dirt": pygame.transform.scale(pygame.image.load("Jack/images/level_2_stone_dirt.png").convert_alpha(), (TILE, TILE)),
            "flag": pygame.transform.scale(pygame.image.load("Jack/images/level_2_flag.png").convert_alpha(), (TILE, TILE * 2)),
            "powerup": pygame.transform.scale(pygame.image.load("Jack/images/armour polish.png").convert_alpha(), (TILE, TILE)),
            "bow_powerup": pygame.transform.scale(pygame.image.load("Jack/images/bow_power_up.png").convert_alpha(), (TILE, TILE)),
            "grass": pygame.transform.scale(pygame.image.load("Jack/images/level_2_deco_1.png").convert_alpha(), (TILE, TILE)),
            "stone": pygame.transform.scale(pygame.image.load("Jack/images/level_2_deco_2.png").convert_alpha(), (TILE, TILE)),
        }

current_level = 1
images = load_images_for_level(current_level)

# --- Editor State ---
tiles = []
decorations = []
enemies = []
powerups = []
flag = None
camera_x = 0
mode = 'tile'

def draw_grid():
    for x in range(0, LEVEL_WIDTH, TILE):
        pygame.draw.line(screen, (200, 200, 200), (x - camera_x, 0), (x - camera_x, HEIGHT))
    for y in range(0, HEIGHT, TILE):
        pygame.draw.line(screen, (200, 200, 200), (0, y), (WIDTH, y))

def draw_toolbar():
    modes = ["tile", "stone_dirt", "grass", "stone", "enemy", "powerup", "bow_powerup", "flag", "delete"]
    spacing = WIDTH // len(modes)  # Dynamically calculate spacing based on screen width

    for i, m in enumerate(modes):
        color = (255, 255, 0) if m == mode else (255, 255, 255)
        label = font.render(m, True, color)
        label_rect = label.get_rect()
        label_x = spacing * i + (spacing - label_rect.width) // 2
        screen.blit(label, (label_x, 10))

    # Show current level
    level_label = font.render(f"Editing Level {current_level}", True, (255, 255, 255))
    screen.blit(level_label, (10, HEIGHT - 30))

    # Show current level
    level_label = font.render(f"Editing Level {current_level}", True, (255, 255, 255))
    screen.blit(level_label, (10, HEIGHT - 30))

def save_level():
    filename = f"Jack/level{current_level}.json"
    data = {
        "tiles": [{"x": t["rect"].x, "y": t["rect"].y, "width": TILE, "height": TILE, "type": t["type"]} for t in tiles],
        "decorations": [{"x": d["x"], "y": d["y"], "width": TILE, "height": TILE, "type": d["type"]} for d in decorations],
        "enemies": [{"x": e["x"], "y": e["y"], "left_bound": e["x"] - 64, "right_bound": e["x"] + 64} for e in enemies],
        "powerups": [{"x": p["x"], "y": p["y"], "type": p.get("type", "armor")} for p in powerups],
        "flag": {"x": flag.x if flag else 0, "y": flag.y if flag else 0, "width": TILE, "height": TILE * 2}
    }
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    print("Level saved to", filename)

def clear_level_data():
    global tiles, decorations, enemies, powerups, flag
    tiles = []
    decorations = []
    enemies = []
    powerups = []
    flag = None

def load_level():
    global tiles, decorations, enemies, powerups, flag
    clear_level_data()
    filename = f"Jack/level{current_level}.json"
    try:
        with open(filename, "r") as f:
            data = json.load(f)
        tiles = [{"rect": pygame.Rect(t["x"], t["y"], TILE, TILE), "type": t["type"]} for t in data.get("tiles", [])]
        decorations = data.get("decorations", [])
        enemies = data.get("enemies", [])
        powerups = [{"x": p["x"], "y": p["y"], "type": p.get("type", "armor")} for p in data.get("powerups", [])]
        f_data = data.get("flag", None)
        if f_data:
            flag = pygame.Rect(f_data["x"], f_data["y"], TILE, TILE * 2)
    except FileNotFoundError:
        print(f"No file for level {current_level}, starting fresh.")

load_level()

running = True
while running:
    screen.fill((50, 50, 80))
    draw_grid()
    draw_toolbar()

    for tile in tiles:
        img = images["platform"] if tile["type"] == "dirt" else images["stone_dirt"]
        screen.blit(img, (tile["rect"].x - camera_x, tile["rect"].y))
    for d in decorations:
        img = images["grass"] if d["type"] == "grass" else images["stone"]
        screen.blit(img, (d["x"] - camera_x, d["y"]))
    for e in enemies:
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(e["x"] - camera_x, e["y"], TILE, TILE * 2))
    for p in powerups:
        if p.get("type") == "bow":
            screen.blit(images["bow_powerup"], (p["x"] - camera_x, p["y"]))
        else:
            screen.blit(images["powerup"], (p["x"] - camera_x, p["y"]))
    if flag:
        screen.blit(images["flag"], (flag.x - camera_x, flag.y))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                save_level()
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_1: mode = 'tile'
            if event.key == pygame.K_2: mode = 'stone_dirt'
            if event.key == pygame.K_3: mode = 'grass'
            if event.key == pygame.K_4: mode = 'stone'
            if event.key == pygame.K_5: mode = 'enemy'
            if event.key == pygame.K_6: mode = 'powerup'
            if event.key == pygame.K_7: mode = 'bow_powerup'
            if event.key == pygame.K_8: mode = 'flag'
            if event.key == pygame.K_9: mode = 'delete'
            if event.key == pygame.K_LEFT:
                camera_x = max(0, camera_x - 64)
            if event.key == pygame.K_RIGHT:
                camera_x = min(LEVEL_WIDTH - WIDTH, camera_x + 64)
            if event.key == pygame.K_l:
                current_level = 2 if current_level == 1 else 1
                images = load_images_for_level(current_level)
                load_level()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            wx = mx + camera_x
            grid_x = wx // TILE * TILE
            grid_y = my // TILE * TILE

            if mode == "delete":
                tiles = [t for t in tiles if not t["rect"].collidepoint(wx, grid_y)]
                decorations = [d for d in decorations if not (d["x"] == grid_x and d["y"] == grid_y)]
                enemies = [e for e in enemies if not (e["x"] == grid_x and e["y"] == grid_y)]
                powerups = [p for p in powerups if not (p["x"] == grid_x and p["y"] == grid_y)]
                if flag and flag.collidepoint(wx, grid_y):
                    flag = None
            else:
                if event.button == 1:
                    if mode in ["tile", "stone_dirt"]:
                        tile_type = "dirt" if mode == "tile" else "stone_dirt"
                        tiles.append({
                            "rect": pygame.Rect(grid_x, grid_y, TILE, TILE),
                            "type": tile_type
                        })
                    elif mode == "grass":
                        decorations.append({"x": grid_x, "y": grid_y, "type": "grass"})
                    elif mode == "stone":
                        decorations.append({"x": grid_x, "y": grid_y, "type": "stone"})
                    elif mode == "enemy":
                        enemies.append({"x": grid_x, "y": grid_y})
                    elif mode == "powerup":
                        powerups.append({"x": grid_x, "y": grid_y, "type": "armor"})
                    elif mode == "bow_powerup":
                        powerups.append({"x": grid_x, "y": grid_y, "type": "bow"})
                    elif mode == "flag":
                        flag = pygame.Rect(grid_x, grid_y, TILE, TILE * 2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()