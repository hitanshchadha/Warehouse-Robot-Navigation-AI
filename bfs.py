
# AI Assignment (Group 22)
# Hitansh Chadha - 2022A8PS1255P
# Vedant Mathur - 2022A3PS0375P
# Krishna Raghunath - 2023A1PS0213P

from grid import create_grid
import pygame
import collections

def bfs(screen, start, item_loc, del_loc, obstacles):
    frontier_q = collections.deque([(start, False, [start])])
    
    explored = set()
    
    for o in obstacles:
        explored.add((o, False))
        explored.add((o, True))

    dir = [(-1, 0), (1, 0), (0, -1), (0, 1)] 

    while frontier_q:        
        create_grid.handle_pygame_events()
        
        current_pos, has_item, current_path = frontier_q.popleft()

        if current_pos == del_loc and has_item:
            return current_path 

        state = (current_pos, has_item)
        if state in explored:
            continue
            
        explored.add(state)

        physical_explored = {s[0] for s in explored}
        physical_q = [(item[0], item[2]) for item in frontier_q] 
        
        create_grid.draw_grid_base(screen, start, [item_loc], del_loc, obstacles, physical_explored, physical_q)
        
        if len(current_path) > 1:
            create_grid.draw_lines(screen, current_path)
        
        if has_item:
            pygame.display.set_caption("Phase 2: Item Acquired! Searching for Delivery...")
        else:
            pygame.display.set_caption("Phase 1: Searching for Item...")
            
        pygame.display.flip()
        create_grid.CLOCK.tick(create_grid.FPS) 

        for dx, dy in dir:
            nx, ny = current_pos[0] + dx, current_pos[1] + dy
            
            if 0 <= nx < create_grid.GRID_SIZE and 0 <= ny < create_grid.GRID_SIZE:
                
                next_has_item = has_item
                if (nx, ny) == item_loc:
                    next_has_item = True
                    
                next_state = ((nx, ny), next_has_item)
                
                if next_state not in explored:
                    frontier_q.append(((nx, ny), next_has_item, current_path + [(nx, ny)]))

    return None

def main():
    test_cases = [
        {
            "difficulty": "Easy",
            "start": (0, 0),
            "item": (2, 2),
            "delivery": (4, 4),
            "obstacles": [(1, 2), (2, 1), (3, 3)]
        },
        {
            "difficulty": "Medium",
            "start": (0, 0),
            "item": (8, 2),
            "delivery": (0, 9),
            # wall blocking the direct path,  robot will go around
            "obstacles": [(4, y) for y in range(0, 8)] 
        },
        {
            "difficulty": "Hard",
            "start": (0, 0),
            "item": (9, 9),
            "delivery": (0, 9),
            # an L-shape and dead end barrier
            "obstacles": [(x, 5) for x in range(2, 10)] + [(5, y) for y in range(0, 4)] + [(2, 7), (3, 7), (4, 7)]
        }
    ]

    for index, tc in enumerate(test_cases):
        difficulty = tc["difficulty"]
        robot_start = tc["start"]
        item_loc = tc["item"]
        del_loc = tc["delivery"]
        obstacles = tc["obstacles"]

        final_path = bfs(create_grid.SCREEN, robot_start, item_loc, del_loc, obstacles)
        
        if final_path:
            create_grid.draw_grid_base(create_grid.SCREEN, robot_start, [item_loc], del_loc, obstacles, set(), []) 
            create_grid.draw_lines(create_grid.SCREEN, final_path)

            font = pygame.font.SysFont(None, 28)
            info_text = f" {difficulty} Case Optimal Path: {len(final_path)-1} steps "
            text_surface = font.render(info_text, True, (255, 255, 255), (0, 0, 0))
            
            screen_rect = create_grid.SCREEN.get_rect()
            text_rect = text_surface.get_rect(midbottom=(screen_rect.centerx, screen_rect.bottom - 10))
            
            create_grid.SCREEN.blit(text_surface, text_rect)
            
            pygame.display.set_caption(f"{difficulty} Completed | Optimal Path: {len(final_path)-1} steps.")
            pygame.display.flip()
        else:
            pygame.display.set_caption(f"{difficulty} FAILED")

        if index < len(test_cases) - 1:
            pygame.time.wait(5000) 

    pygame.display.set_caption("Completed.")
    while True:
        create_grid.handle_pygame_events()
        create_grid.CLOCK.tick(10)

if __name__ == "__main__":
    main()