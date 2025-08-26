import pygame
import random
import sys

# --- Setup ---
pygame.init()
WIDTH, HEIGHT = 600, 700
ROWS, COLS = 3, 3
TILE_SIZE = WIDTH // COLS

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bombs & Potions")

font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 32)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 100, 100)
BLUE = (100, 100, 255)

# --- Game State ---
board = {}  # tile -> "bomb"/"potion"
for r in range(ROWS):
    for c in range(COLS):
        board[(r, c)] = random.choice(["bomb", "potion"])

used_tiles = {}
players = {"P1": 10, "P2": 10}
turn_order = ["P1", "P2"]
turn = 0
game_over = False


# --- Helper Functions ---
def draw_board():
    screen.fill(WHITE)

    # Draw grid
    for r in range(ROWS):
        for c in range(COLS):
            rect = pygame.Rect(c*TILE_SIZE, r*TILE_SIZE+100, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, GRAY, rect, 3)

            if (r, c) in used_tiles:
                player = used_tiles[(r, c)]
                text = font.render(player, True, BLUE if player == "P1" else RED)
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)

    # Draw HP
    hp_text = small_font.render(f"P1 HP: {players['P1']}   P2 HP: {players['P2']}", True, BLACK)
    screen.blit(hp_text, (20, 20))

    # Show turn or winner
    if not game_over:
        t = turn_order[turn % 2]
        turn_text = small_font.render(f"{t}'s turn", True, BLACK)
        screen.blit(turn_text, (20, 60))
    else:
        p1, p2 = players["P1"], players["P2"]
        if p1 > p2:
            msg = "P1 Wins!"
        elif p2 > p1:
            msg = "P2 Wins!"
        else:
            msg = "Draw!"
        msg_text = font.render(msg, True, BLACK)
        screen.blit(msg_text, (WIDTH//2 - msg_text.get_width()//2, 50))


def handle_click(pos):
    global turn, game_over
    if game_over:
        return

    x, y = pos
    if y < 100:  # Ignore clicks above grid
        return

    row = (y-100) // TILE_SIZE
    col = x // TILE_SIZE
    if row >= ROWS or col >= COLS:
        return

    if (row, col) in used_tiles:
        return  # Already taken

    current = turn_order[turn % 2]
    used_tiles[(row, col)] = current
    result = board[(row, col)]

    if result == "bomb":
        players[current] -= 3
    else:
        players[current] += 2

    # Check for game end
    if len(used_tiles) == ROWS*COLS or players["P1"] <= 0 or players["P2"] <= 0:
        game_over = True

    turn += 1


# --- Main Loop ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_click(event.pos)

    draw_board()
    pygame.display.flip()

pygame.quit()
sys.exit()
