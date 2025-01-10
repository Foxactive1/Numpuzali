import pygame
import random
import sys

# Configurações iniciais
pygame.init()
WIDTH, HEIGHT = 600, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_COLOR = (50, 50, 50)
BG_COLOR = (200, 200, 200)
TIMER_COLOR = (200, 50, 50)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Numpuz")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 60)
small_font = pygame.font.Font(None, 40)

def draw_board(board, size):
    """Desenha o tabuleiro no Pygame."""
    tile_size = WIDTH // size
    screen.fill(BG_COLOR)
    for i in range(size):
        for j in range(size):
            num = board[i][j]
            if num != 0:
                rect = pygame.Rect(j * tile_size, i * tile_size, tile_size, tile_size)
                pygame.draw.rect(screen, WHITE, rect)
                pygame.draw.rect(screen, BLACK, rect, 3)
                text = font.render(str(num), True, FONT_COLOR)
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)

def find_empty_tile(board):
    """Encontra a posição do espaço vazio (0)."""
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                return i, j

def move_tile(board, x, y, new_x, new_y):
    """Move o espaço vazio para a nova posição."""
    board[x][y], board[new_x][new_y] = board[new_x][new_y], board[x][y]

def generate_board(size):
    """Gera um tabuleiro inicial embaralhado."""
    numbers = list(range(size * size))
    random.shuffle(numbers)
    while not is_solvable(numbers, size):
        random.shuffle(numbers)
    return [numbers[i:i + size] for i in range(0, size * size, size)]

def is_solvable(numbers, size):
    """Verifica se o tabuleiro é resolvível."""
    inversions = 0
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            if numbers[i] > numbers[j] and numbers[i] != 0 and numbers[j] != 0:
                inversions += 1
    empty_row = size - 1 - (numbers.index(0) // size)
    return (inversions % 2 == 0) if size % 2 == 1 else (empty_row % 2 == 0) == (inversions % 2 == 1)

def is_solved(board):
    """Verifica se o jogador resolveu o quebra-cabeça."""
    correct = list(range(1, len(board) * len(board))) + [0]
    flat_board = [num for row in board for num in row]
    return flat_board == correct

def get_tile_from_pos(pos, size):
    """Obtém a posição do tile com base no toque do usuário."""
    tile_size = WIDTH // size
    x, y = pos
    row = y // tile_size
    col = x // tile_size
    return row, col

def draw_timer(remaining_time):
    """Desenha o cronômetro na tela."""
    minutes = remaining_time // 60
    seconds = remaining_time % 60
    timer_text = small_font.render(f"Tempo: {minutes:02}:{seconds:02}", True, TIMER_COLOR)
    screen.blit(timer_text, (10, HEIGHT - 40))

def select_difficulty():
    """Permite ao jogador selecionar o nível de dificuldade."""
    options = [("Fácil (3x3)", 3), ("Médio (4x4)", 4), ("Difícil (5x5)", 5), ("Extremo (6x6)", 6)]
    while True:
        screen.fill(BG_COLOR)
        title = font.render("Selecione a dificuldade:", True, FONT_COLOR)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))
        for idx, (label, _) in enumerate(options):
            text = small_font.render(f"{idx + 1}. {label}", True, FONT_COLOR)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 150 + idx * 60))

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                    return options[event.key - pygame.K_1][1]

def main():
    """Loop principal do jogo."""
    size = select_difficulty()
    board = generate_board(size)
    total_time = 10 * 60 if size == 6 else None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                row, col = get_tile_from_pos(event.pos, size)
                empty_x, empty_y = find_empty_tile(board)

                if (abs(row - empty_x) == 1 and col == empty_y) or (abs(col - empty_y) == 1 and row == empty_x):
                    move_tile(board, empty_x, empty_y, row, col)

        if is_solved(board):
            screen.fill(BG_COLOR)
            text = font.render("Você venceu!", True, FONT_COLOR)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text, text_rect)
            pygame.display.flip()
            pygame.time.wait(3000)
            break

        screen.fill(BG_COLOR)
        draw_board(board, size)
        if total_time:
            draw_timer(total_time)
            total_time -= 1 / FPS
            if total_time <= 0:
                text = font.render("Tempo esgotado!", True, TIMER_COLOR)
                screen.blit(text, text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
                pygame.display.flip()
                pygame.time.wait(3000)
                break

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()