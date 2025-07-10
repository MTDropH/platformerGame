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
slime_frames = [None, None]  # Initialize slime_frames

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Max the Knight")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

def load_level_sprites(level_number):
    global background_img, platform_images, decoration_images, powerup_img, enemy_frames, flag_img

    if level_number == 3:
        # Level 3 assets - above ground
        flag_img = pygame.transform.scale(
            pygame.image.load("Jack/images/level_3_flag.png").convert_alpha(), (TILE, TILE * 2))

        platform_images["dirt"] = pygame.transform.scale(
            pygame.image.load("Jack/images/dirt.png").convert_alpha(), (TILE, TILE))
        platform_images["stone_dirt"] = pygame.transform.scale(
            pygame.image.load("Jack/images/stone_dirt.png").convert_alpha(), (TILE, TILE))
        
        decoration_images["grass"] = pygame.transform.scale(
            pygame.image.load("Jack/images/deco_grass.png").convert_alpha(), (TILE, TILE))
        decoration_images["stone"] = pygame.transform.scale(
            pygame.image.load("Jack/images/level_3_stone.png").convert_alpha(), (TILE, TILE))

        #powerup_img = pygame.transform.scale(
        #    pygame.image.load("Jack/images/magic_gem.png").convert_alpha(), (TILE, TILE))

        enemy_frames[0] = pygame.transform.scale(
            pygame.image.load("Jack/images/evil guy run1.png").convert_alpha(), (TILE, TILE * 2))
        enemy_frames[1] = pygame.transform.scale(
            pygame.image.load("Jack/images/evil guy run2.png").convert_alpha(), (TILE, TILE * 2))

        # Load background for level 3
        background_img_raw = pygame.image.load("Jack/images/level_3_background.png").convert()
        background_img = pygame.transform.scale(background_img_raw, (
            int(background_img_raw.get_width() * (HEIGHT / background_img_raw.get_height())), HEIGHT))

    elif level_number == 2:
        # Level 2 assets
        flag_img = pygame.transform.scale(
            pygame.image.load("Jack/images/level_2_flag.png").convert_alpha(), (TILE, TILE * 2))

        platform_images["dirt"] = pygame.transform.scale(
            pygame.image.load("Jack/images/level_2_dirt1.png").convert_alpha(), (TILE, TILE))
        platform_images["stone_dirt"] = pygame.transform.scale(
            pygame.image.load("Jack/images/level_2_stone_dirt1.png").convert_alpha(), (TILE, TILE))

        decoration_images["grass"] = pygame.transform.scale(
            pygame.image.load("Jack/images/dark_deco_stone.png").convert_alpha(), (TILE, TILE))
        decoration_images["stone"] = pygame.transform.scale(
            pygame.image.load("Jack/images/level_2_deco_2.png").convert_alpha(), (TILE, TILE))

        powerup_img = pygame.transform.scale(
            pygame.image.load("Jack/images/armour polish.png").convert_alpha(), (TILE, TILE))

        enemy_frames[0] = pygame.transform.scale(
            pygame.image.load("Jack/images/evil guy run1.png").convert_alpha(), (TILE, TILE * 2))
        enemy_frames[1] = pygame.transform.scale(
            pygame.image.load("Jack/images/evil guy run2.png").convert_alpha(), (TILE, TILE * 2))

        # Load background for level 2 (optional if you have different backgrounds)
        background_img_raw = pygame.image.load("Jack/images/new_level_two_background.png").convert()
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

def load_slime_sprites():
    """Load slime sprites - add this to your load_level_sprites function"""
    global slime_frames
    # Replace these with your actual slime image files
    slime_frames = [
        pygame.transform.scale(pygame.image.load("Jack/images/goober1.png").convert_alpha(), (TILE, TILE)),
        pygame.transform.scale(pygame.image.load("Jack/images/goober2.png").convert_alpha(), (TILE, TILE))
    ]

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
        # Add hurt animation variables
        self.is_hurt = False
        self.hurt_timer = 0
        self.hurt_duration = 0.5  # How long the hurt animation plays

    def animate(self):
        # Determine which sprite set to use based on current state
        if self.is_hurt:
            # Use hurt sprites during hurt animation
            if self.lives == 3:
                run_frames = powered_up_run_frames  # You might want powered up hurt frames
                idle_frames = powered_up_idle_frames
                attack_frame = powered_up_attack_frame
            elif self.lives == 2:
                run_frames = player_run_hurt_frames
                idle_frames = player_idle_hurt_frames
                attack_frame = player_attack_hurt_frame
            else:  # lives == 1
                run_frames = player_run_hurt_frames
                idle_frames = player_idle_hurt_frames
                attack_frame = player_attack_hurt_frame
        else:
            # Use normal sprites
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
            if self.is_hurt:
                if self.lives >= 2:
                    image = player_shoot_hurt_frame
                else:
                    image = player_shoot_hurt_frame
            else:
                if self.lives == 3:
                    image = powered_up_shoot_frame
                elif self.lives == 2:
                    image = player_shoot_frame
                else:
                    image = player_shoot_hurt_frame
        elif not self.on_ground:
            if self.is_hurt:
                image = player_jump_hurt_frame
            else:
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
            
        # Handle invincibility flicker
        if self.invincible and int(pygame.time.get_ticks() / 100) % 2 == 0:
            image.set_alpha(128)  # Flicker on
        else:
            image.set_alpha(255)  # Flicker off / normal

        self.image = image

    def take_damage(self):
        """Call this method when the player takes damage"""
        if not self.invincible:
            self.lives -= 1
            self.invincible = True
            self.invincibility_timer = 1.0
            # Start hurt animation
            self.is_hurt = True
            self.hurt_timer = self.hurt_duration
            return True  # Damage was taken
        return False  # No damage taken (invincible)

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

        # Handle hurt animation timer
        if self.is_hurt:
            self.hurt_timer -= 1 / FPS
            if self.hurt_timer <= 0:
                self.is_hurt = False

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

class BossKingSlime(AnimatedEntity):
    def __init__(self, x, y):
        # Load king slime sprites (you'll need to create these images)
        global slime_frames
        
        # Ensure slime_frames are loaded first
        if slime_frames == [None, None] or slime_frames is None:
            load_slime_sprites()
        
        try:
            king_slime_frames = [
                pygame.transform.scale(pygame.image.load("Jack/images/king_goober1.png").convert_alpha(), (TILE * 3, TILE * 3)),
                pygame.transform.scale(pygame.image.load("Jack/images/king_goober2.png").convert_alpha(), (TILE * 3, TILE * 3))
            ]
        except:
            # Fallback: use scaled up regular slime frames
            if slime_frames and slime_frames[0] is not None:
                king_slime_frames = [
                    pygame.transform.scale(slime_frames[0], (TILE * 3, TILE * 3)),
                    pygame.transform.scale(slime_frames[1], (TILE * 3, TILE * 3))
                ]
            else:
                # Final fallback: use enemy frames
                king_slime_frames = [
                    pygame.transform.scale(enemy_frames[0], (TILE * 3, TILE * 3)),
                    pygame.transform.scale(enemy_frames[1], (TILE * 3, TILE * 3))
                ]
        
        super().__init__(x, y, king_slime_frames, animation_speed=0.05)
        
        # Boss stats
        self.max_health = 5
        self.health = self.max_health
        self.jump_height = 12
        self.slam_damage_radius = TILE * 2
        self.on_ground = False
        self.vel.x = 0
        
        # Attack patterns
        self.attack_timer = 2.0  # Start with initial delay
        self.attack_cooldown = 3.0  # Time between attacks
        self.current_attack = "jump"  # "jump", "slam", "spawn_minions"
        self.attack_phase = 0  # Current phase of attack
        
        # Slam attack variables
        self.is_slamming = False
        self.slam_charge_time = 1.0
        self.slam_timer = 0
        
        # Minion spawning
        self.minions_spawned = 0
        self.max_minions = 3
        self.spawn_timer = 0
        
        # Movement
        self.move_speed = 1
        self.move_timer = 0
        self.move_direction = 1
        self.patrol_range = TILE * 8
        self.start_x = x
        
        # Visual effects
        self.hit_flash_timer = 0
        self.invincible = False
        self.invincibility_timer = 0
        
        # Add state tracking
        self.is_attacking = False
        
        # Sound effects (optional) - with better error handling
        self.roar_sound = None
        self.slam_sound = None
        try:
            self.roar_sound = pygame.mixer.Sound("Jack/sounds/boss_roar.mp3")
        except:
            pass
        try:
            self.slam_sound = pygame.mixer.Sound("Jack/sounds/boss_slam.mp3")
        except:
            pass
    
    def take_damage(self):
        """Handle taking damage from player attacks"""
        if not self.invincible:
            self.health -= 1
            self.hit_flash_timer = 0.3
            self.invincible = True
            self.invincibility_timer = 0.8
            
            if self.roar_sound:
                self.roar_sound.play()
            
            # Get more aggressive as health decreases
            if self.health <= 2:
                self.attack_cooldown = 2.0  # Attack more frequently
                self.jump_height = 15  # Jump higher
            
            return self.health <= 0  # Return True if boss is defeated
        return False
    
    def apply_gravity(self):
        if not self.on_ground:
            self.vel.y += GRAVITY
            if self.vel.y > TILE * 2:  # Boss falls faster
                self.vel.y = TILE * 2
    
    def patrol_movement(self):
        """Simple patrol movement when not attacking"""
        if not self.is_attacking:
            # Move horizontally within patrol range
            target_left = self.start_x - self.patrol_range // 2
            target_right = self.start_x + self.patrol_range // 2
            
            if self.rect.centerx <= target_left:
                self.move_direction = 1
            elif self.rect.centerx >= target_right:
                self.move_direction = -1
            
            self.vel.x = self.move_direction * self.move_speed
    
    def jump_attack(self, player):
        """Jump towards the player"""
        if self.on_ground and not self.is_attacking:
            # Calculate direction to player
            direction = 1 if player.rect.centerx > self.rect.centerx else -1
            
            # Jump towards player
            self.vel.y = -self.jump_height
            self.vel.x = direction * 3  # Horizontal velocity towards player
            
            self.is_attacking = True
            return True  # Attack completed
        elif not self.on_ground and self.is_attacking:
            # Keep moving horizontally while in air
            return False
        elif self.on_ground and self.is_attacking:
            # Landed, stop attacking
            self.is_attacking = False
            self.vel.x = 0
            return True
        return False
    
    def slam_attack(self, player):
        """Charge up and slam down with area damage"""
        if self.attack_phase == 0:  # Start charge phase
            self.is_slamming = True
            self.is_attacking = True
            self.slam_timer = self.slam_charge_time
            self.attack_phase = 1
            self.vel.x = 0  # Stop moving
            return False
        
        elif self.attack_phase == 1:  # Charging
            self.slam_timer -= 1 / FPS
            if self.slam_timer <= 0:
                # Execute slam
                self.vel.y = TILE * 2  # Fast downward velocity
                self.attack_phase = 2
            return False
        
        elif self.attack_phase == 2:  # Slamming down
            if self.on_ground:
                # Slam impact - deal area damage
                if self.slam_sound:
                    self.slam_sound.play()
                
                # Check if player is within damage radius
                distance = abs(player.rect.centerx - self.rect.centerx)
                if distance <= self.slam_damage_radius:
                    # Player takes damage from slam
                    if player.take_damage():  # Use player's take_damage method
                        # Knockback player
                        knockback_dir = 1 if player.rect.centerx > self.rect.centerx else -1
                        player.hurt_knockback = pygame.Vector2(knockback_dir * 5, -3)
                
                self.is_slamming = False
                self.is_attacking = False
                self.attack_phase = 0
                return True  # Attack completed
        
        return False
    
    def spawn_minions_attack(self, slimes_group):
        """Spawn small slimes as minions"""
        if not self.is_attacking:
            self.is_attacking = True
            self.minions_spawned = 0
            self.spawn_timer = 0.5
        
        if self.minions_spawned < self.max_minions:
            self.spawn_timer -= 1 / FPS
            if self.spawn_timer <= 0:
                # Spawn a minion slime on either side of the boss
                side = 1 if self.minions_spawned % 2 == 0 else -1
                spawn_x = self.rect.centerx + (side * TILE * 2)
                spawn_y = self.rect.bottom - TILE
                
                minion = Slime(spawn_x, spawn_y, jump_height=6, jump_interval=1.5)
                slimes_group.add(minion)
                
                self.minions_spawned += 1
                self.spawn_timer = 0.5  # Delay between spawns
        
        if self.minions_spawned >= self.max_minions:
            self.is_attacking = False
            return True  # Attack completed
        
        return False
    
    def choose_next_attack(self):
        """Choose the next attack pattern"""
        import random
        
        if self.health <= 2:
            # More aggressive attacks when low health
            attacks = ["slam", "jump", "spawn_minions"]
            weights = [40, 40, 20]  # Prefer slam and jump
        else:
            attacks = ["jump", "slam", "spawn_minions"]
            weights = [50, 30, 20]  # Prefer jumping
        
        self.current_attack = random.choices(attacks, weights=weights)[0]
        self.attack_phase = 0
    
    def collide(self, tiles):
        """Handle collision with tiles"""
        # Vertical collision first
        old_y = self.rect.y
        self.rect.y += self.vel.y
        
        self.on_ground = False
        for tile in tiles:
            if self.rect.colliderect(tile):
                if self.vel.y > 0:  # Falling down
                    self.rect.bottom = tile.top
                    self.vel.y = 0
                    self.on_ground = True
                elif self.vel.y < 0:  # Moving up
                    self.rect.top = tile.bottom
                    self.vel.y = 0
        
        # Horizontal collision
        old_x = self.rect.x
        self.rect.x += self.vel.x
        
        for tile in tiles:
            if self.rect.colliderect(tile):
                if self.vel.x > 0:  # Moving right
                    self.rect.right = tile.left
                    self.vel.x = 0
                    self.move_direction = -1  # Change direction
                elif self.vel.x < 0:  # Moving left
                    self.rect.left = tile.right
                    self.vel.x = 0
                    self.move_direction = 1  # Change direction
    
    def update(self, player=None, tiles=None, slimes_group=None):
        """Main update method"""
        if not player:
            return
            
        # Handle invincibility
        if self.invincible:
            self.invincibility_timer -= 1 / FPS
            if self.invincibility_timer <= 0:
                self.invincible = False
        
        # Handle hit flash effect
        if self.hit_flash_timer > 0:
            self.hit_flash_timer -= 1 / FPS
        
        # Attack logic
        self.attack_timer -= 1 / FPS
        
        attack_completed = False
        if self.attack_timer <= 0 or self.is_attacking:
            # Execute current attack
            if self.current_attack == "jump":
                if self.jump_attack(player):
                    self.attack_timer = self.attack_cooldown
                    self.choose_next_attack()
                    attack_completed = True
            
            elif self.current_attack == "slam":
                if self.slam_attack(player):
                    self.attack_timer = self.attack_cooldown
                    self.choose_next_attack()
                    attack_completed = True
            
            elif self.current_attack == "spawn_minions":
                if slimes_group and self.spawn_minions_attack(slimes_group):
                    self.attack_timer = self.attack_cooldown
                    self.choose_next_attack()
                    attack_completed = True
        
        # Movement when not attacking
        if not self.is_attacking and not self.is_slamming:
            self.patrol_movement()
        
        # Apply physics
        self.apply_gravity()
        if tiles:
            self.collide(tiles)
        
        # Animation
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        
        frame = self.frames[int(self.frame_index)]
        
        # Flip sprite based on movement direction
        if self.vel.x < 0 or self.move_direction < 0:
            frame = pygame.transform.flip(frame, True, False)
        
        # Visual effects
        if self.hit_flash_timer > 0 and int(pygame.time.get_ticks() / 50) % 2 == 0:
            # Flash red when hit
            flash_surface = frame.copy()
            flash_surface.fill((255, 100, 100), special_flags=pygame.BLEND_ADD)
            self.image = flash_surface
        elif self.is_slamming and self.attack_phase == 1:
            # Flash white when charging slam
            flash_surface = frame.copy()
            flash_surface.fill((255, 255, 255), special_flags=pygame.BLEND_ADD)
            self.image = flash_surface
        else:
            self.image = frame
    
    def draw_health_bar(self, surface, camera_x):
        """Draw boss health bar"""
        if self.health <= 0:
            return
            
        bar_width = 200
        bar_height = 20
        bar_x = self.rect.centerx - bar_width // 2 - camera_x
        bar_y = self.rect.top - 40
        
        # Make sure health bar stays on screen
        if bar_x < 10:
            bar_x = 10
        elif bar_x + bar_width > WIDTH - 10:
            bar_x = WIDTH - bar_width - 10
            
        if bar_y < 10:
            bar_y = 10
        
        # Background
        pygame.draw.rect(surface, (100, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        
        # Health
        health_width = int((self.health / self.max_health) * bar_width)
        if health_width > 0:
            pygame.draw.rect(surface, (255, 0, 0), (bar_x, bar_y, health_width, bar_height))
        
        # Border
        pygame.draw.rect(surface, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)
        
        # Boss name
        try:
            font = pygame.font.SysFont("Arial", 16)
            name_text = font.render("KING SLIME", True, (255, 255, 255))
            name_x = bar_x + bar_width // 2 - name_text.get_width() // 2
            surface.blit(name_text, (name_x, bar_y - 25))
        except:
            pass  # Skip text if font fails

# Fixed load_slime_sprites function
def load_slime_sprites():
    """Load slime sprites - call this before creating any slimes"""
    global slime_frames
    try:
        slime_frames = [
            pygame.transform.scale(pygame.image.load("Jack/images/goober1.png").convert_alpha(), (TILE, TILE)),
            pygame.transform.scale(pygame.image.load("Jack/images/goober2.png").convert_alpha(), (TILE, TILE))
        ]
    except Exception as e:
        print(f"Could not load slime sprites: {e}")
        # Fallback to enemy frames
        slime_frames = [
            pygame.transform.scale(enemy_frames[0], (TILE, TILE)),
            pygame.transform.scale(enemy_frames[1], (TILE, TILE))
        ]

# Updated Slime class with better initialization
class Slime(AnimatedEntity):
    def __init__(self, x, y, jump_height=8, jump_interval=2.0):
        # Ensure slime_frames are loaded
        global slime_frames
        if slime_frames == [None, None] or slime_frames is None:
            load_slime_sprites()
        
        super().__init__(x, y, slime_frames)
        self.jump_height = jump_height
        self.jump_interval = jump_interval  # Time between jumps in seconds
        self.jump_timer = jump_interval  # Start with full timer
        self.on_ground = False
        self.vel.x = 0  # Slime doesn't move horizontally
        
    def apply_gravity(self):
        if not self.on_ground:
            self.vel.y += GRAVITY
            if self.vel.y > TILE:
                self.vel.y = TILE
    
    def jump(self):
        """Make the slime jump"""
        if self.on_ground:
            self.vel.y = -self.jump_height
            self.jump_timer = self.jump_interval
    
    def collide(self, tiles):
        # Vertical collision
        self.rect.y += self.vel.y
        self.on_ground = False
        for tile in tiles:
            if self.rect.colliderect(tile):
                if self.vel.y > 0:  # Falling down
                    self.rect.bottom = tile.top
                    self.vel.y = 0
                    self.on_ground = True
                elif self.vel.y < 0:  # Moving up (head hit)
                    self.rect.top = tile.bottom
                    self.vel.y = 0
    
    def update(self, player=None, tiles=None):
        # Handle jump timing
        if self.jump_timer > 0:
            self.jump_timer -= 1 / FPS
        else:
            self.jump()  # Jump when timer reaches 0
        
        # Animation
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        frame = self.frames[int(self.frame_index)]
        
        # Optional: Face the player direction for more dynamic feel
        if player and player.rect.centerx < self.rect.centerx:
            self.image = pygame.transform.flip(frame, True, False)
        else:
            self.image = frame
        
        # Apply physics
        self.apply_gravity()
        if tiles:
            self.collide(tiles)
    
    def draw_health_bar(self, surface, camera_x):
        """Draw boss health bar"""
        bar_width = 200
        bar_height = 20
        bar_x = self.rect.centerx - bar_width // 2 - camera_x
        bar_y = self.rect.top - 40
        
        # Background
        pygame.draw.rect(surface, (100, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        
        # Health
        health_width = int((self.health / self.max_health) * bar_width)
        pygame.draw.rect(surface, (255, 0, 0), (bar_x, bar_y, health_width, bar_height))
        
        # Border
        pygame.draw.rect(surface, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)
        
        # Boss name
        font = pygame.font.SysFont("Arial", 16)
        name_text = font.render("KING SLIME", True, (255, 255, 255))
        name_x = bar_x + bar_width // 2 - name_text.get_width() // 2
        surface.blit(name_text, (name_x, bar_y - 25))

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
            game_over_text = font.render("", True, (255, 0, 0))
            restart_text = font.render("", True, (255, 255, 255))
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 40))
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 10))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "restart"  # Return restart signal instead of calling main()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
    return False

def show_level_complete_screen(level_number=1):
    try:
        if level_number == 1:
            pygame.mixer.music.load("Jack/sounds/level_complete.mp3")
            pygame.mixer.music.play()
            level_complete_img = pygame.image.load("Jack/images/level_1_complete1.png").convert_alpha()
        elif level_number == 2:
            pygame.mixer.music.load("Jack/sounds/level_complete.mp3")
            pygame.mixer.music.play()
            level_complete_img = pygame.image.load("Jack/images/level_2_complete.png").convert_alpha()
        elif level_number == 3:
            pygame.mixer.music.load("Jack/sounds/level_complete.mp3")
            pygame.mixer.music.play()
            level_complete_img = pygame.image.load("Jack/images/game_complete.png").convert_alpha()

    except:
        # Fallback if images/sounds don't exist
        level_complete_img = None

    if level_complete_img:
        level_complete_img = pygame.transform.scale(level_complete_img, (WIDTH, HEIGHT))

    waiting = True
    while waiting:
        screen.fill((0, 0, 0))
        
        if level_complete_img:
            screen.blit(level_complete_img, (0, 0))
        
        if level_number == 3:
            # Game complete message
            complete_text = font.render("CONGRATULATIONS! GAME COMPLETE!", True, (255, 255, 0))
            thanks_text = font.render("Thanks for playing Max the Knight!", True, (255, 255, 255))
            restart_text = font.render("Press ENTER to play again or ESC to quit", True, (200, 200, 200))
            
            screen.blit(complete_text, (WIDTH // 2 - complete_text.get_width() // 2, HEIGHT // 2 - 60))
            screen.blit(thanks_text, (WIDTH // 2 - thanks_text.get_width() // 2, HEIGHT // 2 - 20))
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 20))
        else:
            # For levels 1 and 2, show "Press any key to continue" message
            continue_text = font.render("", True, (255, 255, 255))
            screen.blit(continue_text, (WIDTH // 2 - continue_text.get_width() // 2, HEIGHT - 50))
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if level_number == 3:
                    if event.key == pygame.K_RETURN:
                        return "restart"  # Return restart signal instead of calling main() directly
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                else:
                    # For levels 1 and 2, any key continues
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

def create_level_with_boss(filename='Jack/level1.json'):
    """Load level data from JSON file with boss support"""
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
        tile_type = tile_data.get("type", "dirt")
        tiles.append(rect)
        tile_types.append(tile_type)

    decorations = []
    for deco in data.get("decorations", []):
        rect = pygame.Rect(deco["x"], deco["y"], deco["width"], deco["height"])
        deco_type = deco.get("type", "grass")
        decorations.append({"rect": rect, "type": deco_type})

    # Regular enemies
    enemies = pygame.sprite.Group()
    for enemy_data in data.get("enemies", []):
        enemy = Enemy(enemy_data["x"], enemy_data["y"], enemy_data["left_bound"], enemy_data["right_bound"])
        enemies.add(enemy)
    
    # Add slimes
    slimes = pygame.sprite.Group()
    for slime_data in data.get("slimes", []):
        jump_height = slime_data.get("jump_height", 8)
        jump_interval = slime_data.get("jump_interval", 2.0)
        slime = Slime(slime_data["x"], slime_data["y"], jump_height, jump_interval)
        slimes.add(slime)
    
    # Add boss (FIXED: Check for "boss" type instead of "king_slime")
    boss = None
    boss_data = data.get("boss")
    if boss_data and boss_data.get("type") == "boss":  # Changed from "king_slime" to "boss"
        boss = BossKingSlime(boss_data["x"], boss_data["y"])
        print(f"Boss created at ({boss_data['x']}, {boss_data['y']})")  # Debug print
    else:
        print(f"Boss data: {boss_data}")  # Debug print to see what's in the data

    flag_data = data["flag"]
    flag = pygame.Rect(flag_data["x"], flag_data["y"], flag_data["width"], flag_data["height"])

    powerups = pygame.sprite.Group()
    for powerup_data in data.get("powerups", []):
        powerup = PowerUp(powerup_data["x"], powerup_data["y"], powerup_data.get("type", "health"))
        powerups.add(powerup)

    return tiles, tile_types, decorations, enemies, slimes, flag, powerups, boss


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
    tiles, tile_types, decorations, enemies, slimes, flag, powerups, boss = create_level_with_boss(level_file)

    player = Player(64, HEIGHT - 3 * TILE)
    player.arrow_group = pygame.sprite.Group()

    sprites = pygame.sprite.Group(player, *enemies, *slimes, *powerups)
    if boss:
        sprites.add(boss)  

    # Boss AI timing variables
    boss_attack_timer = 0
    boss_move_timer = 0
    boss_special_attack_timer = 0
    boss_invulnerability_timer = 0

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

        # Death barrier: Player falls below the screen
        if player.rect.top > HEIGHT + 100:  # 100 pixels below screen
            player.lives -= 1
            if player.lives <= 0:
                result = show_game_over_screen()
                if result == "restart":
                    return "restart"  # Signal to restart the game
                return "quit"  # Signal to quit the game
            else:
                player.rect.topleft = (64, HEIGHT - 3 * TILE)
                player.vel = pygame.Vector2(0, 0)

        # Update enemies and slimes
        for enemy in enemies:
            enemy.update(player, tiles)
            
        for slime in slimes:
            slime.update(player, tiles)

        # Enhanced Boss AI
        if boss and boss.health > 0:
            # Update boss timers
            boss_attack_timer += dt
            boss_move_timer += dt
            boss_special_attack_timer += dt
            boss_invulnerability_timer -= dt

            # Calculate distance to player
            distance_to_player = abs(boss.rect.centerx - player.rect.centerx)
            player_below = player.rect.centery > boss.rect.centery
            
            # Boss movement AI - more intelligent positioning
            if boss_move_timer > 1.0:  # Move decision every second
                boss_move_timer = 0
                
                # If player is too close, try to maintain distance
                if distance_to_player < 150:
                    if player.rect.centerx < boss.rect.centerx:
                        boss.target_direction = 1  # Move right
                    else:
                        boss.target_direction = -1  # Move left
                # If player is too far, move closer
                elif distance_to_player > 300:
                    if player.rect.centerx < boss.rect.centerx:
                        boss.target_direction = -1  # Move left
                    else:
                        boss.target_direction = 1  # Move right
                else:
                    boss.target_direction = 0  # Stay in position

            # Boss attack patterns based on health
            health_percentage = boss.health / boss.max_health if hasattr(boss, 'max_health') else 1.0
            
            # Basic attack - more frequent when health is low
            attack_cooldown = 2.0 if health_percentage > 0.5 else 1.5
            if boss_attack_timer > attack_cooldown and distance_to_player < 200:
                boss_attack_timer = 0
                # Trigger boss basic attack (you'll need to implement this in boss class)
                if hasattr(boss, 'attack'):
                    boss.attack(player)

            # Special attack - triggered at certain health thresholds
            special_cooldown = 8.0 if health_percentage > 0.3 else 5.0
            if boss_special_attack_timer > special_cooldown:
                boss_special_attack_timer = 0
                # Trigger special attack based on health
                if health_percentage <= 0.3:  # Desperate phase
                    if hasattr(boss, 'desperate_attack'):
                        boss.desperate_attack(player)
                elif health_percentage <= 0.6:  # Angry phase
                    if hasattr(boss, 'special_attack'):
                        boss.special_attack(player)

            # Update boss with original parameters (compatible with existing boss class)
            boss.update(player, tiles, slimes)
            
            # Apply enhanced AI movement if boss has the attributes
            if hasattr(boss, 'target_direction'):
                if boss.target_direction == 1:
                    boss.vel.x = min(boss.vel.x + 100 * dt, 50)  # Move right
                elif boss.target_direction == -1:
                    boss.vel.x = max(boss.vel.x - 100 * dt, -50)  # Move left
                else:
                    boss.vel.x *= 0.9  # Slow down when not moving

        sprites.update()
        attack_rect = player.get_attack_hitbox()

        # Handle player collision with slimes (same as enemies)
        for slime in list(slimes):  # Use list() to avoid modification during iteration
            if player.rect.colliderect(slime.rect):
                if player.vel.y > 0 and player.rect.bottom - slime.rect.top < TILE * 0.75:
                    # stomp slime
                    slimes.remove(slime)
                    sprites.remove(slime)
                    player.vel.y = JUMP_VELOCITY / 1.5
                else:
                    if not player.invincible:
                        player.lives -= 1
                        player.invincible = True
                        player.invincibility_timer = 1.0
                        
                        if player.lives <= 0:
                            result = show_game_over_screen()
                            if result == "restart":
                                return "restart"
                            return "quit"

        # Handle sword attacks on slimes
        if attack_rect:
            for slime in list(slimes):  # Use list() to avoid modification during iteration
                if attack_rect.colliderect(slime.rect):
                    slimes.remove(slime)
                    sprites.remove(slime)

        # Handle arrow hits on slimes
        for arrow in player.arrow_group:
            hit_slimes = pygame.sprite.spritecollide(arrow, slimes, dokill=True)
            if hit_slimes:
                arrow.kill()
                for slime in hit_slimes:
                    sprites.remove(slime)

        # Handle sword attacks on enemies
        if attack_rect:
            for enemy in list(enemies):  # Use list() to avoid modification during iteration
                if attack_rect.colliderect(enemy.rect):
                    enemies.remove(enemy)
                    sprites.remove(enemy)

        # Handle arrow hits on enemies
        for arrow in player.arrow_group:
            hit_enemies = pygame.sprite.spritecollide(arrow, enemies, dokill=True)
            if hit_enemies:
                arrow.kill()
                for enemy in hit_enemies:
                    sprites.remove(enemy)

        # Handle player collision with enemies
        for enemy in list(enemies):  # Use list() to avoid modification during iteration
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
                            result = show_game_over_screen()
                            if result == "restart":
                                return "restart"
                            return "quit"

        # Enhanced boss combat with invulnerability frames
        if boss and boss.health > 0:
            # Check if player attacks hit the boss (with invulnerability check)
            if attack_rect and attack_rect.colliderect(boss.rect) and boss_invulnerability_timer <= 0:
                if boss.take_damage():
                    # Boss defeated!
                    boss = None
                    # Maybe spawn a special powerup or trigger level completion
                else:
                    boss_invulnerability_timer = 0.5  # Brief invulnerability after hit
                    # Boss hit reaction - could trigger rage mode
                    if hasattr(boss, 'on_hit'):
                        boss.on_hit(player)

            # Check arrow hits on boss (with invulnerability check)
            for arrow in list(player.arrow_group):
                if arrow.rect.colliderect(boss.rect) and boss_invulnerability_timer <= 0:
                    arrow.kill()
                    if boss.take_damage():
                        boss = None
                    else:
                        boss_invulnerability_timer = 0.5
                        if hasattr(boss, 'on_hit'):
                            boss.on_hit(player)

            # Check boss collision with player - enhanced damage system
            if boss and player.rect.colliderect(boss.rect) and not player.invincible:
                # Different damage based on boss attack state
                damage = 1
                if hasattr(boss, 'is_attacking') and boss.is_attacking:
                    damage = 2  # More damage during boss attacks
                
                player.lives -= damage
                player.invincible = True
                player.invincibility_timer = 2.0  # Longer invincibility after boss hit
                
                # Knockback effect
                knockback_force = 200
                if player.rect.centerx < boss.rect.centerx:
                    player.vel.x = -knockback_force
                else:
                    player.vel.x = knockback_force
                
                if player.lives <= 0:
                    result = show_game_over_screen()
                    if result == "restart":
                        return "restart"
                    return "quit"

        # Handle powerup collection
        for powerup in list(powerups):  # Use list() to avoid modification during iteration
            if player.rect.colliderect(powerup.rect):
                powerups.remove(powerup)
                sprites.remove(powerup)
                item_sound.play()
                if powerup.type == "bow":
                    player.has_bow = True
                else:
                    if player.lives < 3:
                        player.lives += 1

        # Check for level completion
        if player.rect.colliderect(flag):
            # Only allow completion if boss is defeated (if there was one)
            if not boss or boss.health <= 0:
                print("Level complete!")
                result = show_level_complete_screen(level_number)
                if result == "restart":
                    return "restart"
                if level_number >= 3:
                    return "complete"  # Game completed
                else:
                    return "next_level"  # Go to next level

        camera_x = max(0, min(player.rect.centerx - WIDTH // 2, LEVEL_WIDTH - WIDTH))

        # --- DRAW ---
        for x in range(0, WIDTH * 3, background_width):
            screen.blit(background_img, (x - camera_x * background_scroll_speed, 0))

        draw_tiles(screen, tiles, tile_types, camera_x, decorations)
        
        # Draw all sprites
        for sprite in sprites:
            # Boss flashing effect when hit
            if sprite == boss and boss_invulnerability_timer > 0:
                if int(boss_invulnerability_timer * 20) % 2:  # Flash effect
                    continue  # Skip drawing this frame
            screen.blit(sprite.image, sprite.rect.move(-camera_x, 0))

        # Draw boss
        if boss and boss.health > 0:
            # Skip drawing if flashing
            if not (boss_invulnerability_timer > 0 and int(boss_invulnerability_timer * 20) % 2):
                screen.blit(boss.image, (boss.rect.x - camera_x, boss.rect.y))
            boss.draw_health_bar(screen, camera_x)

        # Draw attack sword
        if attack_rect:
            sword_pos = (player.rect.right if player.facing_right else player.rect.left - sword_img.get_width(),
                         player.rect.top + 32)
            sword_image = sword_img if player.facing_right else pygame.transform.flip(sword_img, True, False)
            screen.blit(sword_image, (sword_pos[0] - camera_x, sword_pos[1]))

        # Draw arrows
        for arrow in player.arrow_group:
            screen.blit(arrow.image, arrow.rect.move(-camera_x, 0))

        # Draw flag and UI
        screen.blit(flag_img, flag.move(-camera_x, 0))
        draw_lives(screen, player.lives)

        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    current_level = 1
    while True:
        result = main(level_number=current_level)
        if result == "restart":
            current_level = 1  # Restart from level 1
        elif result == "next_level":
            current_level += 1
            if current_level > 3:  # Assuming you have 3 levels
                current_level = 1  # Loop back to level 1 or handle game completion
        elif result == "complete":
            current_level = 1  # Reset to level 1 after game completion
        else:
            break  # Exit the game