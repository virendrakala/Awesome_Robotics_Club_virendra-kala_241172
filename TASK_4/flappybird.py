import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH = 400
HEIGHT = 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 155, 255)
GREEN = (0, 200, 0)
BIRD_COLOR = (255, 255, 0)

# Game settings
FPS = 60
GRAVITY = 0.2
JUMP_STRENGTH = -5
PIPE_GAP = 150
PIPE_WIDTH = 70
PIPE_SPEED = 4

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Bird class
class Bird:
    def __init__(self):
        self.x = 50
        self.y = HEIGHT // 2
        self.velocity = 0
        self.radius = 15

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity

    def jump(self):
        self.velocity = JUMP_STRENGTH

    def draw(self):
        pygame.draw.circle(SCREEN, BIRD_COLOR, (int(self.x), int(self.y)), self.radius)

# Pipe class
class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(50, HEIGHT - PIPE_GAP - 50)
        self.passed = False

    def update(self):
        self.x -= PIPE_SPEED

    def draw(self):
        pygame.draw.rect(SCREEN, GREEN, (self.x, 0, PIPE_WIDTH, self.height))
        pygame.draw.rect(SCREEN, GREEN, (self.x, self.height + PIPE_GAP, PIPE_WIDTH, HEIGHT))

    def collide(self, bird):
        bird_rect = pygame.Rect(bird.x - bird.radius, bird.y - bird.radius, bird.radius * 2, bird.radius * 2)
        top_rect = pygame.Rect(self.x, 0, PIPE_WIDTH, self.height)
        bottom_rect = pygame.Rect(self.x, self.height + PIPE_GAP, PIPE_WIDTH, HEIGHT)
        return bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect)

# Start screen
def show_start_screen():
    while True:
        SCREEN.fill(BLUE)
        title = font.render("Flappy Bird", True, WHITE)
        prompt = font.render("Press 'S' to Start", True, WHITE)
        SCREEN.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 60))
        SCREEN.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                return

# End screen
def show_game_over(score):
    while True:
        SCREEN.fill(BLUE)
        over_text = font.render("Game Over!", True, WHITE)
        score_text = font.render(f"Score: {score}", True, WHITE)
        retry_text = font.render("Press 'C' to Play Again", True, WHITE)
        SCREEN.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2 - 60))
        SCREEN.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 20))
        SCREEN.blit(retry_text, (WIDTH // 2 - retry_text.get_width() // 2, HEIGHT // 2 + 20))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                return

# Main game loop
def main():
    while True:
        show_start_screen()

        bird = Bird()
        pipes = [Pipe(WIDTH + 100)]
        score = 0
        running = True

        while running:
            clock.tick(FPS)
            SCREEN.fill(BLUE)

            # Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    bird.jump()

            bird.update()

            # Add new pipes
            if pipes[-1].x < WIDTH - 200:
                pipes.append(Pipe(WIDTH))

            for pipe in pipes:
                pipe.update()
                pipe.draw()
                if pipe.collide(bird):
                    running = False
                if not pipe.passed and pipe.x + PIPE_WIDTH < bird.x:
                    pipe.passed = True
                    score += 1

            # Remove off-screen pipes
            pipes = [pipe for pipe in pipes if pipe.x + PIPE_WIDTH > 0]

            # Ground/ceiling collision
            if bird.y - bird.radius < 0 or bird.y + bird.radius > HEIGHT:
                running = False

            bird.draw()

            # Score
            score_text = font.render(f"Score: {score}", True, WHITE)
            SCREEN.blit(score_text, (10, 10))

            pygame.display.flip()

        show_game_over(score)

if __name__ == "__main__":
    main()
