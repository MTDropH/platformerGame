
import sys
import random
import pygame
import os

def clear_screen():
    # Clear the screen for Windows or Unix
    os.system('cls' if os.name == 'nt' else 'clear')

def splash_screen():
    print("===================================")
    print("       WELCOME TO MY GAME!")
    print("     Press Enter to Start...")
    print("===================================")
    input()  # Wait for Enter key

def start_page():
    clear_screen()
    print("===================================")
    print("            START PAGE             ")
    print("  1. Start New Game")
    print("  2. Load Game")
    print("  3. Options")
    print("  4. Quit")
    print("===================================")

# Run the splash screen, then the start page
splash_screen()
start_page()

pygame.mixer.init()
pygame.mixer.music.load("Hodgehegs/Sounds/sad-violin_FtcVu13.mp3")
pygame.mixer.music.play(-1)
pygame.init()

WIDTH, HEIGHT = 800, 800
FPS            = 60

SKY            = (255, 255, 255)
BLUE           = (0, 0, 255)
BROWN          = (139, 69, 19)
GREEN          = (0, 255, 0)
GRAVITY        = 0.6
PLAYER_SPEED   = 5
JUMP_VELOCITY  = -9
TILE           = 32   
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Donkey King")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Century Gothic", 24)

pygame.mixer.init()
pygame.mixer.music.load("Hodgehegs/Sounds/doingdamage.mp3")
pygame.mixer.music.play(-1)

clock = pygame.time.Clock()
win   = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Donkey Kong")

def load(path, w, h):
    return pygame.transform.scale(pygame.image.load(path).convert_alpha(), (w, h))

title_screen = load("Hodgehegs/Images/dk.webp", WIDTH, HEIGHT)
death_screen = load("Hodgehegs/Images/dk_gameover.webp", WIDTH, HEIGHT)

game_image = load("Hodgehegs/Images/bigboy.jpg", WIDTH, HEIGHT)
player_run_frames  = [
    load("Hodgehegs/Images/Mario1.png",  TILE, TILE * 2),
    load("Hodgehegs/Images/Mariorun1.png",  TILE, TILE * 2),
]
player_idle_frames = [
    load("Hodgehegs/Images/Mario1.png",       TILE, TILE * 2),]

donkey_kong_run_frames = [
    load("Hodgehegs/Images/Donkey_kong_barrel.png",TILE*2, TILE * 3),
    load("Hodgehegs/Images/Donkey_kong.png",TILE*2, TILE * 3)
    ]

donkey_kong_idle_frames = [
    load("Hodgehegs/Images/Donkey_kong.png",TILE, TILE * 3),]


class AnimatedEntity(pygame.sprite.Sprite):
    def __init__(self, x, y, frames, animation_speed=0.1):
        super().__init__()
        self.frames = frames
        self.frame_index = 0
        self.animation_speed = animation_speed
        self.image = self.frames[0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vel  = pygame.Vector2(0, 0)

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
        super().__init__(x, y, player_idle_frames, animation_speed=0.07)
        self.on_ground    = False
        self.facing_right = True

    # ── controls ─────────────────
    def handle_input(self, keys):
        self.vel.x = 0
        if keys[pygame.K_LEFT]:
            self.vel.x = -PLAYER_SPEED
            self.facing_right = False
        if keys[pygame.K_RIGHT]:
            self.vel.x =  PLAYER_SPEED
            self.facing_right = True
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and self.on_ground:
            self.vel.y = JUMP_VELOCITY

    # ── animation selection ──────
    def animate(self):
        self.frames         = player_run_frames if self.vel.x else player_idle_frames
        self.animation_speed = 0.15 if self.vel.x else 0.07

        super().animate()                           # advance frame
        if not self.facing_right:                   # mirror if needed
            self.image = pygame.transform.flip(self.image, True, False)

    # ── physics helpers ──────────
    def apply_gravity(self):
        self.vel.y += GRAVITY
        if self.vel.y > TILE:           # clamp fall‑speed
            self.vel.y = TILE

    def collide(self, platforms):
        # horizontal sweep
        self.rect.x += self.vel.x
        hits = [p for p in platforms if self.rect.colliderect(p)]
        for p in hits:
            if self.vel.x > 0:  self.rect.right = p.left
            if self.vel.x < 0:  self.rect.left  = p.right

        # vertical sweep
        self.rect.y += self.vel.y
        hits = [p for p in platforms if self.rect.colliderect(p)]
        self.on_ground = False
        for p in hits:
            if self.vel.y > 0:          # falling
                self.rect.bottom = p.top
                self.vel.y = 0
                self.on_ground = True
            elif self.vel.y < 0:        # hitting head
                self.rect.top = p.bottom
                self.vel.y = 0

platforms = [
    pygame.Rect(   0, HEIGHT -  20, WIDTH, 20),
    
    pygame.Rect( 100, 650, 600, 20),
    pygame.Rect(   0, 550, 600, 20),
    pygame.Rect(   100, 400, 600, 20),
    pygame.Rect(   0, 250, 600, 20),
    pygame.Rect( 100, 100, 600, 20),
    pygame.Rect(   0, -200, 600, 20),
    ]
goal = pygame.Rect(WIDTH - 60, 150, 50, 50)

BARREL_SIZE  = 30
BARREL_SPEED = 4
barrels = []

def spawn_barrel():
    x = random.randint(0, WIDTH - BARREL_SIZE)
    barrels.append(pygame.Rect(x, 0, BARREL_SIZE, BARREL_SIZE))

def move_and_cull_barrels():
    for b in barrels:
        b.y += BARREL_SPEED
    # keep only onscreen barrels
    barrels[:] = [b for b in barrels if b.y < HEIGHT]

def hit_player(player_rect):
    return any(player_rect.colliderect(b) for b in barrels)

player  = Player(50, HEIGHT - player_idle_frames[0].get_height() - 10)
sprites = pygame.sprite.Group(player)

running       = True
barrel_timer  = 0
dk_tick      = 0
dk_frame     = 0

game_state = "start"

while True:
    dt = clock.tick(FPS) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    keys = pygame.key.get_pressed()

    # ─────────── START SCREEN ────────────
    if game_state == "start":
        win.blit(title_screen, (0, 0))
        if keys[pygame.K_SPACE]:
            # reset game
            player.rect.topleft = (50, HEIGHT - player_idle_frames[0].get_height() - 10)
            barrels.clear()
            game_state = "playing"
        pygame.display.update()
        continue

    # ─────────── DEATH SCREEN ────────────
    if game_state == "dead":
        win.blit(death_screen, (0, 0))
        if keys[pygame.K_SPACE]:
            # respawn
            player.rect.topleft = (50, HEIGHT - player_idle_frames[0].get_height() - 10)
            barrels.clear()
            game_state = "playing"
        pygame.display.update()
        continue

    # ─────────── GAMEPLAY ────────────────
    barrel_timer += 1
    if barrel_timer > 120:
        spawn_barrel()
        barrel_timer = -1

    player.handle_input(keys)
    player.apply_gravity()
    player.collide(platforms)
    sprites.update()
    move_and_cull_barrels()

    if hit_player(player.rect):
        print("Game Over!")
        game_state = "dead"

    if player.rect.colliderect(goal):
        print("You Win!")
        game_state = "start"  # go back to title on win

    # ─────────── RENDERING ───────────────
    win.blit(game_image, (0, 0))
    for p in platforms:
        pygame.draw.rect(win, BLUE, p)
    for b in barrels:
        pygame.draw.rect(win, BROWN, b)
    pygame.draw.rect(win, GREEN, goal)

    for sprite in sprites:
        win.blit(sprite.image, sprite.rect)

    dk_tick += 1
    if dk_tick % 12 == 0:
        dk_frame = (dk_frame + 1) % len(donkey_kong_run_frames)
    win.blit(donkey_kong_run_frames[dk_frame], (350, 0))

    pygame.display.update()

pygame.quit()
sys.exit()
