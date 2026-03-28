
# AI Assignment (Group 22)
# Hitansh Chadha - 2022A8PS1255P
# Vedant Mathur - 2022A3PS0375P
# Krishna Raghunath - 2023A1PS0213P

import pygame
import sys

import bfs
import ucs
import astar
import idastar
pygame.init()

WIDTH, HEIGHT = 600, 600 
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu")

TITLE_FONT = pygame.font.SysFont("Verdana",35, bold=True)
BUTTON_FONT = pygame.font.SysFont("Verdana", 18)

def draw_button(screen, text, x, y, w, h, mouse_pos):
    rect = pygame.Rect(x, y, w, h)
    if rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, (170, 170, 170), rect, border_radius=20)
    else:
        pygame.draw.rect(screen, (200, 200, 200), rect, border_radius=20)

    text_surf = BUTTON_FONT.render(text, True, (0, 0, 0))
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)
    
    return rect

def main_menu():
    running = True
    btn_w, btn_h = 350, 50
    btn_x = (WIDTH - btn_w) // 2 
    btn1_y = 220
    btn2_y = 300
    btn3_y = 380
    btn4_y = 460
    
    while running:
        SCREEN.fill((0, 0, 0))
        mouse_pos = pygame.mouse.get_pos()
        
        title_surf = TITLE_FONT.render("Warehouse Robot Navigation", True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(WIDTH//2, 90))

        SCREEN.blit(title_surf, title_rect)
        bottom_surf = BUTTON_FONT.render("AI Assignment (Group 22)", True, (255, 255, 255))
        bottom_rect = title_surf.get_rect(center=(170+WIDTH//2, 150))
        SCREEN.blit(bottom_surf, bottom_rect)
        
        btn1 = draw_button(SCREEN, "1. Run BFS (Single Item)", btn_x, btn1_y, btn_w, btn_h, mouse_pos)
        btn2 = draw_button(SCREEN, "2. Run UCS (Multi-Item)", btn_x, btn2_y, btn_w, btn_h, mouse_pos)
        btn3 = draw_button(SCREEN, "3. Run A* (Manhattan Distance)", btn_x, btn3_y, btn_w, btn_h, mouse_pos)
        btn4 = draw_button(SCREEN, "4. Run IDA* (MST)", btn_x, btn4_y, btn_w, btn_h, mouse_pos)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if btn1.collidepoint(mouse_pos):
                        return "bfs"
                    elif btn2.collidepoint(mouse_pos):
                        return "ucs"
                    elif btn3.collidepoint(mouse_pos):
                        return "astar"
                    elif btn4.collidepoint(mouse_pos):
                        return "idastar"
                        
        pygame.display.flip()

def run_bfs():
    bfs.main()

def run_ucs():
    ucs.main()

def run_astar():
    astar.main()

def run_idastar():
    idastar.main()


if __name__ == "__main__":
    selected_option = main_menu()
    if selected_option == "bfs":
        run_bfs()
    elif selected_option == "ucs":
        run_ucs()
    elif selected_option == "astar":
        run_astar()
    elif selected_option == "idastar":
        run_idastar()