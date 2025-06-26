import sys
import pygame
import json

WIDTH, HEIGHT = 800, 448
FPS = 60
GRAVITY = 0.5
PLAYER_SPEED = 2
JUMP_VELOCITY = -10
TILE = 32
LEVEL_WIDTH = 3392
ENEMY_SPEED = 1 
SKY = (135, 206, 235)
platform_images = {}
decoration_images = {}
enemy_frames = [None, None]  
bow_powerup_img = None

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Max the Knight")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

def load_level_sprites(level_number):
    global background_img, platform_images, decoration_images, powerup_img, enemy_frames, flag_img

    if level_number == 2:
        # Level 2 assets
        flag_img = pygame.transform.scale(
            pygame.image.load("Jack/images/level_2_flag.png").convert_alpha(), (TILE, TILE * 2))

        platform_images["dirt"] = pygame.transform.scale(
            pygame.image.load("Jack/images/level_2_dirt.png").convert_alpha(), (TILE, TILE))
        platform_images["stone_dirt"] = pygame.transform.scale(
            pygame.image.load("Jack/images/level_2_stone_dirt.png").convert_alpha(), (TILE, TILE))

        decoration_images["grass"] = pygame.transform.scale(
            pygame.image.load("Jack/images/level_2_deco_1.png").convert_alpha(), (TILE, TILE))
        decoration_images["stone"] = pygame.transform.scale(
            pygame.image.load("Jack/images/level_2_deco_2.png").convert_alpha(), (TILE, TILE))

        powerup_img = pygame.transform.scale(
            pygame.image.load("Jack/images/armour polish.png").convert_alpha(), (TILE, TILE))

        enemy_frames[0] = pygame.transform.scale(
            pygame.image.load("Jack/images/evil guy run1.png").convert_alpha(), (TILE, TILE * 2))
        enemy_frames[1] = pygame.transform.scale(
            pygame.image.load("Jack/images/evil guy run2.png").convert_alpha(), (TILE, TILE * 2))

        # Load background for level 2 (optional if you have different backgrounds)
        background_img_raw = pygame.image.load("Jack/images/level_2_background.png").convert()
        background_img = pygame.transform.scale(background_img_raw, (
            int(background_img_raw.get_width() * (HEIGHT / background_img_raw.get_height())), HEIGHT))

    else:
        # Level 1 assets
        flag_img = pygame.transform.scale(
            pygame.image.load("Jack/images/flag.png").convert_alpha(), (TILE, TILE * 2))

        platform_images["dirt"] = pygame.transform.scale(
            pygame.image.load("Jack/images/dirt.png").convert_alpha(), (TILE, TILE))
        platform_images["stone_dirt"] = pygame.transform.scale(
            pygame.image.load("Jack/images/stone_dirt.png").convert_alpha(), (TILE, TILE))

        decoration_images["grass"] = pygame.transform.scale(
            pygame.image.load("Jack/images/deco_grass.png").convert_alpha(), (TILE, TILE))
        decoration_images["stone"] = pygame.transform.scale(
            pygame.image.load("Jack/images/deco_stone.png").convert_alpha(), (TILE, TILE))

        powerup_img = pygame.transform.scale(
            pygame.image.load("Jack/images/armour_power_up.png").convert_alpha(), (TILE, TILE))
        
        global bow_powerup_img
        bow_powerup_img = pygame.transform.scale(
            pygame.image.load("Jack/images/bow_power_up.png").convert_alpha(), (TILE, TILE))

        enemy_frames[0] = pygame.transform.scale(
            pygame.image.load("Jack/images/evil guy run1.png").convert_alpha(), (TILE, TILE * 2))
        enemy_frames[1] = pygame.transform.scale(
            pygame.image.load("Jack/images/evil guy run2.png").convert_alpha(), (TILE, TILE * 2))

        # Load background for level 1 (if you want to reload or change it)
        background_img_raw = pygame.image.load("Jack/images/new_background.png").convert()
        background_img = pygame.transform.scale(background_img_raw, (
            int(background_img_raw.get_width() * (HEIGHT / background_img_raw.get_height())), HEIGHT))

# Load background image and scale it to screen height
background_img_raw = pygame.image.load("Jack/images/new_background.png").convert()
background_img = pygame.transform.scale(background_img_raw, (
    int(background_img_raw.get_width() * (HEIGHT / background_img_raw.get_height())), HEIGHT))
background_width = background_img.get_width()
background_scroll_speed = 0.5

pygame.mixer.init()
# --- Load Sound Effects ---
jump_sound = pygame.mixer.Sound("Jack/sounds/jump.mp3")
sword_sound = pygame.mixer.Sound("Jack/sounds/sword_whoosh.mp3")
item_sound = pygame.mixer.Sound("Jack/sounds/item_grab.mp3")
bow_sound = pygame.mixer.Sound("Jack/sounds/bow_shoot.mp3")

# --- Load Music Tracks ---
title_music = "Jack/sounds/title_screen.mp3"
level_music = "Jack/sounds/level_1_music.mp3"
game_over_music = "Jack/sounds/game_over_voice.mp3"


# Load images
platform_images = {
    "dirt": pygame.transform.scale(pygame.image.load("Jack/images/dirt.png").convert_alpha(), (TILE, TILE)),
    "stone_dirt": pygame.transform.scale(pygame.image.load("Jack/images/stone_dirt.png").convert_alpha(), (TILE, TILE)),
}

flag_img = pygame.transform.scale(pygame.image.load("Jack/images/flag.png").convert_alpha(), (TILE, 2 * TILE))
title_img = pygame.image.load("Jack/images/new_title_screen.png").convert_alpha()

# Decoration tile images by type
decoration_images = {
    "grass": pygame.transform.scale(pygame.image.load("Jack/images/deco_grass.png").convert_alpha(), (TILE, TILE)),
    "stone": pygame.transform.scale(pygame.image.load("Jack/images/deco_stone.png").convert_alpha(), (TILE, TILE)),
    # Add more types as needed
}

try:
    game_over_img = pygame.image.load("Jack/images/fixed_game_over.png").convert_alpha()
except:
    game_over_img = None

player_run_frames = [
    pygame.transform.scale(pygame.image.load("Jack/images/Max final run 1.png").convert_alpha(), (TILE, int(TILE * 2))),
    pygame.transform.scale(pygame.image.load("Jack/images/Max final run 2.png").convert_alpha(), (TILE, int(TILE * 2)))
]

player_jump_frame = pygame.transform.scale(pygame.image.load("Jack/images/Max_jump.png").convert_alpha(),(TILE, int(TILE * 2)))

powered_up_jump_frame = pygame.transform.scale(
    pygame.image.load("Jack/images/Max_jump_super.png").convert_alpha(),
    (TILE, int(TILE * 2))
)

player_jump_hurt_frame = pygame.transform.scale(
    pygame.image.load("Jack/images/Max_jump_hurt.png").convert_alpha(),
    (TILE, int(TILE * 2))
)

player_idle_frames = [
    pygame.transform.scale(pygame.image.load("Jack/images/Max idle 1.png").convert_alpha(), (TILE, int(TILE * 2))),
    pygame.transform.scale(pygame.image.load("Jack/images/Max idle 2.png").convert_alpha(), (TILE, int(TILE * 2)))
]

player_attack_frame = pygame.transform.scale(pygame.image.load("Jack/images/Max swing sword1.png").convert_alpha(), (TILE, int(TILE * 2)))
sword_img = pygame.transform.scale(pygame.image.load("Jack/images/sword end.png").convert_alpha(), (32, 32))

player_run_hurt_frames = [
    pygame.transform.scale(pygame.image.load("Jack/images/Max run hurt1.png").convert_alpha(), (TILE, int(TILE * 2))),
    pygame.transform.scale(pygame.image.load("Jack/images/Max run hurt2.png").convert_alpha(), (TILE, int(TILE * 2)))
]

player_idle_hurt_frames = [
    pygame.transform.scale(pygame.image.load("Jack/images/Max idle hurt1.png").convert_alpha(), (TILE, int(TILE * 2))),
    pygame.transform.scale(pygame.image.load("Jack/images/Max idle hurt2.png").convert_alpha(), (TILE, int(TILE * 2)))
]

player_attack_hurt_frame = pygame.transform.scale(pygame.image.load("Jack/images/Max swing sword hurt.png").convert_alpha(), (TILE, int(TILE * 2)))

# Power-up image
powerup_img = pygame.transform.scale(pygame.image.load("Jack/images/armour polish.png").convert_alpha(), (TILE, TILE))

# Powered-up player frames
powered_up_idle_frames = [
    pygame.transform.scale(pygame.image.load("Jack/images/Max idle super1.png").convert_alpha(), (TILE, int(TILE * 2))),
    pygame.transform.scale(pygame.image.load("Jack/images/Max idle super2.png").convert_alpha(), (TILE, int(TILE * 2)))
]

powered_up_run_frames = [
    pygame.transform.scale(pygame.image.load("Jack/images/Max run super1.png").convert_alpha(), (TILE, int(TILE * 2))),
    pygame.transform.scale(pygame.image.load("Jack/images/Max run super2.png").convert_alpha(), (TILE, int(TILE * 2)))
]

powered_up_attack_frame = pygame.transform.scale(pygame.image.load("Jack/images/Max swing sword super.png").convert_alpha(), (TILE, int(TILE * 2)))

# Bow shooting frames
player_shoot_frame = pygame.transform.scale(
    pygame.image.load("Jack/images/Max shoot bow.png").convert_alpha(), (TILE, int(TILE * 2))
)

player_shoot_hurt_frame = pygame.transform.scale(
    pygame.image.load("Jack/images/Max hurt shoot bow.png").convert_alpha(), (TILE, int(TILE * 2))
)

powered_up_shoot_frame = pygame.transform.scale(
    pygame.image.load("Jack/images/Max super shoot bow.png").convert_alpha(), (TILE, int(TILE * 2))
)

enemy_frames = [
    pygame.transform.scale(pygame.image.load("Jack/images/evil guy run1.png").convert_alpha(), (TILE, int(TILE * 2))),
    pygame.transform.scale(pygame.image.load("Jack/images/evil guy run2.png").convert_alpha(), (TILE, int(TILE * 2)))
]
# Load life images
life1_img = pygame.image.load("Jack/images/health bar1.png").convert_alpha()
life2_img = pygame.image.load("Jack/images/health bar2.png").convert_alpha()
life3_img = pygame.image.load("Jack/images/health bar3.png").convert_alpha()

# Scale life images if needed
life1_img = pygame.transform.scale(life1_img, (132, 64))  # adjust size
life2_img = pygame.transform.scale(life2_img, (132, 64))
life3_img = pygame.transform.scale(life3_img, (132, 64))
class AnimatedEntity(pygame.sprite.Sprite):

    def __init__(self, x, y, frames, animation_speed=0.1):
        super().__init__()
        self.frames = frames
        self.image = self.frames[0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vel = pygame.Vector2(0, 0)
        self.animation_speed = animation_speed
        self.frame_index = 0
        self.invincible = False
        self.invincibility_timer = 0
        self.hurt_knockback = pygame.Vector2(0, 0)
        self.arrow_group = pygame.sprite.Group()

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animate()
        self.rect.x += self.vel.x
        self.rect.y += self.vel.y

class Player(AnimatedEntity):
    def __init__(self, x, y):
        super().__init__(x, y, player_idle_frames)
        self.on_ground = False
        self.facing_right = True
        self.is_attacking = False
        self.attack_timer = 0
        self.attack_cooldown = 0.3
        self.lives = 2  # 3: powered up, 2: normal, 1: hurt
        self.has_bow = False
        self.arrow_cooldown = 0.5
        self.arrow_timer = 0

    def animate(self):
        if self.lives == 3:
            run_frames = powered_up_run_frames
            idle_frames = powered_up_idle_frames
            attack_frame = powered_up_attack_frame
        elif self.lives == 2:
            run_frames = player_run_frames
            idle_frames = player_idle_frames
            attack_frame = player_attack_frame
        else:  # lives == 1
            run_frames = player_run_hurt_frames
            idle_frames = player_idle_hurt_frames
            attack_frame = player_attack_hurt_frame

        if self.is_attacking:
            image = attack_frame
        elif self.arrow_timer > 0 and self.has_bow:
            if self.lives == 3:
                image = powered_up_shoot_frame
            elif self.lives == 2:
                image = player_shoot_frame
            else:
                image = player_shoot_hurt_frame
        elif not self.on_ground:
            if self.lives == 3:
                image = powered_up_jump_frame
            elif self.lives == 2:
                image = player_jump_frame
            else:  # lives == 1
                image = player_jump_hurt_frame
        else:
            if self.vel.x == 0:
                self.frames = idle_frames
                self.animation_speed = 0.07
            else:
                self.frames = run_frames
                self.animation_speed = 0.15

            self.frame_index += self.animation_speed
            if self.frame_index >= len(self.frames):
                self.frame_index = 0
            image = self.frames[int(self.frame_index)]

        if not self.facing_right:
            image = pygame.transform.flip(image, True, False)
            
        if self.invincible and int(pygame.time.get_ticks() / 100) % 2 == 0:
            self.image.set_alpha(128)  # Flicker on
        else:
            self.image.set_alpha(255)  # Flicker off / normal

        self.image = image

    def apply_gravity(self):
        self.vel.y += GRAVITY
        if self.vel.y > TILE:
            self.vel.y = TILE

    def handle_input(self, keys):
        self.vel.x = 0
        if keys[pygame.K_LEFT]:
            self.vel.x = -PLAYER_SPEED
            self.facing_right = False
        if keys[pygame.K_RIGHT]:
            self.vel.x = PLAYER_SPEED
            self.facing_right = True
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and self.on_ground:
            self.vel.y = JUMP_VELOCITY
            jump_sound.play()
        if keys[pygame.K_z] and not self.is_attacking:
            self.is_attacking = True
            self.attack_timer = self.attack_cooldown
            sword_sound.play()
        if keys[pygame.K_x] and self.has_bow and self.arrow_timer <= 0:
            direction = 1 if self.facing_right else -1
            # Use sword hitbox logic to set arrow start position
            if self.facing_right:
                arrow_x = self.rect.right
            else:
                arrow_x = self.rect.left - TILE  # spawn to the left of player

            arrow_y = self.rect.centery  # middle of the player's body
            arrow = Arrow(arrow_x, arrow_y, direction)
            self.arrow_group.add(arrow)
            self.arrow_timer = self.arrow_cooldown
            bow_sound.play()

    def collide(self, tiles):
        # 1. Horizontal movement first
        self.rect.x += self.vel.x
        for tile in tiles:
            if self.rect.colliderect(tile):
                if self.vel.x > 0:
                    self.rect.right = tile.left  # Hit wall from left
                elif self.vel.x < 0:
                    self.rect.left = tile.right  # Hit wall from right
                self.vel.x = 0

        # 2. Then vertical movement
        self.rect.y += self.vel.y
        self.on_ground = False
        for tile in tiles:
            if self.rect.colliderect(tile):
                if self.vel.y > 0:
                    self.rect.bottom = tile.top  # Land on tile
                    self.vel.y = 0
                    self.on_ground = True
                elif self.vel.y < 0:
                    self.rect.top = tile.bottom  # Hit head on ceiling
                    self.vel.y = 0

    def get_attack_hitbox(self):
        if self.is_attacking:
            if self.facing_right:
                return pygame.Rect(self.rect.right, self.rect.top, 32, self.rect.height)
            else:
                return pygame.Rect(self.rect.left - 32, self.rect.top, 32, self.rect.height)
        return None

    def update(self):
        if self.is_attacking:
            self.attack_timer -= 1 / FPS
            if self.attack_timer <= 0:
                self.is_attacking = False

        if self.arrow_timer > 0:
            self.arrow_timer -= 1 / FPS

        # Handle invincibility timer
        if self.invincible:
            self.invincibility_timer -= 1 / FPS
            if self.invincibility_timer <= 0:
                self.invincible = False

        # Apply knockback, if any
        if self.hurt_knockback.length_squared() > 0:
            self.vel = self.hurt_knockback
            self.hurt_knockback *= 0.9  # Slow down over time
            if self.hurt_knockback.length() < 0.5:
                self.hurt_knockback = pygame.Vector2(0, 0)

        super().update()  # Continue with animation + position updates

class Enemy(AnimatedEntity):
    def __init__(self, x, y, left_bound, right_bound, chase_range=200):
        super().__init__(x, y, enemy_frames)
        self.left_bound = left_bound
        self.right_bound = right_bound
        self.vel.x = ENEMY_SPEED
        self.chase_range = chase_range
        self.is_chasing = False
        self.on_ground = False

    def collide(self, tiles):
        self.rect.y += self.vel.y
        vertical_hits = [t for t in tiles if self.rect.colliderect(t)]
        self.on_ground = False
        for tile in vertical_hits:
            if self.vel.y > 0:  # Falling down
                self.rect.bottom = tile.top
                self.vel.y = 0
                self.on_ground = True
            elif self.vel.y < 0:  # Moving up (head hit)
                self.rect.top = tile.bottom
                self.vel.y = 0

        self.rect.x += self.vel.x
        horizontal_hits = [t for t in tiles if self.rect.colliderect(t)]
        for tile in horizontal_hits:
            if self.vel.x > 0:  # Moving right
                self.rect.right = tile.left
                self.vel.x = -ENEMY_SPEED  # Reverse direction on collision
            elif self.vel.x < 0:  # Moving left
                self.rect.left = tile.right
                self.vel.x = ENEMY_SPEED  # Reverse direction on collision

    def apply_gravity(self):
        self.vel.y += GRAVITY
        if self.vel.y > TILE:
            self.vel.y = TILE

    def update(self, player=None, tiles=None):
        # Enemy patrols between left_bound and right_bound
        if self.rect.left <= self.left_bound or self.rect.right >= self.right_bound:
            self.vel.x *= -1  # Reverse direction when reaching bounds

        # Flip sprite based on direction
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        frame = self.frames[int(self.frame_index)]

        if self.vel.x > 0:
            self.image = frame
        else:
            self.image = pygame.transform.flip(frame, True, False)

        self.apply_gravity()
        if tiles:
            self.collide(tiles)

        self.rect.x += self.vel.x
        self.rect.y += self.vel.y

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, type="health"):
        super().__init__()
        self.type = type
        if self.type == "bow":
            self.image = bow_powerup_img
        else:
            self.image = powerup_img
        self.rect = self.image.get_rect(topleft=(x, y))

class Arrow(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.image.load("Jack/images/arrow.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (32, 32))  # Match sword tip size
        if direction < 0:
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect(center=(x, y))
        self.vel = direction * 6

    def update(self):
        self.rect.x += self.vel
        if self.rect.right < 0 or self.rect.left > LEVEL_WIDTH:
            self.kill()

def show_title_screen():
    pygame.mixer.music.load(title_music)
    pygame.mixer.music.play(-1)

    original_width, original_height = title_img.get_size()
    quadrupled_title_img = pygame.transform.scale(title_img, (original_width * 4, original_height * 4))
    title_rect = quadrupled_title_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    waiting = True
    while waiting:
        screen.fill((0, 0, 0))
        screen.blit(quadrupled_title_img, title_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Only start on Enter
                    pygame.mixer.music.stop()
                    waiting = False
def show_game_over_screen():
    pygame.mixer.music.stop()
    pygame.mixer.music.load(game_over_music)
    pygame.mixer.music.play()

    waiting = True
    while waiting:
        screen.fill((0, 0, 0))
        if game_over_img:
            img = pygame.transform.scale(game_over_img, (WIDTH, HEIGHT))
            screen.blit(img, (0, 0))
        else:
            game_over_text = font.render("GAME OVER", True, (255, 0, 0))
            restart_text = font.render("Press R to restart or ESC to quit", True, (255, 255, 255))
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 40))
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 10))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True  # Restart
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
    return False

def show_level_complete_screen():
    pygame.mixer.music.load("Jack/sounds/level_complete.mp3")
    pygame.mixer.music.play()

    # Load and scale level complete image
    level_complete_img = pygame.image.load("Jack/images/level_1_complete1.png").convert_alpha()
    level_complete_img = pygame.transform.scale(level_complete_img, (WIDTH, HEIGHT))

    waiting = True
    while waiting:
        screen.fill((0, 0, 0))
        screen.blit(level_complete_img, (0, 0))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                waiting = False

    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                waiting = False

def draw_tiles(surf, tiles, tile_types, camera_x, decorations=None):
    for rect, tile_type in zip(tiles, tile_types):
        image = platform_images.get(tile_type, platform_images["dirt"])  # Default to dirt if missing
        for x in range(0, rect.width, TILE):
            surf.blit(image, (rect.x + x - camera_x, rect.y))

    if decorations:
        for deco in decorations:
            image = decoration_images.get(deco["type"], platform_images["dirt"])
            surf.blit(image, (deco["rect"].x - camera_x, deco["rect"].y))

# Updated function: draw life using images
def draw_lives(surf, lives):
    if lives == 3:
        surf.blit(life3_img, (10, 10))
    elif lives == 2:
        surf.blit(life2_img, (10, 10))
    elif lives == 1:
        surf.blit(life1_img, (10, 10))


def create_level(filename='Jack/level1.json'):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading level file {filename}: {e}")
        sys.exit()

    tiles = []
    tile_types = []
    for tile_data in data["tiles"]:
        rect = pygame.Rect(tile_data["x"], tile_data["y"], tile_data["width"], tile_data["height"])
        tile_type = tile_data.get("type", "dirt")  # Default to "dirt" if type not specified
        tiles.append(rect)
        tile_types.append(tile_type)

    decorations = []
    for deco in data.get("decorations", []):
        rect = pygame.Rect(deco["x"], deco["y"], deco["width"], deco["height"])
        deco_type = deco.get("type", "grass")
        decorations.append({"rect": rect, "type": deco_type})

    enemies = pygame.sprite.Group()
    for enemy_data in data["enemies"]:
        enemy = Enemy(enemy_data["x"], enemy_data["y"], enemy_data["left_bound"], enemy_data["right_bound"])
        enemies.add(enemy)

    flag_data = data["flag"]
    flag = pygame.Rect(flag_data["x"], flag_data["y"], flag_data["width"], flag_data["height"])

    powerups = pygame.sprite.Group()
    for powerup_data in data.get("powerups", []):
        powerup = PowerUp(powerup_data["x"], powerup_data["y"], powerup_data.get("type", "health"))
        powerups.add(powerup)

    return tiles, tile_types, decorations, enemies, flag, powerups


def main(level_number=1):
    if level_number == 1:
        show_title_screen()

    load_level_sprites(level_number)

    if level_number == 2:
        pygame.mixer.music.load("Jack/sounds/level_2_theme.mp3")
    else:
        pygame.mixer.music.load(level_music)

    pygame.mixer.music.play(-1)

    level_file = f'Jack/level{level_number}.json'
    tiles, tile_types, decorations, enemies, flag, powerups = create_level(level_file)

    player = Player(64, HEIGHT - 3 * TILE)


    player.arrow_group = pygame.sprite.Group()

    sprites = pygame.sprite.Group(player, *enemies, *powerups)

    running = True
    while running:
        dt = clock.tick(FPS) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        player.handle_input(keys)
        player.apply_gravity()
        player.collide(tiles)
        player.arrow_group.update()

# --- Death barrier: Player falls below the screen ---
        if player.rect.top > HEIGHT + 100:  # 100 pixels below screen
            player.lives -= 1
            if player.lives <= 0:
                restart = show_game_over_screen()
                if restart:
                    main(level_number=1)  # Restart from level 1
                running = False
                break
            else:
                player.rect.topleft = (64, HEIGHT - 3 * TILE)
                player.vel = pygame.Vector2(0, 0)

        for enemy in enemies:
            enemy.update(player, tiles)
            # Arrow hits enemy
            for arrow in player.arrow_group:
                hit_enemies = pygame.sprite.spritecollide(arrow, enemies, dokill=True)
                if hit_enemies:
                    arrow.kill()
                    for enemy in hit_enemies:
                        sprites.remove(enemy)  # remove enemy from draw/update group

        sprites.update()
        attack_rect = player.get_attack_hitbox()

        if attack_rect:
            for enemy in enemies.copy():
                if attack_rect.colliderect(enemy.rect):
                    enemies.remove(enemy)
                    sprites.remove(enemy)

        for enemy in enemies:
            if player.rect.colliderect(enemy.rect):
                if player.vel.y > 0 and player.rect.bottom - enemy.rect.top < TILE * 0.75:
                    # stomp enemy
                    enemies.remove(enemy)
                    sprites.remove(enemy)
                    player.vel.y = JUMP_VELOCITY / 1.5
                else:
                    if not player.invincible:
                        player.lives -= 1
                        player.invincible = True
                        player.invincibility_timer = 1.0

                        if player.lives <= 0:
                            show_game_over_screen()
                            running = False
                            break

        for powerup in powerups:
            if player.rect.colliderect(powerup.rect):
                powerups.remove(powerup)
                sprites.remove(powerup)
                item_sound.play()
                if powerup.type == "bow":
                    player.has_bow = True
                else:
                    if player.lives < 3:
                        player.lives += 1


        if player.rect.colliderect(flag):
            print("Level complete!")
            show_level_complete_screen()
            main(level_number + 1)  # Load next level
            return

        camera_x = max(0, min(player.rect.centerx - WIDTH // 2, LEVEL_WIDTH - WIDTH))

        # --- DRAW ---
        for x in range(0, WIDTH * 3, background_width):
            screen.blit(background_img, (x - camera_x * background_scroll_speed, 0))

        draw_tiles(screen, tiles, tile_types, camera_x, decorations)
        for sprite in sprites:
            screen.blit(sprite.image, sprite.rect.move(-camera_x, 0))

        if attack_rect:
            sword_pos = (player.rect.right if player.facing_right else player.rect.left - sword_img.get_width(),
                         player.rect.top + 32)
            sword_image = sword_img if player.facing_right else pygame.transform.flip(sword_img, True, False)
            screen.blit(sword_image, (sword_pos[0] - camera_x, sword_pos[1]))

        for arrow in player.arrow_group:
            screen.blit(arrow.image, arrow.rect.move(-camera_x, 0))

        screen.blit(flag_img, flag.move(-camera_x, 0))
        draw_lives(screen, player.lives)

        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main(level_number=1)