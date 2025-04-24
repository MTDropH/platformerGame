import sys
import pygame

# --- constants -----------------------------------------------------
WIDTH, HEIGHT = 800, 448           # 14 x 32‑pixel tiles high (exact multiple of 32)
FPS = 60
GRAVITY = 0.5
PLAYER_SPEED = 4
JUMP_VELOCITY = -10
TILE = 32

# colours (R,G,B)
SKY      = (135, 206, 235)
GROUND   = (160, 82, 45)
PLAYER_C = (255, 0, 0)
ENEMY_C  = (0, 0, 255)
PLAT_C   = (124, 252, 0)

# -------------------------------------------------------------------
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Platformer Demo")
clock = pygame.time.Clock()


class Entity(pygame.sprite.Sprite):
    """Base class for player & enemies"""
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
        if self.vel.y > TILE:   # terminal‑ish velocity clamp
            self.vel.y = TILE

    def collide(self, tiles):
        """Very simple AABB collisions, resolves separately on x & y."""
        # horizontal
        self.rect.x += self.vel.x
        hits = [t for t in tiles if self.rect.colliderect(t)]
        for tile in hits:
            if self.vel.x > 0:
                self.rect.right = tile.left
            elif self.vel.x < 0:
                self.rect.left = tile.right

        # vertical
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
    def __init__(self, x, y, left_bound, right_bound):
        super().__init__(x, y, TILE, TILE, ENEMY_C)
        self.left_bound = left_bound
        self.right_bound = right_bound
        self.vel.x = 2

    def update(self):
        super().update()
        if self.rect.left <= self.left_bound or self.rect.right >= self.right_bound:
            self.vel.x *= -1   # change direction


def create_level():
    """Returns list of rect tiles & enemy sprites for a tiny demo level."""
    tiles = []
    # ground
    for x in range(0, WIDTH, TILE):
        tiles.append(pygame.Rect(x, HEIGHT - TILE, TILE, TILE))

    # floating platforms
    tiles.append(pygame.Rect(200, HEIGHT - 5*TILE, TILE*3, TILE))
    tiles.append(pygame.Rect(500, HEIGHT - 7*TILE, TILE*2, TILE))

    # enemies
    enemies = pygame.sprite.Group()
    enemies.add(Enemy(300, HEIGHT - 2*TILE, 300, 500))
    enemies.add(Enemy(550, HEIGHT - 8*TILE - TILE, 500, 650))

    return tiles, enemies


def draw_tiles(surf, tiles):
    for rect in tiles:
        pygame.draw.rect(surf, PLAT_C, rect)


def main():
    tiles, enemies = create_level()
    player = Player(64, HEIGHT - 3*TILE)

    sprites = pygame.sprite.Group(player, *enemies)

    running = True
    while running:
        dt = clock.tick(FPS) / 1000  # seconds passed – not really used but handy

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        player.handle_input(keys)
        player.apply_gravity()
        player.collide(tiles)

        sprites.update()

        # collision: player with enemies
        if pygame.sprite.spritecollideany(player, enemies):
            print("Ouch! Respawn...")
            player.rect.topleft = (64, HEIGHT - 3*TILE)
            player.vel = pygame.Vector2(0, 0)

        # --- drawing ------------------------------------------------
        screen.fill(SKY)
        draw_tiles(screen, tiles)
        sprites.draw(screen)
        pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
