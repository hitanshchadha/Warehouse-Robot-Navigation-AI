import pygame
import collections
import time
import sys

GRID_SIZE = 10  # 10x10 grid
CELL_SIZE = 60
WINDOW = GRID_SIZE * CELL_SIZE
FPS = 20  # animation speed can be controlled by adjusting FPS

pygame.init()
SCREEN = pygame.display.set_mode((WINDOW, WINDOW))
CLOCK = pygame.time.Clock()
FONT = pygame.font.SysFont("Arial", 20, bold=True)


def draw_grid_base(screen, start, items, delivery, obstacles, explored_set, frontier_q):
    screen.fill((0, 0, 0))

    for r, c in explored_set:
        if (r, c) != start and (r, c) not in items and (r, c) != delivery:
            pygame.draw.rect(screen, (100, 205, 255), (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    for pos, _ in frontier_q:
        if pos not in items and pos != delivery:
             pygame.draw.rect(screen, (0, 255, 255), (pos[1] * CELL_SIZE, pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    for x in range(0, WINDOW, CELL_SIZE):
        pygame.draw.line(screen, (255, 255, 255), (x, 0), (x, WINDOW))
    for y in range(0, WINDOW, CELL_SIZE):
        pygame.draw.line(screen, (255, 255, 255), (0, y), (WINDOW, y))

    for (r, c) in obstacles:
        pygame.draw.rect(screen, (220, 20, 60), (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    draw_special_cell(screen, start, (0, 0, 255), "R")
    
    if type(items) is tuple:
        draw_special_cell(screen, items, (0, 200, 0), "I")
    else:
        for item in items:
            draw_special_cell(screen, item, (0, 200, 0), "I")
        
    draw_special_cell(screen, delivery, (40, 40, 40), "D")

def draw_special_cell(screen, pos, color, label):
    r, c = pos
    pygame.draw.rect(screen, color, (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    text = FONT.render(label, True, (255, 255, 255))
    text_rect = text.get_rect(center=(c * CELL_SIZE + CELL_SIZE//2, r * CELL_SIZE + CELL_SIZE//2))
    screen.blit(text, text_rect)

def handle_pygame_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

def draw_lines(screen, current_path):
    pygame.draw.lines(screen, (255, 255, 0), False, [(c*CELL_SIZE + CELL_SIZE//2, r*CELL_SIZE+ 15 + CELL_SIZE//2) for (r, c) in current_path], 5)

def draw_final_path(difficulty, final_path, robot_start, item_loc, del_loc, obstacles):
    draw_grid_base(SCREEN, robot_start, [item_loc], del_loc, obstacles, set(), []) 
    draw_lines(SCREEN, final_path)

    font = pygame.font.SysFont(None, 28)
    info_text = f" {difficulty} Case Optimal Path: {len(final_path)-1} steps "
    text_surface = font.render(info_text, True, (255, 255, 255), (0, 0, 0))
            
    screen_rect = SCREEN.get_rect()
    text_rect = text_surface.get_rect(midbottom=(screen_rect.centerx, screen_rect.bottom - 10))
            
    SCREEN.blit(text_surface, text_rect)