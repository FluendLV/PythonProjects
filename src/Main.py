import pygame
import time
import random

# initialize pygame library
pygame.init()

# set game window dimensions
WIDTH, HEIGHT = 500, 500
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Nim Game")

# define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# set font
FONT = pygame.font.SysFont("calibri", 32)

# set game variables
HEAP_SIZE = 25
TURN = 0
AI_TURN = 2
HUMAN_TURN = 1
AI_START = False

# define functions
def draw_text(text, font, color, x, y):
    """function to draw text"""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    WINDOW.blit(text_surface, text_rect)

def draw_stones(stones):
    """function to draw stones"""
    x, y = 250, 200
    draw_text(str(stones) + " stones remaining", FONT, BLACK, x, y)

def clear_Area(stones):
    WINDOW.fill(WHITE, (100, 180, 400, 100))
    draw_stones(stones)

def get_ai_move(stones, currentTurn):
    global AI_START
    print("Stones: ", stones)
    """function to get AI move using minimax algorithm"""
    if currentTurn == 2 and stones == 25:
        AI_START = True

    if stones < 4:
        return stones
    else:
        best_move = None
        best_score = float('-inf')
        for move in range(1, 4):
            new_stones = stones - move
            print(AI_START)
            score = minimax(new_stones, not AI_START)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

def minimax(stones, is_maximizing):
    """function to calculate minimax score"""
    if stones == 0:
        if is_maximizing:
            return -1
        else:
            return 1
    elif stones < 0:
        return float('-inf') if is_maximizing else float('inf')
    elif is_maximizing:
        max_score = float('-inf')
        for move in range(1, 4):
            score = minimax(stones - move, False)
            max_score = max(max_score, score)
        return max_score
    else:
        min_score = float('inf')
        for move in range(1, 4):
            score = minimax(stones - move, True)
            min_score = min(min_score, score)
        return min_score

def nim_game():
    """function to play nim game"""
    # initialize game variable
    stones = HEAP_SIZE
    winner = None
    TURN = 0

    # menu screen loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if x > 100 and x < 400 and y > 250 and y < 350:
                    TURN = HUMAN_TURN
                    break
                elif x > 100 and x < 400 and y > 350 and y < 450:
                    TURN = AI_TURN
                    break

        # draw menu screen
        WINDOW.fill(WHITE)
        draw_text("Nim Game", FONT, BLACK, 250, 50)
        draw_text("Who goes first?", FONT, BLACK, 250, 150)
        draw_text("Player", FONT, BLACK, 250, 300)
        draw_text("AI", FONT, BLACK, 250, 400)
        pygame.display.update()

        if TURN != 0:
            break

    # game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and winner is None and TURN == HUMAN_TURN:
                x, y = pygame.mouse.get_pos()
                pygame.display.update()
                draw_stones(stones)
                if x > 100 and x < 200 and y > 350 and y < 450:
                    stones -= 1
                    clear_Area(stones)
                    pygame.display.update()
                    if stones <= 0:
                        winner = "HUMAN"
                        WINDOW.fill(WHITE)
                        draw_text(f"{winner} wins!", FONT, BLACK, WIDTH // 2, HEIGHT // 2)
                        pygame.display.update()
                        time.sleep(3)

                    TURN = AI_TURN
                    print(stones)
                elif x > 200 and x < 300 and y > 350 and y < 450:
                    stones -= 2
                    if stones <= 0:
                        winner = "HUMAN"
                        WINDOW.fill(WHITE)
                        draw_text(f"{winner} wins!", FONT, BLACK, WIDTH // 2, HEIGHT // 2)
                        pygame.display.update()
                        time.sleep(3)
                        stones = 25

                    clear_Area(stones)
                    TURN = AI_TURN
                    print(stones)
                elif x > 300 and x < 400 and y > 350 and y < 450:
                    stones -= 3
                    if stones <= 0:
                        winner = "HUMAN"
                        WINDOW.fill(WHITE)
                        draw_text(f"{winner} wins!", FONT, BLACK, WIDTH // 2, HEIGHT // 2)
                        pygame.display.update()
                        time.sleep(5)
                        stones = 25

                    clear_Area(stones)
                    TURN = AI_TURN
                    print(stones)

        # AI move
        if TURN == AI_TURN and winner is None:
            WINDOW.fill(WHITE, (100, 230, 400, 100))
            draw_text("AI is thinking...", FONT, BLACK, 250, 250)
            pygame.display.update()
            time.sleep(2)
            move = get_ai_move(stones, TURN)
            stones -= move
            if stones <= 0:
                    winner = "AI"
                    WINDOW.fill(WHITE)
                    draw_text(f"{winner} wins!", FONT, BLACK, WIDTH // 2, HEIGHT // 2)
                    pygame.display.update()
                    time.sleep(3)
            TURN = HUMAN_TURN
            print(stones)


        # draw game window
        WINDOW.fill(WHITE)
        draw_text("Nim Game", FONT, BLACK, 250, 50)
        draw_stones(stones)
        draw_text("1", FONT, BLACK, 150, 400)
        draw_text("2", FONT, BLACK, 250, 400)
        draw_text("3", FONT, BLACK, 350, 400)

        if TURN == HUMAN_TURN:
            draw_text("Your turn", FONT, BLACK, 250, 250)
        else:
            draw_text("AI is thinking...", FONT, BLACK, 250, 250)

        pygame.display.update()

    # quit pygame
    pygame.quit()

# start the game
nim_game()
