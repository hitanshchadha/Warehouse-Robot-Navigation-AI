
# AI Assignment (Group 22)
# Hitansh Chadha - 2022A8PS1255P
# Vedant Mathur - 2022A3PS0375P
# Krishna Raghunath - 2023A1PS0213P

from grid import create_grid
import pygame
import heapq

def ucs(screen, start, items_to_coll, delivery, obstacles):
    
    target_items = frozenset(items_to_coll) 
    initial_coll = frozenset() 
    
    counter = 0
    pq = [(0, counter, start, initial_coll, [start])]
    
    exp_set = set()
    dir = [(-1, 0), (1, 0), (0, -1), (0, 1)] 

    while pq:
        create_grid.handle_pygame_events()

        cost, _, curr_pos, coll, curr_path = heapq.heappop(pq)

        if curr_pos == delivery and coll == target_items:
            return curr_path 

        state = (curr_pos, coll)

        if state not in exp_set:
            exp_set.add(state)
            
            create_grid.draw_grid_base(screen, start, items_to_coll, delivery, obstacles, {s[0] for s in exp_set}, [(item[2], None) for item in pq])
            
            if len(curr_path) > 1:
                create_grid.draw_lines(screen, curr_path)
            
            pygame.display.flip()
            create_grid.CLOCK.tick(create_grid.FPS)
            
            next_coll = coll
            if curr_pos in target_items and curr_pos not in coll:
                next_coll = coll | frozenset([curr_pos])

            for dx, dy in dir:
                nx, ny = curr_pos[0] + dx, curr_pos[1] + dy
                
                if 0 <= nx < create_grid.GRID_SIZE and 0 <= ny < create_grid.GRID_SIZE and (nx, ny) not in obstacles:
                    next_state = ((nx, ny), next_coll)
                    
                    if next_state not in exp_set:
                        counter += 1
                        step_cost = 1
                        heapq.heappush(pq, (cost + step_cost, counter, (nx, ny), next_coll, curr_path + [(nx, ny)]))

    return None

def main():
    test_cases = [
        {
            "difficulty": "Easy",
            "start": (0, 0),
            "items": [(2, 2)],
            "delivery": (4, 4),
            "obstacles": [(1, 2), (2, 1), (3, 3)] 
        },
        {
            "difficulty": "Medium",
            "start": (0, 0),
            "items": [(8, 2), (2, 8)],
            "delivery": (9, 9),
            # A wall forcing the search to expand around it
            "obstacles": [(4, y) for y in range(0, 8)] 
        },
        {
            "difficulty": "Hard",
            "start": (0, 0),
            "items": [(2, 7), (8, 2), (4, 6)],
            "delivery": (9, 9),
            # Complex barriers: L-shapes and dead ends
            "obstacles": [(x, 5) for x in range(2, 10)] + [(5, y) for y in range(0, 4)] + [(2, 8), (3, 8), (4, 8)]
        }
    ]

    for index, tc in enumerate(test_cases):
        difficulty = tc["difficulty"]
        robot_start = tc["start"]
        items = tc["items"]
        delivery_loc = tc["delivery"]
        obstacles = tc["obstacles"]

        final_path = ucs(
            create_grid.SCREEN, 
            robot_start, 
            items, 
            delivery_loc, 
            obstacles
        )
        
        if final_path:
            print(f"[{difficulty}] Optimal route found: {len(final_path)-1} total steps.")
            
            create_grid.draw_grid_base(
                create_grid.SCREEN, 
                robot_start, 
                items, 
                delivery_loc, 
                obstacles, 
                set(), 
                []
            ) 
            create_grid.draw_lines(create_grid.SCREEN, final_path)
            
            font = pygame.font.SysFont(None, 28)
            info_text = f" {difficulty} Case Optimal Path: {len(final_path)-1} steps "
            text_surface = font.render(info_text, True, (255, 255, 255), (0, 0, 0))
            
            screen_rect = create_grid.SCREEN.get_rect()
            text_rect = text_surface.get_rect(midbottom=(screen_rect.centerx, screen_rect.bottom - 10))
            
            create_grid.SCREEN.blit(text_surface, text_rect)
            
            pygame.display.set_caption(f"{difficulty} Mission Completed | Path: {len(final_path)-1} steps")
            pygame.display.flip()
            
        else:
            print(f"[{difficulty}] Route not found")
            pygame.display.set_caption(f"{difficulty} FAILED: Target is unreachable.")

        if index < len(test_cases) - 1:
            pygame.time.wait(5000)

    pygame.display.set_caption("All Test Cases Completed.")
    print("All missions completed.")
    
    while True:
        create_grid.handle_pygame_events()
        create_grid.CLOCK.tick(10)

if __name__ == "__main__":
    main()