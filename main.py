import random

import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
GROUND_HEIGHT = 80
FPS = 60
GRAVITY = 0.42
FLAP_STRENGTH = -8.5
PIPE_WIDTH = 80
PIPE_GAP = 170
PIPE_SPEED = 3.5
PIPE_INTERVAL = 1500

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 28)


def reset_game():
    global bird, pipes, score, started, game_over, last_pipe_spawn
    bird = {
        "x": 150,
        "y": HEIGHT * 0.45,
        "radius": 16,
        "velocity": 0,
    }
    pipes = []
    score = 0
    started = False
    game_over = False
    last_pipe_spawn = 0


reset_game()


def spawn_pipe():
    min_top = 80
    max_top = HEIGHT - GROUND_HEIGHT - PIPE_GAP - 80
    top_height = random.randint(min_top, max_top)
    pipes.append({
        "x": WIDTH + 40,
        "top_height": top_height,
        "passed": False,
    })


def draw_background():
    screen.fill((135, 206, 235))

    for i in range(0, WIDTH + 100, 60):
        pygame.draw.circle(screen, (255, 255, 255), (i, 70), 20)

    pygame.draw.rect(screen, (110, 200, 80), (0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT))
    pygame.draw.rect(screen, (120, 90, 40), (0, HEIGHT - GROUND_HEIGHT, WIDTH, 10))


def draw_bird():
    x, y, radius = bird["x"], bird["y"], bird["radius"]
    pygame.draw.circle(screen, (255, 230, 80), (int(x), int(y)), radius)
    pygame.draw.circle(screen, (0, 0, 0), (int(x - 5), int(y - 5)), 3)
    pygame.draw.circle(screen, (0, 0, 0), (int(x + 5), int(y - 5)), 3)
    pygame.draw.arc(screen, (0, 0, 0), (x - 10, y - 5, 20, 20), 3.2, 6.2, 2)


def draw_pipes():
    for pipe in pipes:
        top_height = pipe["top_height"]
        bottom_y = top_height + PIPE_GAP

        pygame.draw.rect(screen, (40, 180, 70), (pipe["x"], 0, PIPE_WIDTH, top_height))
        pygame.draw.rect(screen, (40, 180, 70), (pipe["x"], bottom_y, PIPE_WIDTH, HEIGHT - GROUND_HEIGHT - bottom_y))

        pygame.draw.rect(screen, (90, 220, 110), (pipe["x"] - 5, top_height - 20, PIPE_WIDTH + 10, 20))
        pygame.draw.rect(screen, (90, 220, 110), (pipe["x"] - 5, bottom_y, PIPE_WIDTH + 10, 20))


def draw_score():
    label = font.render(str(score), True, (255, 255, 255))
    screen.blit(label, (WIDTH // 2 - 20, 40))


def draw_start_screen():
    title = font.render("Flappy Bird", True, (255, 255, 255))
    subtitle = small_font.render("Press SPACE to fap", True, (255, 255, 255))
    screen.blit(title, (WIDTH // 2 - 120, HEIGHT // 2 - 80))
    screen.blit(subtitle, (WIDTH // 2 - 110, HEIGHT // 2))


def draw_game_over():
    game_over_text = font.render("Game Over", True, (255, 255, 255))
    restart_text = small_font.render("Press SPACE to retry", True, (255, 255, 255))
    screen.blit(game_over_text, (WIDTH // 2 - 110, HEIGHT // 2 - 50))
    screen.blit(restart_text, (WIDTH // 2 - 120, HEIGHT // 2 + 20))


def handle_flap():
    global started
    if game_over:
        reset_game()
        return

    if not started:
        started = True

    bird["velocity"] = FLAP_STRENGTH


def check_collision():
    global game_over
    if bird["y"] - bird["radius"] <= 0:
        bird["y"] = bird["radius"]
        bird["velocity"] = 0

    if bird["y"] + bird["radius"] >= HEIGHT - GROUND_HEIGHT:
        bird["y"] = HEIGHT - GROUND_HEIGHT - bird["radius"]
        game_over = True

    for pipe in pipes:
        left = pipe["x"]
        right = pipe["x"] + PIPE_WIDTH
        bird_left = bird["x"] - bird["radius"]
        bird_right = bird["x"] + bird["radius"]

        if bird_right > left and bird_left < right:
            if bird["y"] - bird["radius"] < pipe["top_height"] or bird["y"] + bird["radius"] > pipe["top_height"] + PIPE_GAP:
                game_over = True

        if not pipe["passed"] and pipe["x"] + PIPE_WIDTH < bird["x"]:
            pipe["passed"] = True
            if not game_over:
                global score
                score += 1


running = True
while running:
    dt = clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_UP):
                handle_flap()

        if event.type == pygame.MOUSEBUTTONDOWN:
            handle_flap()

    if started and not game_over:
        bird["velocity"] += GRAVITY
        bird["y"] += bird["velocity"]

        last_pipe_spawn += dt
        if last_pipe_spawn >= PIPE_INTERVAL:
            spawn_pipe()
            last_pipe_spawn = 0

        for pipe in pipes:
            pipe["x"] -= PIPE_SPEED

        check_collision()

    if game_over:
        bird["velocity"] = 0

    draw_background()
    draw_pipes()
    draw_bird()
    draw_score()

    if not started and not game_over:
        draw_start_screen()
    elif game_over:
        draw_game_over()

    pygame.display.flip()

pygame.quit() 