# This week's tasks:
# - Add a game over screen
# - Instead of a rectangle, use an image for the player
# - Put an image for the enemies
# - Make the game longer (maybe add a second level?)
# - Add a 'flag' or something else to indicate the end of the level

import sys
import pygame


WIDTH, HEIGHT = 800, 448
FPS = 60
GRAVITY = 0.5
PLAYER_SPEED = 4
JUMP_VELOCITY = -10
TILE = 32
LEVEL_WIDTH = 4800

SKY      = (0, 0, 201)
GROUND   = (0, 194, 0)
PLAYER_C = (0, 0, 0)
ENEMY_C  = (255, 255, 255)
PLAT_C   = (124, 252, 0)
FLAG_C   = (255, 215, 0)

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chaye's Game")
clock = pygame.time.Clock()

background_img_raw = pygame.image.load("Jack/images/new_background.png").convert()
background_img = pygame.transform.scale(background_img_raw, (
    int(background_img_raw.get_width() * (HEIGHT / background_img_raw.get_height())), HEIGHT))
background_width = background_img.get_width()
background_scroll_speed = 0.5

death_sound = pygame.mixer.Sound("caye/thud-sound-effect-319090.mp3")
jump_sound = pygame.mixer.Sound("MWT/sounds/686523__xupr_e3__mixkit-arcade-game-jump-coin-216.wav")

class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, colour):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(colour)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vel = pygame.Vector2(0, 0)

    def update(self):
        self.rect.x += self.vel.x
        self.rect.y += self.vel.y


class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, TILE, int(TILE), PLAYER_C)
        self.on_ground = False
        self.LIVES = 3
        self.image = pygame.image.load("Jack/images/goober1.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))

    def handle_input(self, keys):
        self.vel.x = 0
        if keys[pygame.K_a]:
            self.vel.x = -PLAYER_SPEED
        if keys[pygame.K_d]:
            self.vel.x = PLAYER_SPEED
        if (keys[pygame.K_SPACE] or keys[pygame.K_w]) and self.on_ground:
            self.vel.y = JUMP_VELOCITY
            jump_sound.play()

    def apply_gravity(self):
        self.vel.y += GRAVITY
        if self.vel.y > TILE:
            self.vel.y = TILE

    def collide(self, tiles):
        self.rect.x += self.vel.x
        hits = [t for t in tiles if self.rect.colliderect(t)]
        for tile in hits:
            if self.vel.x > 0:
                self.rect.right = tile.left
            elif self.vel.x < 0:
                self.rect.left = tile.right

        self.rect.y += self.vel.y
        hits = [t for t in tiles if self.rect.colliderect(t)]
        self.on_ground = False
        for tile in hits:
            if self.vel.y > 0:
                self.rect.bottom = tile.top
                self.vel.y = 0
                self.on_ground = True
            elif self.vel.y < 0:
                self.rect.top = tile.bottom
                self.vel.y = 0

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Enemy(Entity):
    def __init__(self, x, y, left_bound, right_bound, colour=ENEMY_C):
        super().__init__(x, y, TILE, TILE, colour)
        self.left_bound = left_bound
        self.right_bound = right_bound
        self.vel.x = 2
        self.image = pygame.image.load("Jack/images/hopper_main1.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))

    def update(self):
        super().update()
        if self.rect.left <= self.left_bound or self.rect.right >= self.right_bound:
            self.vel.x *= -1
            
    def draw(self, surface):
        surface.blit(self.image, self.rect)


import json

def create_level():
    with open('caye/1.json', 'r') as f:
        data = json.load(f)

    tiles = []
    for tile_data in data["tiles"]:
        rect = pygame.Rect(
            tile_data["x"],
            tile_data["y"],
            tile_data["width"],
            tile_data["height"]
        )
        tiles.append(rect)

    enemies = pygame.sprite.Group()
    for enemy_data in data["enemies"]:
        enemy = Enemy(
            enemy_data["x"],
            enemy_data["y"],
            enemy_data["left_bound"],
            enemy_data["right_bound"]
        )
        enemies.add(enemy)

    flag_data = data["flag"]
    flag = pygame.Rect(
        flag_data["x"],
        flag_data["y"],
        flag_data["width"],
        flag_data["height"]
    )

    return tiles, enemies, flag

def draw_tiles(surf, tiles, camera_x):
    original_image = pygame.image.load("Jack/images/level_2_stone_dirt.png").convert_alpha()
    image = pygame.transform.scale(original_image, (TILE, TILE))  # TILE must be predefined

    for rect in tiles:
        shifted_rect = rect.move(-camera_x, 0)
        surf.blit(image, shifted_rect.topleft)

def start_screen():
    font = pygame.font.Font(None, 72)
    text = font.render("Press SPACE to Start", True, (255,255,255))
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))

    waiting = True
    while waiting:
        screen.fill((0,0,0))
        screen.blit(text, text_rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                waiting = False

def game_over_screen():
    game_over_img = pygame.image.load("caye/gameOver.jpeg").convert_alpha()
    game_over_img = pygame.transform.scale(game_over_img, (WIDTH, HEIGHT))
    waiting = True
    while waiting:
        screen.blit(game_over_img, (0,0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key in [pygame.K_ESCAPE, pygame.K_RETURN]:
                waiting = False


onetime = 0
def main():
    global onetime
    start_screen()
    tiles, enemies, flag = create_level()
    player = Player(64, HEIGHT - 3*TILE)
    sprites = pygame.sprite.Group(player, *enemies)

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

        sprites.update()

        for enemy in enemies:
            if player.rect.colliderect(enemy.rect):
                if player.vel.y > 0 and player.rect.bottom - enemy.rect.top < TILE // 2:
                    enemies.remove(enemy)
                    sprites.remove(enemy)
                    player.vel.y = JUMP_VELOCITY / 1.5
                    player.LIVES += 1
                else:
                    print("Ouch! Respawn...")
                    player.rect.topleft = (64, HEIGHT - 3*TILE)
                    player.vel = pygame.Vector2(0, 0)
                    death_sound.play()
                    player.LIVES -= 1
                    if player.LIVES < 1:
                        game_over_screen()
                        running = False

        camera_x = max(0, min(player.rect.centerx - WIDTH // 2, LEVEL_WIDTH - WIDTH))

        # Background
        for x in range(0, WIDTH * 3, background_width):
            screen.blit(background_img, (x - camera_x * background_scroll_speed, 0))
        draw_tiles(screen, tiles, camera_x)

        for sprite in sprites:
            screen.blit(sprite.image, sprite.rect.move(-camera_x, 0))

        if onetime == 0 and len(enemies) == 0:
            # Second wave
            new_enemy = Enemy(1020, HEIGHT - 5*TILE, 300, 1500)
            new_enemy2 = Enemy(720, HEIGHT - 5*TILE, 200, 900)
            new_enemy3 = Enemy(720, HEIGHT - 7*TILE, 399, 400, (102, 0, 0))
            enemies.add(new_enemy, new_enemy2, new_enemy3)
            sprites.add(new_enemy, new_enemy2, new_enemy3)
            onetime = 1

        if onetime == 1:
            pygame.draw.rect(screen, FLAG_C, flag.move(-camera_x,0))
            if player.rect.colliderect(flag):
                print("Level complete!")
                running = False

        # Draw Lives
        font = pygame.font.Font(None, 36)
        lives_text = font.render(f"Lives: {player.LIVES}", True, (255,255,255))
        screen.blit(lives_text, (10,10))

        pygame.display.update()

    pygame.quit()

    sys.exit()

if __name__ == "__main__":
    main()
