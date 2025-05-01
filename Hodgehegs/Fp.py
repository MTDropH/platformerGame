import pygame
import random
import json
import os

pygame.init()

WIDTH, HEIGHT = 1050, 600
FPS = 60
GRAVITY = 1.5
FLAP_STRENGTH = -15
PIPE_WIDTH = 90
PIPE_GAP = 400
PIPE_SPEED = 7

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (93, 0, 75)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()

bird_image = pygame.image.load('Millie/Bird.png').convert_alpha()
background_image = pygame.image.load('Millie/Forest.webp').convert_alpha()

class Bird:
    def __init__(self):
        self.image = bird_image
        self.x = 50
        self.y = HEIGHT // 2
        self.velocity = 0
        self.angle = 0  # Degrees

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity

        # Rotate right (downward) over time, up to 90°
        if self.angle < 80:
            self.angle += 3  # Adjust speed of rotation as needed

    def flap(self):
        self.velocity = FLAP_STRENGTH

        # Rotate left (upward), but not beyond -45°
        if self.angle > -45:
            self.angle -= 50  # Adjust amount of lift rotation

    def draw(self):
        # Rotate image and center it around current position
        rotated_image = pygame.transform.rotate(self.image, -self.angle)  # Negative to rotate visually correct
        new_rect = rotated_image.get_rect(center=(self.x + self.image.get_width() // 2, self.y + self.image.get_height() // 2))
        screen.blit(rotated_image, new_rect.topleft)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())


class Pipe:
    def __init__(self):
        self.x = WIDTH
        self.height = random.randint(50, HEIGHT - PIPE_GAP - 50)
        self.top_rect = pygame.Rect(self.x, 0, PIPE_WIDTH, self.height)
        self.bottom_rect = pygame.Rect(self.x, self.height + PIPE_GAP, PIPE_WIDTH, HEIGHT)

    def update(self):
        self.x -= PIPE_SPEED
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x

    def draw(self):
        pygame.draw.rect(screen, GREEN, self.top_rect)
        pygame.draw.rect(screen, GREEN, self.bottom_rect)

    def off_screen(self):
        return self.x < -PIPE_WIDTH

    def collide(self, bird):
        return self.top_rect.colliderect(bird.get_rect()) or self.bottom_rect.colliderect(bird.get_rect())

bird = Bird()
pipes = [Pipe(), Pipe(), Pipe()]
pipes[1].x -= 1000
pipes[2].x -= 500
score = 0

start = False
game_over = False

import requests
import json

# Define the server URL
server_url = "https://tearabytess.co.uk/Teaching/highscore"

# Optional: load high score from the server
try:
    response = requests.get(server_url)
    response.raise_for_status()  # Will raise an exception for 4xx/5xx status codes
    high_score_data = response.json()
    high_score = high_score_data.get("score", 0)
except requests.exceptions.RequestException as e:
    print(f"Error fetching high score: {e}")
    high_score = 0  # Fallback to 0 if there's an error

running = True
while running:
    clock.tick(FPS)
    screen.blit(background_image, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if not game_over:
                bird.flap()
                start = True
            else:
                # If game_over is True and user hits SPACE, perhaps restart:
                bird = Bird()
                pipes = [Pipe(), Pipe(), Pipe()]
                pipes[1].x -= 1000
                pipes[2].x -= 500
                score = 0
                PIPE_SPEED = 7
                start = False
                game_over = False

    if not game_over:
        if start:
            bird.update()
            for pipe in pipes:
                pipe.update()
                # Collision
                if pipe.collide(bird):
                    game_over = True
                # Off-screen
                if pipe.off_screen():
                    pipes.remove(pipe)   
                    pipes.append(Pipe())
                    score += 1
                    PIPE_SPEED += 0.5

            # Check if out of bounds
            if bird.y > HEIGHT or bird.y < 0:
                game_over = True

        # Draw everything
        bird.draw()
        for pipe in pipes:
            pipe.draw()

        # Draw score
        font = pygame.font.SysFont(None, 36) 
        text = font.render(f'Score: {score}, Highscore: {high_score}', True, BLACK)
        screen.blit(text, (10, 10))

    else:
        if score > high_score:
            high_score = score
            try:
                response = requests.post(
                    "https://tearabytess.co.uk/Teaching/highscore",
                    headers={"Content-Type": "application/json"},
                    json={"score": high_score}
                )
                response.raise_for_status()
                print("High score updated on server.")
            except requests.exceptions.RequestException as e:
                print(f"Failed to update high score on server: {e}")


        font = pygame.font.SysFont(None, 72)
        msg = f"GAME OVER! Score: {score} (Best: {high_score})"
        text = font.render(msg, True, (255, 0, 0))
        screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))

    pygame.display.flip()

pygame.quit()
