import sys
import pygame

pygame.mixer.init()
pygame.mixer.music.load("Jack/sounds/8bit-sample-69080.mp3")
pygame.mixer.music.play(-1)

jump_sound = pygame.mixer.Sound("Jack/sounds/sword_whoosh.mp3")
 
WIDTH, HEIGHT = 800, 448
FPS = 60
GRAVITY = 0.5
PLAYER_SPEED = 4
JUMP_VELOCITY = -10
TILE = 32
LEVEL_WIDTH = 4096

SKY      = (135, 206, 235)
GROUND   = (160, 82, 45)
PLAYER_C = (255, 0, 0)
ENEMY_C  = (0, 0, 255)
PLAT_C   = (124, 252, 0)
FLAG_C   = (255, 215, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Running Man")
clock = pygame.time.Clock()

background_img_raw = pygame.image.load("joe/images/streetbackround.jpg").convert()
background_img = pygame.transform.scale(background_img_raw, (
    int(background_img_raw.get_width() * (HEIGHT / background_img_raw.get_height())), HEIGHT))
background_width = background_img.get_width()
background_scroll_speed = 0.5

idle_images = [
    pygame.transform.scale(pygame.image.load('joe/images/idle1RM.png').convert_alpha(), (TILE, int(TILE * 3))),
    pygame.transform.scale(pygame.image.load('joe/images/idle2RM.png').convert_alpha(), (TILE, int(TILE * 3)))
]

run_images = [
    pygame.transform.scale(pygame.image.load('joe/images/running1RM.png').convert_alpha(), (TILE, int(TILE * 3))),
    pygame.transform.scale(pygame.image.load('joe/images/running2RM.png').convert_alpha(), (TILE, int(TILE * 3)))
]

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
        super().__init__(x, y, int(TILE*1.4), int(TILE * 1.2), PLAYER_C)
        self.idle_images = idle_images
        self.run_images = run_images
        self.current_images = self.idle_images
        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speed = 0.1  # Controls how fast the animation flips

        self.image = self.idle_images[0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.on_ground = False

    def handle_input(self, keys):
        self.vel.x = 0
        if keys[pygame.K_LEFT]:
            self.vel.x = -PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.vel.x = PLAYER_SPEED
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and self.on_ground:
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

    def update(self):
        # Choose which animation to use
        if self.vel.x != 0:
            self.current_images = self.run_images
        else:
            self.current_images = self.idle_images

        # Update animation frame
        self.animation_timer += self.animation_speed
        if self.animation_timer >= 1:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.current_images)

        self.image = self.current_images[self.frame_index]
        self.rect = self.image.get_rect(topleft=self.rect.topleft)

        super().update()
        
enemy_images_right = [
    pygame.transform.scale(pygame.image.load('joe/images/badGuy1.png').convert_alpha(), (TILE, TILE*1.5)),
    pygame.transform.scale(pygame.image.load('joe/images/badGuy2.png').convert_alpha(), (TILE, TILE*1.5))
]

enemy_images_left = [
    pygame.transform.flip(img, True, False) for img in enemy_images_right
]

class Enemy(Entity):
    def __init__(self, x, y, left_bound, right_bound):
        super().__init__(x, y, TILE, TILE, ENEMY_C)
        self.left_bound = left_bound
        self.right_bound = right_bound
        self.vel.x = 2  # Start moving right

        self.images_right = enemy_images_right
        self.images_left = enemy_images_left
        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speed = 0.15

        self.image = self.images_right[0]
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        super().update()

        # Reverse direction on bounds
        if self.rect.left <= self.left_bound or self.rect.right >= self.right_bound:
            self.vel.x *= -1

        # Choose image set based on direction
        images = self.images_right if self.vel.x > 0 else self.images_left

        # Animate
        self.animation_timer += self.animation_speed
        if self.animation_timer >= 1:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(images)

        self.image = images[self.frame_index]
        self.rect = self.image.get_rect(topleft=self.rect.topleft)

import json

def create_level():
    with open('joe/mario.json', 'r') as f:
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

tile_image = pygame.image.load('joe/images/streetjumpblocks.jpg').convert_alpha()
tile_image = pygame.transform.scale(tile_image, (32, 32))

def draw_tiles(surf, tiles, camera_x, tile_image=tile_image):
    for rect in tiles:
        shifted_rect = rect.move(-camera_x, 0)
        surf.blit(tile_image, shifted_rect)

# if player.rect.top > HEIGHT + 100:  # 100 pixels below screen
#     player.lives -= 1
#     if player.lives <= 0:
#         restart = show_game_over_screen()
#         if restart:
#             main(level_number=1)  # Restart from level 1
#         running = False
#     else:
#         player.rect.topleft = (64, HEIGHT - 3 * TILE)
#         player.vel = pygame.Vector2(0, 0)


def main():
    tiles, enemies, flag = create_level()
    player = Player(64, HEIGHT - 5*TILE)
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
                else:
                    print("Ouch! Respawn...")
                    player.rect.topleft = (64, HEIGHT - 3*TILE)
                    player.vel = pygame.Vector2(0, 0)

        # End condition
        if player.rect.colliderect(flag):
            print("Level complete!")
            
            running = False

        camera_x = max(0, min(player.rect.centerx - WIDTH // 2, LEVEL_WIDTH - WIDTH))

        for x in range(0, WIDTH * 3, background_width):
            screen.blit(background_img, (x - camera_x * background_scroll_speed, 0))
            
        draw_tiles(screen, tiles, camera_x)
        for sprite in sprites:
            screen.blit(sprite.image, sprite.rect.move(-camera_x, 0))

        pygame.draw.rect(screen, FLAG_C, flag.move(-camera_x, 0))

        pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
