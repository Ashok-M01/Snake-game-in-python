import pygame
import random
import sys

pygame.init()

# --------------------
# Screen Settings
# --------------------
WIDTH = 1050
HEIGHT = 2100

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

CELL = 30

GRID_W = WIDTH // CELL
GRID_H = (HEIGHT - 250) // CELL

# --------------------
# Colors
# --------------------
BLACK = (20,20,20)
WHITE = (255,255,255)
GREEN = (0,220,0)
DARK_GREEN = (0,150,0)
RED = (255,60,60)
GRAY = (60,60,60)

font = pygame.font.SysFont(None, 40)

# --------------------
# Snake
# --------------------
snake = [
    (8,8),
    (7,8),
    (6,8)
]

direction = (1,0)

food = (
    random.randint(0,GRID_W-1),
    random.randint(0,GRID_H-1)
)

score = 0

FPS = 10

# --------------------
# Touch Buttons
# --------------------
BTN = 120

up_btn = pygame.Rect(
WIDTH//2-BTN//2,
HEIGHT-220,
BTN,
BTN)

down_btn = pygame.Rect(
WIDTH//2-BTN//2,
HEIGHT+40,
BTN,
BTN)

left_btn = pygame.Rect(
WIDTH//2-180,
HEIGHT-90,
BTN,
BTN)

right_btn = pygame.Rect(
WIDTH//2+60,
HEIGHT-90,
BTN,
BTN)

def draw_buttons():

    pygame.draw.rect(screen,GRAY,up_btn,border_radius=15)
    pygame.draw.rect(screen,GRAY,down_btn,border_radius=15)
    pygame.draw.rect(screen,GRAY,left_btn,border_radius=15)
    pygame.draw.rect(screen,GRAY,right_btn,border_radius=15)

    screen.blit(font.render("UP",True,WHITE),
        (up_btn.x+45,up_btn.y+45))

    screen.blit(font.render("DN",True,WHITE),
        (down_btn.x+45,down_btn.y+45))

    screen.blit(font.render("LT",True,WHITE),
        (left_btn.x+45,left_btn.y+45))

    screen.blit(font.render("RT",True,WHITE),
        (right_btn.x+45,right_btn.y+45))
        
# --------------------
# Draw Functions
# --------------------

def draw_grid():
    for x in range(0, WIDTH, CELL):
        pygame.draw.line(
            screen,
            (40, 40, 40),
            (x+CELL, 0),
            (x+CELL, GRID_H * CELL)
        )

    for y in range(0, GRID_H * CELL, CELL):
        pygame.draw.line(
            screen,
            (40, 40, 40),
            (0, y+CELL),
            (WIDTH, y+CELL)
        )


def draw_snake():
    for i, (x, y) in enumerate(snake):

        rect = pygame.Rect(
            x * CELL,
            y * CELL,
            CELL,
            CELL
        )

        if i == 0:
            pygame.draw.rect(
                screen,
                GREEN,
                rect,
                border_radius=8
            )
        else:
            pygame.draw.rect(
                screen,
                DARK_GREEN,
                rect,
                border_radius=6
            )


def draw_food():
    pygame.draw.circle(
        screen,
        RED,
        (
            food[0] * CELL + CELL // 2,
            food[1] * CELL + CELL // 2
        ),
        CELL // 2 - 2
    )


def draw_score():
    txt = font.render(
        f"Score : {score}",
        True,
        WHITE
    )
    screen.blit(txt, (20, 20))


def place_food():
    while True:
        pos = (
            random.randint(0, GRID_W - 1),
            random.randint(0, GRID_H - 1)
        )

        if pos not in snake:
            return pos
# --------------------
# Snake Movement
# --------------------

def move_snake():
    global snake, food, score

    head_x, head_y = snake[0]
    dx, dy = direction

    new_head = (head_x + dx, head_y + dy)

    # Wall collision
    if (new_head[0] < 0 or
        new_head[0] >= GRID_W or
        new_head[1] < 0 or
        new_head[1] >= GRID_H):
        return False

    # Self collision
    if new_head in snake:
        return False

    # Move snake
    snake.insert(0, new_head)

    # Eat food
    if new_head == food:
        score += 1
        food = place_food()

        # Increase speed
        global FPS
        FPS = min(FPS + 0.5, 25)

    else:
        snake.pop()

    return True
# --------------------
# Main Game Loop
# --------------------

running = True

while running:

    clock.tick(FPS)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:

            x, y = event.pos

            if up_btn.collidepoint(x, y):
                if direction != (0, 1):
                    direction = (0, -1)

            elif down_btn.collidepoint(x, y):
                if direction != (0, -1):
                    direction = (0, 1)

            elif left_btn.collidepoint(x, y):
                if direction != (1, 0):
                    direction = (-1, 0)

            elif right_btn.collidepoint(x, y):
                if direction != (-1, 0):
                    direction = (1, 0)

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP and direction != (0, 1):
                direction = (0, -1)

            elif event.key == pygame.K_DOWN and direction != (0, -1):
                direction = (0, 1)

            elif event.key == pygame.K_LEFT and direction != (1, 0):
                direction = (-1, 0)

            elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                direction = (1, 0)

    if not move_snake():
        running = False

    screen.fill(BLACK)

    draw_grid()
    draw_food()
    draw_snake()
    draw_score()
    draw_buttons()

    pygame.display.flip()
# --------------------
# Game Over & Restart
# --------------------

def reset_game():
    global snake, direction, food, score, FPS

    snake = [
        (8, 8),
        (7, 8),
        (6, 8)
    ]

    direction = (1, 0)

    food = place_food()

    score = 0

    FPS = 10


def game_over_screen():

    while True:

        screen.fill(BLACK)

        title = font.render(
            "GAME OVER",
            True,
            RED
        )

        score_txt = font.render(
            f"Score : {score}",
            True,
            WHITE
        )

        info = font.render(
            "Tap anywhere to restart",
            True,
            WHITE
        )

        screen.blit(
            title,
            (
                WIDTH//2 - title.get_width()//2,
                250
            )
        )

        screen.blit(
            score_txt,
            (
                WIDTH//2 - score_txt.get_width()//2,
                330
            )
        )

        screen.blit(
            info,
            (
                WIDTH//2 - info.get_width()//2,
                420
            )
        )

        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                reset_game()
                return

            elif event.type == pygame.KEYDOWN:
                reset_game()
                return
             
pygame.quit()
sys.exit()