# This week's tasks:
# - Add a backgroung image
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
LEVEL_WIDTH = 1600

SKY      = (0, 0, 201)
GROUND   = (0, 194, 0)
PLAYER_C = (0, 0, 0)
ENEMY_C  = (255, 255, 255)
PLAT_C   = (124, 252, 0)
FLAG_C   = (255, 215, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Platformer Demo")
clock = pygame.time.Clock()


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
        super().__init__(x, y, TILE, int(TILE * 1.5), PLAYER_C)
        self.on_ground = False

    def handle_input(self, keys):
        self.vel.x = 0
        if keys[pygame.K_LEFT]:
            self.vel.x = -PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.vel.x = PLAYER_SPEED
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and self.on_ground:
            self.vel.y = JUMP_VELOCITY

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


class Enemy(Entity):
    def __init__(self, x, y, left_bound, right_bound, colour=ENEMY_C):
        super().__init__(x, y, TILE, TILE, colour)
        self.left_bound = left_bound
        self.right_bound = right_bound
        self.vel.x = 2

    def update(self):
        super().update()
        if self.rect.left <= self.left_bound or self.rect.right >= self.right_bound:
            self.vel.x *= -1


def create_level():
    tiles = []
    for x in range(0, LEVEL_WIDTH, TILE):
        tiles.append(pygame.Rect(x, HEIGHT - TILE, TILE, TILE))

    tiles.append(pygame.Rect(200, HEIGHT - 5*TILE, TILE*3, TILE))
    tiles.append(pygame.Rect(500, HEIGHT - 7*TILE, TILE*2, TILE))
    tiles.append(pygame.Rect(1000, HEIGHT - 4*TILE, TILE*4, TILE))
    tiles.append(pygame.Rect(1350, HEIGHT - 6*TILE, TILE*2, TILE))

    enemies = pygame.sprite.Group()
    enemies.add(Enemy(300, HEIGHT - 2*TILE, 300, 500))
    enemies.add(Enemy(550, HEIGHT - 8*TILE - TILE, 500, 650, (100,100,100)))
    enemies.add(Enemy(890, HEIGHT - 9*TILE, 300, 1200))
    enemies.add(Enemy(1020, HEIGHT - 5*TILE, 1000, 1200))
    enemies.add(Enemy(1020, HEIGHT - 5*TILE, 300, 1500))

    flag = pygame.Rect(LEVEL_WIDTH - 2*TILE, HEIGHT - 3*TILE, TILE, 2*TILE)

    return tiles, enemies, flag

def draw_tiles(surf, tiles, camera_x):
    for rect in tiles:
        shifted_rect = rect.move(-camera_x, 0)
        pygame.draw.rect(surf, PLAT_C, shifted_rect)

onetime = 0
def main():
    global onetime
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
                else:
                    print("Ouch! Respawn...")
                    player.rect.topleft = (64, HEIGHT - 3*TILE)
                    player.vel = pygame.Vector2(0, 0)

        camera_x = max(0, min(player.rect.centerx - WIDTH // 2, LEVEL_WIDTH - WIDTH))

        screen.fill(SKY)
        draw_tiles(screen, tiles, camera_x)
        for sprite in sprites:
            screen.blit(sprite.image, sprite.rect.move(-camera_x, 0))

        if (onetime == 0) and (len(enemies) == 0):
            new_enemy = Enemy(1020, HEIGHT - 5*TILE, 300, 1500)
            new_enemy2 = Enemy(720, HEIGHT - 5*TILE, 200, 900)
            new_enemy3 = Enemy(720, HEIGHT - 7*TILE, 399, 400, (102, 0, 0))
            enemies.add(new_enemy)
            sprites.add(new_enemy)
            enemies.add(new_enemy2)
            sprites.add(new_enemy2)
            enemies.add(new_enemy3)
            sprites.add(new_enemy3)
            onetime = 1
            
        if onetime == 1:
            pygame.draw.rect(screen, FLAG_C, flag.move(-camera_x,-0))
            if player.rect.colliderect(flag):
                print("Level.complete!")
                running = False

        pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
