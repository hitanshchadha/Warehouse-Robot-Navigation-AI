import pygame
import collections
import time
import sys


GRID_SIZE = 10  # 10x10 grid
CELL_SIZE = 50
WINDOW = GRID_SIZE * CELL_SIZE
FPS = 20  # animation speed can be controlled by adjusting FPS

# colours (R, G, B)
WHITE      = (255, 255, 255)  
BLACK      = (0, 0, 0)        
DARK_GRAY  = (50, 50, 50)     
BLUE       = (0, 0, 255)      
GREEN      = (0, 200, 0)      
RED        = (220, 20, 60)   
CYAN       = (0, 255, 255)    
LIGHT_BLUE = (173, 216, 230)  
YELLOW     = (255, 255, 0)    

pygame.init()
SCREEN = pygame.display.set_mode((WINDOW, WINDOW))
CLOCK = pygame.time.Clock()
FONT = pygame.font.SysFont("Arial", 20, bold=True)

OBSTACLES = {
    (2, 2), (2, 3), (2, 4), (2, 5),
    (6, 7), (7, 7), (8, 7),         
    (4, 4), (5, 4), (5, 5),         
}

def draw_grid(screen, start, item, delivery, obstacles, explored_set, frontier_q):
    screen.fill(WHITE)

    for r, c in explored_set:
        if (r, c) != start and (r, c) != item and (r, c) != delivery:
            pygame.draw.rect(screen, LIGHT_BLUE, (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    for pos, _ in frontier_q:
        if pos != item and pos != delivery:
             pygame.draw.rect(screen, CYAN, (pos[1] * CELL_SIZE, pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    for x in range(0, WINDOW, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (x, 0), (x, WINDOW))
    for y in range(0, WINDOW, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (0, y), (WINDOW, y))

    for (r, c) in obstacles:
        pygame.draw.rect(screen, DARK_GRAY, (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    draw_special_cell(screen, start, BLUE, "R")
    draw_special_cell(screen, item, GREEN, "I")
    draw_special_cell(screen, delivery, RED, "D")

def draw_special_cell(screen, pos, color, label):
    r, c = pos
    pygame.draw.rect(screen, color, (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    text = FONT.render(label, True, WHITE)
    text_rect = text.get_rect(center=(c * CELL_SIZE + CELL_SIZE//2, r * CELL_SIZE + CELL_SIZE//2))
    screen.blit(text, text_rect)

def handle_pygame_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()