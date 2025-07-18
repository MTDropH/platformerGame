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

# --- Load Images for All Levels ---
def load_images_for_level(level):
    if level == 1:
        return {
            "platform": pygame.transform.scale(pygame.image.load("Jack/images/dirt.png").convert_alpha(), (TILE, TILE)),
            "stone_dirt": pygame.transform.scale(pygame.image.load("Jack/images/stone_dirt.png").convert_alpha(), (TILE, TILE)),
            "flag": pygame.transform.scale(pygame.image.load("Jack/images/flag.png").convert_alpha(), (TILE * 1, TILE * 2)),
            "powerup": pygame.transform.scale(pygame.image.load("Jack/images/armour_power_up.png").convert_alpha(), (TILE, TILE)),
            "bow_powerup": pygame.transform.scale(pygame.image.load("Jack/images/bow_power_up.png").convert_alpha(), (TILE, TILE)),
            "grass": pygame.transform.scale(pygame.image.load("Jack/images/deco_grass.png").convert_alpha(), (TILE, TILE)),
            "stone": pygame.transform.scale(pygame.image.load("Jack/images/deco_stone.png").convert_alpha(), (TILE, TILE)),
        }
    elif level == 2:
        return {
            "platform": pygame.transform.scale(pygame.image.load("Jack/images/level_2_dirt1.png").convert_alpha(), (TILE, TILE)),
            "stone_dirt": pygame.transform.scale(pygame.image.load("Jack/images/level_2_stone_dirt1.png").convert_alpha(), (TILE, TILE)),
            "flag": pygame.transform.scale(pygame.image.load("Jack/images/level_2_flag.png").convert_alpha(), (TILE, TILE * 2)),
            "powerup": pygame.transform.scale(pygame.image.load("Jack/images/armour polish.png").convert_alpha(), (TILE, TILE)),
            "bow_powerup": pygame.transform.scale(pygame.image.load("Jack/images/bow_power_up.png").convert_alpha(), (TILE, TILE)),
            "grass": pygame.transform.scale(pygame.image.load("Jack/images/dark_deco_stone.png").convert_alpha(), (TILE, TILE)),
            "stone": pygame.transform.scale(pygame.image.load("Jack/images/level_2_deco_2.png").convert_alpha(), (TILE, TILE)),
        }
    elif level == 3:
        return {
            "platform": pygame.transform.scale(pygame.image.load("Jack/images/dirt.png").convert_alpha(), (TILE, TILE)),
            "stone_dirt": pygame.transform.scale(pygame.image.load("Jack/images/stone_dirt.png").convert_alpha(), (TILE, TILE)),
            "flag": pygame.transform.scale(pygame.image.load("Jack/images/level_3_flag.png").convert_alpha(), (TILE, TILE * 2)),
            "powerup": pygame.transform.scale(pygame.image.load("Jack/images/armour_power_up.png").convert_alpha(), (TILE, TILE)),
            "bow_powerup": pygame.transform.scale(pygame.image.load("Jack/images/bow_power_up.png").convert_alpha(), (TILE, TILE)),
            "grass": pygame.transform.scale(pygame.image.load("Jack/images/deco_grass.png").convert_alpha(), (TILE, TILE)),
            "stone": pygame.transform.scale(pygame.image.load("Jack/images/level_3_stone.png").convert_alpha(), (TILE, TILE)),
        }

current_level = 1
images = load_images_for_level(current_level)

# --- Editor State ---
tiles = []
decorations = []
enemies = []
slimes = []
powerups = []
boss = None  # Boss data
flag = None
camera_x = 0
mode = 'tile'

def draw_grid():
    for x in range(0, LEVEL_WIDTH, TILE):
        pygame.draw.line(screen, (200, 200, 200), (x - camera_x, 0), (x - camera_x, HEIGHT))
    for y in range(0, HEIGHT, TILE):
        pygame.draw.line(screen, (200, 200, 200), (0, y), (WIDTH, y))

def draw_toolbar():
    modes = ["tile", "stone_dirt", "grass", "stone", "enemy", "slime", "powerup", "bow_powerup", "boss", "flag", "delete"]
    spacing = WIDTH // len(modes)  # Dynamically calculate spacing based on screen width

    for i, m in enumerate(modes):
        color = (255, 255, 0) if m == mode else (255, 255, 255)
        label = font.render(m, True, color)
        label_rect = label.get_rect()
        label_x = spacing * i + (spacing - label_rect.width) // 2
        screen.blit(label, (label_x, 10))

    # Show current level and controls
    level_label = font.render(f"Editing Level {current_level}", True, (255, 255, 255))
    screen.blit(level_label, (10, HEIGHT - 70))
    
    # Show level switching instructions
    switch_label = font.render("Press L to switch levels (1-3)", True, (200, 200, 200))
    screen.blit(switch_label, (10, HEIGHT - 50))
    
    # Show boss info
    boss_info = f"Boss: {'Placed' if boss else 'None'}"
    boss_label = font.render(boss_info, True, (255, 100, 100))
    screen.blit(boss_label, (10, HEIGHT - 30))

def save_level():
    filename = f"Jack/level{current_level}.json"
    data = {
        "tiles": [{"x": t["rect"].x, "y": t["rect"].y, "width": TILE, "height": TILE, "type": t["type"]} for t in tiles],
        "decorations": [{"x": d["x"], "y": d["y"], "width": TILE, "height": TILE, "type": d["type"]} for d in decorations],
        "enemies": [{"x": e["x"], "y": e["y"], "left_bound": e["x"] - 64, "right_bound": e["x"] + 64} for e in enemies],
        "slimes": [{"x": s["x"], "y": s["y"], "left_bound": s["x"] - 64, "right_bound": s["x"] + 64} for s in slimes],
        "powerups": [{"x": p["x"], "y": p["y"], "type": p.get("type", "armor")} for p in powerups],
        "boss": boss if boss else None,  # Save boss data
        "flag": {"x": flag.x if flag else 0, "y": flag.y if flag else 0, "width": TILE, "height": TILE * 2}
    }
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Level {current_level} saved to {filename}")

def clear_level_data():
    global tiles, decorations, enemies, slimes, powerups, boss, flag
    tiles = []
    decorations = []
    enemies = []
    slimes = []
    powerups = []
    boss = None
    flag = None

def load_level():
    global tiles, decorations, enemies, slimes, powerups, boss, flag
    clear_level_data()
    filename = f"Jack/level{current_level}.json"
    try:
        with open(filename, "r") as f:
            data = json.load(f)
        tiles = [{"rect": pygame.Rect(t["x"], t["y"], TILE, TILE), "type": t["type"]} for t in data.get("tiles", [])]
        decorations = data.get("decorations", [])
        enemies = data.get("enemies", [])
        slimes = data.get("slimes", [])
        powerups = [{"x": p["x"], "y": p["y"], "type": p.get("type", "armor")} for p in data.get("powerups", [])]
        boss = data.get("boss", None)  # Load boss data
        f_data = data.get("flag", None)
        if f_data:
            flag = pygame.Rect(f_data["x"], f_data["y"], TILE, TILE * 2)
        print(f"Level {current_level} loaded successfully")
    except FileNotFoundError:
        print(f"No file for level {current_level}, starting fresh.")

def switch_level():
    global current_level, images
    # Cycle through levels 1 -> 2 -> 3 -> 1
    current_level = (current_level % 3) + 1
    images = load_images_for_level(current_level)
    load_level()
    print(f"Switched to Level {current_level}")

load_level()

running = True
while running:
    # Set background color based on level theme
    if current_level == 1:
        screen.fill((135, 206, 235))  # Sky blue for level 1
    elif current_level == 2:
        screen.fill((70, 130, 180))   # Steel blue for level 2
    else:  # Level 3
        screen.fill((135, 206, 235))     # above 
    
    draw_grid()
    draw_toolbar()

    # Draw tiles
    for tile in tiles:
        img = images["platform"] if tile["type"] == "dirt" else images["stone_dirt"]
        screen.blit(img, (tile["rect"].x - camera_x, tile["rect"].y))
    
    # Draw decorations
    for d in decorations:
        img = images["grass"] if d["type"] == "grass" else images["stone"]
        screen.blit(img, (d["x"] - camera_x, d["y"]))
    
    # Draw enemies
    for e in enemies:
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(e["x"] - camera_x, e["y"], TILE, TILE * 2))
        # Draw a simple enemy label
        enemy_label = font.render("E", True, (255, 255, 255))
        screen.blit(enemy_label, (e["x"] - camera_x + 8, e["y"] + 16))
    
    # Draw slimes
    for s in slimes:
        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(s["x"] - camera_x, s["y"], TILE, TILE))
        # Draw a simple slime label
        slime_label = font.render("S", True, (255, 255, 255))
        screen.blit(slime_label, (s["x"] - camera_x + 8, s["y"] + 8))
    
    # Draw boss
    if boss:
        boss_width = boss.get("width", TILE * 3)
        boss_height = boss.get("height", TILE * 3)
        pygame.draw.rect(screen, (128, 0, 128), pygame.Rect(boss["x"] - camera_x, boss["y"], boss_width, boss_height))
        # Draw boss label
        boss_label = font.render("BOSS", True, (255, 255, 255))
        screen.blit(boss_label, (boss["x"] - camera_x + boss_width//4, boss["y"] + boss_height//2))
        
        # Draw health info
        health_text = f"HP: {boss.get('health', 3)}"
        health_label = font.render(health_text, True, (255, 255, 255))
        screen.blit(health_label, (boss["x"] - camera_x + 5, boss["y"] + 5))
    
    # Draw powerups
    for p in powerups:
        if p.get("type") == "bow":
            screen.blit(images["bow_powerup"], (p["x"] - camera_x, p["y"]))
        else:
            screen.blit(images["powerup"], (p["x"] - camera_x, p["y"]))
    
    # Draw flag
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
            if event.key == pygame.K_6: mode = 'slime'
            if event.key == pygame.K_7: mode = 'powerup'
            if event.key == pygame.K_8: mode = 'bow_powerup'
            if event.key == pygame.K_9: mode = 'boss'
            if event.key == pygame.K_F1: mode = 'flag'
            if event.key == pygame.K_0: mode = 'delete'
            if event.key == pygame.K_LEFT:
                camera_x = max(0, camera_x - 64)
            if event.key == pygame.K_RIGHT:
                camera_x = min(LEVEL_WIDTH - WIDTH, camera_x + 64)
            if event.key == pygame.K_l:
                switch_level()
            
            # Boss health adjustment (when boss is selected and placed)
            if boss and mode == 'boss':
                if event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    boss["health"] = min(boss.get("health", 3) + 1, 10)
                    print(f"Boss health increased to {boss['health']}")
                elif event.key == pygame.K_MINUS:
                    boss["health"] = max(boss.get("health", 3) - 1, 1)
                    print(f"Boss health decreased to {boss['health']}")

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            wx = mx + camera_x
            grid_x = wx // TILE * TILE
            grid_y = my // TILE * TILE

            if mode == "delete":
                tiles = [t for t in tiles if not t["rect"].collidepoint(wx, grid_y)]
                decorations = [d for d in decorations if not (d["x"] == grid_x and d["y"] == grid_y)]
                enemies = [e for e in enemies if not (e["x"] == grid_x and e["y"] == grid_y)]
                slimes = [s for s in slimes if not (s["x"] == grid_x and s["y"] == grid_y)]
                powerups = [p for p in powerups if not (p["x"] == grid_x and p["y"] == grid_y)]
                
                # Delete boss if clicked on
                if boss:
                    boss_width = boss.get("width", TILE * 3)
                    boss_height = boss.get("height", TILE * 3)
                    boss_rect = pygame.Rect(boss["x"], boss["y"], boss_width, boss_height)
                    if boss_rect.collidepoint(wx, grid_y):
                        boss = None
                        print("Boss deleted")
                
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
                    elif mode == "slime":
                        slimes.append({"x": grid_x, "y": grid_y})
                    elif mode == "powerup":
                        powerups.append({"x": grid_x, "y": grid_y, "type": "armor"})
                    elif mode == "bow_powerup":
                        powerups.append({"x": grid_x, "y": grid_y, "type": "bow"})
                    elif mode == "boss":
                        # Only allow one boss per level
                        boss = {
                            "x": grid_x,
                            "y": grid_y,
                            "width": TILE * 3,
                            "height": TILE * 3,
                            "health": 3,
                            "type": "boss"
                        }
                        print(f"Boss placed at ({grid_x}, {grid_y}) with {boss['health']} health")
                        print("Use +/- keys to adjust boss health while in boss mode")
                    elif mode == "flag":
                        flag = pygame.Rect(grid_x, grid_y, TILE, TILE * 2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()