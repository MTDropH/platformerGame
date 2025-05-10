import sys
import pygame
import json

WIDTH, HEIGHT = 800, 448
FPS = 60
GRAVITY = 0.5
PLAYER_SPEED = 3
JUMP_VELOCITY = -10
TILE = 32
LEVEL_WIDTH = 1600

SKY = (135, 206, 235)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Max the Knight")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

# Load images
platform_img = pygame.transform.scale(pygame.image.load("Jack/dirt.png").convert_alpha(), (TILE, TILE))
flag_img = pygame.transform.scale(pygame.image.load("Jack/Max final run 1.png").convert_alpha(), (TILE, 2 * TILE))
title_img = pygame.image.load("Jack/max title screen.png").convert_alpha()

# Try loading optional game over screen
try:
    game_over_img = pygame.image.load("Jack/game over.png").convert_alpha()
except:
    game_over_img = None

# Player sprites
player_run_frames = [
    pygame.transform.scale(pygame.image.load("Jack/Max final run 1.png").convert_alpha(), (TILE, int(TILE * 2))),
    pygame.transform.scale(pygame.image.load("Jack/Max final run 2.png").convert_alpha(), (TILE, int(TILE * 2)))
]

player_idle_frames = [
    pygame.transform.scale(pygame.image.load("Jack/Max idle 1.png").convert_alpha(), (TILE, int(TILE * 2))),
    pygame.transform.scale(pygame.image.load("Jack/Max idle 2.png").convert_alpha(), (TILE, int(TILE * 2)))
]

player_attack_frame = pygame.transform.scale(pygame.image.load("Jack/Max swing sword1.png").convert_alpha(), (TILE, int(TILE * 2)))
sword_img = pygame.transform.scale(pygame.image.load("Jack/sword end.png").convert_alpha(), (32, 32))

# Hurt sprites
player_run_hurt_frames = [
    pygame.transform.scale(pygame.image.load("Jack/Max run hurt1.png").convert_alpha(), (TILE, int(TILE * 2))),
    pygame.transform.scale(pygame.image.load("Jack/Max run hurt2.png").convert_alpha(), (TILE, int(TILE * 2)))
]

player_idle_hurt_frames = [
    pygame.transform.scale(pygame.image.load("Jack/Max idle hurt1.png").convert_alpha(), (TILE, int(TILE * 2))),
    pygame.transform.scale(pygame.image.load("Jack/Max idle hurt2.png").convert_alpha(), (TILE, int(TILE * 2)))
]

player_attack_hurt_frame = pygame.transform.scale(pygame.image.load("Jack/Max swing sword hurt.png").convert_alpha(), (TILE, int(TILE * 2)))

enemy_frames = [
    pygame.transform.scale(pygame.image.load("Jack/evil guy run1.png").convert_alpha(), (TILE, int(TILE * 2))),
    pygame.transform.scale(pygame.image.load("Jack/evil guy run2.png").convert_alpha(), (TILE, int(TILE * 2)))
]

class AnimatedEntity(pygame.sprite.Sprite):
    def __init__(self, x, y, frames, animation_speed=0.1):
        super().__init__()
        self.frames = frames
        self.image = self.frames[0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vel = pygame.Vector2(0, 0)
        self.animation_speed = animation_speed
        self.frame_index = 0

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
        self.lives = 2
        self.is_hurt_version = False

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
        if keys[pygame.K_z] and not self.is_attacking:
            self.is_attacking = True
            self.attack_timer = self.attack_cooldown

    def animate(self):
        if self.is_hurt_version:
            run_frames = player_run_hurt_frames
            idle_frames = player_idle_hurt_frames
            attack_frame = player_attack_hurt_frame
        else:
            run_frames = player_run_frames
            idle_frames = player_idle_frames
            attack_frame = player_attack_frame

        if self.is_attacking:
            image = attack_frame
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

        self.image = image

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
        super().update()

class Enemy(AnimatedEntity):
    def __init__(self, x, y, left_bound, right_bound, chase_range=200):
        super().__init__(x, y, enemy_frames)
        self.left_bound = left_bound
        self.right_bound = right_bound
        self.vel.x = 2
        self.chase_range = chase_range
        self.is_chasing = False
        self.on_ground = False

    def apply_gravity(self):
        self.vel.y += GRAVITY
        if self.vel.y > TILE:
            self.vel.y = TILE

    def collide(self, tiles):
        # Vertical collision
        self.rect.y += self.vel.y
        self.on_ground = False
        for tile in tiles:
            if self.rect.colliderect(tile):
                if self.vel.y > 0:
                    self.rect.bottom = tile.top
                    self.vel.y = 0
                    self.on_ground = True
                elif self.vel.y < 0:
                    self.rect.top = tile.bottom
                    self.vel.y = 0

        # Horizontal collision
        self.rect.x += self.vel.x
        for tile in tiles:
            if self.rect.colliderect(tile):
                if self.vel.x > 0:
                    self.rect.right = tile.left
                    self.vel.x *= -1
                elif self.vel.x < 0:
                    self.rect.left = tile.right
                    self.vel.x *= -1

    def update(self, player=None, tiles=None):
        if player:
            distance_to_player = self.rect.centerx - player.rect.centerx
            if abs(distance_to_player) < self.chase_range:
                self.is_chasing = True
            else:
                self.is_chasing = False

            if self.is_chasing:
                self.vel.x = -2 if distance_to_player > 0 else 2
            else:
                if self.rect.left <= self.left_bound or self.rect.right >= self.right_bound:
                    self.vel.x *= -1

        self.apply_gravity()
        if tiles:
            self.collide(tiles)

        super().update()

def show_title_screen():
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
                waiting = False

def show_game_over_screen():
    waiting = True
    while waiting:
        screen.fill((0, 0, 0))
        if game_over_img:
            img = pygame.transform.scale(game_over_img, (WIDTH, HEIGHT))
            screen.blit(img, (0, 0))
        else:
            game_over_text = font.render("GAME OVER", True, (255, 0, 0))
            instruction = font.render("Press any key to exit...", True, (255, 255, 255))
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 40))
            screen.blit(instruction, (WIDTH // 2 - instruction.get_width() // 2, HEIGHT // 2 + 10))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                pygame.quit()
                sys.exit()

def draw_tiles(surf, tiles, camera_x):
    for rect in tiles:
        for x in range(0, rect.width, TILE):
            surf.blit(platform_img, (rect.x + x - camera_x, rect.y))

def draw_lives(surf, lives):
    text = font.render(f"Lives: {lives}", True, (255, 255, 255))
    surf.blit(text, (10, 10))

def create_level():
    with open('Jack/level1.json', 'r') as f:
        data = json.load(f)

    tiles = []
    for tile_data in data["tiles"]:
        rect = pygame.Rect(tile_data["x"], tile_data["y"], tile_data["width"], tile_data["height"])
        tiles.append(rect)

    enemies = pygame.sprite.Group()
    for enemy_data in data["enemies"]:
        enemy = Enemy(enemy_data["x"], enemy_data["y"], enemy_data["left_bound"], enemy_data["right_bound"])
        enemies.add(enemy)

    flag_data = data["flag"]
    flag = pygame.Rect(flag_data["x"], flag_data["y"], flag_data["width"], flag_data["height"])
    return tiles, enemies, flag

def main():
    show_title_screen()

    tiles, enemies, flag = create_level()
    player = Player(64, HEIGHT - 3 * TILE)
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

        for enemy in enemies:
            enemy.update(player, tiles)

        sprites.update()
        attack_rect = player.get_attack_hitbox()

        if attack_rect:
            for enemy in enemies.copy():
                if attack_rect.colliderect(enemy.rect):
                    enemies.remove(enemy)
                    sprites.remove(enemy)

        for enemy in enemies:
            if player.rect.colliderect(enemy.rect):
                if player.vel.y > 0 and player.rect.bottom - enemy.rect.top < TILE // 2:
                    enemies.remove(enemy)
                    sprites.remove(enemy)
                    player.vel.y = JUMP_VELOCITY / 1.5
                else:
                    player.lives -= 1
                    player.is_hurt_version = True
                    if player.lives <= 0:
                        show_game_over_screen()
                        running = False
                    else:
                        player.rect.topleft = (64, HEIGHT - 3 * TILE)
                        player.vel = pygame.Vector2(0, 0)

        if player.rect.colliderect(flag):
            print("Level complete!")
            running = False

        camera_x = max(0, min(player.rect.centerx - WIDTH // 2, LEVEL_WIDTH - WIDTH))
        screen.fill(SKY)
        draw_tiles(screen, tiles, camera_x)
        for sprite in sprites:
            screen.blit(sprite.image, sprite.rect.move(-camera_x, 0))

        if attack_rect:
            sword_pos = (player.rect.right if player.facing_right else player.rect.left - sword_img.get_width(),
                         player.rect.top + 32)
            sword_image = sword_img if player.facing_right else pygame.transform.flip(sword_img, True, False)
            screen.blit(sword_image, (sword_pos[0] - camera_x, sword_pos[1]))

        screen.blit(flag_img, flag.move(-camera_x, 0))
        draw_lives(screen, player.lives)
        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()