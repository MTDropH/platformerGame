import sys
import pygame

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

platform_img = pygame.transform.scale(
    pygame.image.load("Jack/dirt.png").convert_alpha(), (TILE, TILE)
)
flag_img = pygame.transform.scale(
    pygame.image.load("Jack/Max final run 1.png").convert_alpha(), (TILE, 2 * TILE)
)
sword_img = pygame.transform.scale(
    pygame.image.load("Jack/Max sword.png").convert_alpha(), (TILE, TILE)
)

player_run_frames = [
    pygame.transform.scale(
        pygame.image.load("Jack/Max final run 1.png").convert_alpha(),
        (TILE, int(TILE * 2)),
    ),
    pygame.transform.scale(
        pygame.image.load("Jack/Max final run 2.png").convert_alpha(),
        (TILE, int(TILE * 2)),
    ),
]

player_idle_frames = [
    pygame.transform.scale(
        pygame.image.load("Jack/Max idle 1.png").convert_alpha(),
        (TILE, int(TILE * 2)),
    ),
    pygame.transform.scale(
        pygame.image.load("Jack/Max idle 2.png").convert_alpha(),
        (TILE, int(TILE * 2)),
    ),
]

enemy_frames = player_run_frames

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

        self.sword_active = False
        self.sword_timer = 0.0
        self.SWORD_DURATION = 0.2

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

    def swing_sword(self):
        if not self.sword_active:
            self.sword_active = True
            self.sword_timer = self.SWORD_DURATION

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

    def update_sword(self, dt):
        if self.sword_active:
            self.sword_timer -= dt
            if self.sword_timer <= 0:
                self.sword_active = False

    def get_sword_hitbox(self):
        if not self.sword_active:
            return None
        offset_x = TILE if self.facing_right else -TILE
        return pygame.Rect(
            self.rect.centerx + offset_x - TILE // 2,
            self.rect.centery - TILE // 2,
            TILE,
            TILE,
        )

    def update(self, dt):
        super().update()

        if self.vel.x == 0:
            self.frames = player_idle_frames
            self.animation_speed = 0.07
        else:
            self.frames = player_run_frames
            self.animation_speed = 0.15

        self.animate()

        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)

        self.update_sword(dt)


class Enemy(AnimatedEntity):
    def __init__(self, x, y, left_bound, right_bound):
        super().__init__(x, y, enemy_frames)
        self.left_bound = left_bound
        self.right_bound = right_bound
        self.vel.x = 2

    def update(self, dt=0):
        super().update()
        if self.rect.left <= self.left_bound or self.rect.right >= self.right_bound:
            self.vel.x *= -1


def create_level():
    tiles = [pygame.Rect(x, HEIGHT - TILE, TILE, TILE) for x in range(0, LEVEL_WIDTH, TILE)]

    tiles.extend([
        pygame.Rect(200, HEIGHT - 5 * TILE, TILE, TILE),
        pygame.Rect(500, HEIGHT - 7 * TILE, TILE, TILE),
        pygame.Rect(1000, HEIGHT - 4 * TILE, TILE, TILE),
        pygame.Rect(1350, HEIGHT - 6 * TILE, TILE, TILE),
    ])

    enemies = pygame.sprite.Group(
        Enemy(300, HEIGHT - 2 * TILE, 300, 500),
        Enemy(550, HEIGHT - 8 * TILE - TILE, 500, 650),
        Enemy(1020, HEIGHT - 5 * TILE, 1000, 1200),
    )

    flag = pygame.Rect(LEVEL_WIDTH - 2 * TILE, HEIGHT - 3 * TILE, TILE, 2 * TILE)
    return tiles, enemies, flag


def draw_tiles(surf, tiles, camera_x):
    for rect in tiles:
        for x in range(0, rect.width, TILE):
            surf.blit(platform_img, (rect.x + x - camera_x, rect.y))


def main():
    tiles, enemies, flag = create_level()
    player = Player(64, HEIGHT - 3 * TILE)
    sprites = pygame.sprite.Group(player, *enemies)

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        player.handle_input(keys)
        if keys[pygame.K_z]:
            player.swing_sword()

        player.apply_gravity()
        player.collide(tiles)
        sprites.update(dt)

        sword_hitbox = player.get_sword_hitbox()
        if sword_hitbox:
            for enemy in list(enemies):
                if sword_hitbox.colliderect(enemy.rect):
                    enemies.remove(enemy)
                    sprites.remove(enemy)

        for enemy in enemies:
            if player.rect.colliderect(enemy.rect):
                if player.vel.y > 0 and player.rect.bottom - enemy.rect.top < TILE // 2:
                    enemies.remove(enemy)
                    sprites.remove(enemy)
                    player.vel.y = JUMP_VELOCITY / 1.5
                else:
                    print("Ouch! Respawn…")
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

        screen.blit(flag_img, flag.move(-camera_x, 0))

        if sword_hitbox:
            screen.blit(sword_img, sword_hitbox.move(-camera_x, 0))

        pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()