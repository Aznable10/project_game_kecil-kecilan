import pygame
import random
import sys

# ---------- Setup ----------
pygame.init()

WIDTH, HEIGHT = 900, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Mario Runner")
clock = pygame.time.Clock()

# Colors
BG_SKY = (135, 206, 235)
BG_GROUND = (80, 180, 80)
PLAYER_COLOR = (235, 60, 35)
DARK_BROWN = (109, 79, 49)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Player variables
PLAYER_X = 100
PLAYER_WIDTH = 32
PLAYER_HEIGHT = 40
GROUND_Y = 330
player_y = GROUND_Y - PLAYER_HEIGHT
player_vel_y = 0
gravity = 0.7
jump_power = -13
on_ground = True

# Obstacles
obstacles = []
spawn_timer = 0
score = 0
game_over = False

# Font
font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 72)

# ---------- Helper functions ----------
def reset_game():
    global player_y, player_vel_y, obstacles, score, spawn_timer, game_over, on_ground
    player_y = GROUND_Y - PLAYER_HEIGHT
    player_vel_y = 0
    obstacles.clear()
    score = 0
    spawn_timer = 0
    game_over = False
    on_ground = True

def draw_player():
    # Body
    pygame.draw.rect(screen, PLAYER_COLOR, (PLAYER_X, player_y, PLAYER_WIDTH, PLAYER_HEIGHT))
    # Shirt/overalls
    pygame.draw.rect(screen, (80, 130, 255), (PLAYER_X + 5, player_y + 22, 22, 15))
    # Face
    pygame.draw.rect(screen, (255, 220, 180), (PLAYER_X + 5, player_y + 5, 8, 8))
    pygame.draw.rect(screen, (255, 220, 180), (PLAYER_X + 19, player_y + 5, 8, 8))
    # Eyes
    pygame.draw.rect(screen, BLACK, (PLAYER_X + 7, player_y + 7, 2, 2))
    pygame.draw.rect(screen, BLACK, (PLAYER_X + 23, player_y + 7, 2, 2))
    # Mustache
    pygame.draw.rect(screen, DARK_BROWN, (PLAYER_X + 8, player_y + 12, 16, 3))
    # Hat
    pygame.draw.rect(screen, DARK_BROWN, (PLAYER_X + 2, player_y - 2, 28, 8))

def draw_obstacle(obs):
    x, y, w, h = obs
    pygame.draw.rect(screen, (70, 160, 90), (x, y, w, h))
    pygame.draw.rect(screen, (110, 210, 120), (x, y, w, 5))
    # Brick details
    for i in range(1, int(w / 8)):
        pygame.draw.rect(screen, (90, 190, 110), (x + i * 8, y + 10, 4, h - 12))

def draw_ground():
    pygame.draw.rect(screen, BG_GROUND, (0, GROUND_Y + PLAYER_HEIGHT, WIDTH, HEIGHT - GROUND_Y - PLAYER_HEIGHT))
    pygame.draw.rect(screen, (100, 80, 50), (0, GROUND_Y + PLAYER_HEIGHT, WIDTH, 10))

def draw_background():
    screen.fill(BG_SKY)

    # Clouds
    for x in [80, 320, 600, 760]:
        pygame.draw.ellipse(screen, WHITE, (x, 60, 70, 30))
        pygame.draw.ellipse(screen, WHITE, (x + 25, 45, 60, 35))
        pygame.draw.ellipse(screen, WHITE, (x + 50, 55, 60, 30))

    # Mountains
    for x in [0, 220, 450, 720]:
        pygame.draw.polygon(screen, (110, 120, 140), [(x, 300), (x + 80, 180), (x + 160, 300)])

def draw_score():
    text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(text, (20, 20))

def draw_game_over():
    text = big_font.render("Game Over", True, (180, 20, 20))
    screen.blit(text, (300, 130))

    restart = font.render("Press R to restart", True, BLACK)
    screen.blit(restart, (330, 210))

# ---------- Main loop ----------
reset_game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                reset_game()

    keys = pygame.key.get_pressed()

    if not game_over:
        # Jump
        if keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]:
            if on_ground:
                player_vel_y = jump_power
                on_ground = False

        # Physics
        player_vel_y += gravity
        player_y += player_vel_y

        if player_y >= GROUND_Y - PLAYER_HEIGHT:
            player_y = GROUND_Y - PLAYER_HEIGHT
            player_vel_y = 0
            on_ground = True

        # Spawn obstacles
        if spawn_timer <= 0:
            height = random.randint(30, 70)
            width = random.randint(20, 35)
            x = WIDTH + 20
            y = GROUND_Y - height + PLAYER_HEIGHT
            obstacles.append([x, y, width, height])
            spawn_timer = random.randint(60, 110)
        else:
            spawn_timer -= 1

        # Move obstacles
        speed = 6 + (score // 800)
        for obs in obstacles:
            obs[0] -= speed

        # Remove offscreen obstacles
        obstacles = [obs for obs in obstacles if obs[0] + obs[2] > 0]

        # Score
        score += 1

        # Collision detection
        player_rect = pygame.Rect(PLAYER_X, player_y, PLAYER_WIDTH, PLAYER_HEIGHT)
        for obs in obstacles:
            obs_rect = pygame.Rect(obs[0], obs[1], obs[2], obs[3])
            if player_rect.colliderect(obs_rect):
                game_over = True

    # Draw everything
    draw_background()
    draw_ground()
    draw_player()

    for obs in obstacles:
        draw_obstacle(obs)

    draw_score()

    if game_over:
        draw_game_over()

    pygame.display.flip()
    clock.tick(60)