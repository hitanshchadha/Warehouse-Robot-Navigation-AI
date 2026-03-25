from grid import create_grid
import pygame
import heapq

def ucs(screen, start, items_to_collect, delivery, obstacles):
    
    target_items = frozenset(items_to_collect) 
    initial_collected = frozenset() 
    
    counter = 0
    pq = [(0, counter, start, initial_collected, [start])]
    
    exp_set = set()
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] 

    while pq:
        create_grid.handle_pygame_events()

        cost, _, current_pos, collected, current_path = heapq.heappop(pq)

        if current_pos == delivery and collected == target_items:
            return current_path 

        state = (current_pos, collected)

        if state not in exp_set:
            exp_set.add(state)

            physical_exp_set = {s[0] for s in exp_set}
            physical_queue = [(item[2], None) for item in pq] 
            
            create_grid.draw_grid_base(screen, start, items_to_collect, delivery, obstacles, physical_exp_set, physical_queue)
            
            if len(current_path) > 1:
                create_grid.draw_lines(screen, current_path)
            
            pygame.display.flip()
            create_grid.CLOCK.tick(create_grid.FPS)
            
            next_collected = collected
            if current_pos in target_items and current_pos not in collected:
                next_collected = collected | frozenset([current_pos])

            for dx, dy in directions:
                nx, ny = current_pos[0] + dx, current_pos[1] + dy
                
                if 0 <= nx < create_grid.GRID_SIZE and 0 <= ny < create_grid.GRID_SIZE and (nx, ny) not in obstacles:
                    next_state = ((nx, ny), next_collected)
                    
                    if next_state not in exp_set:
                        counter += 1
                        step_cost = 1
                        heapq.heappush(pq, (cost + step_cost, counter, (nx, ny), next_collected, current_path + [(nx, ny)]))

    return None

def main():
    robot_start = (0, 0)
    items = [(2, 7), (8, 2), (4, 5)] 
    delivery_loc = (9, 9)

    mission_complete = False

    while not mission_complete:
        create_grid.handle_pygame_events()
        
        final_path = ucs(create_grid.SCREEN, robot_start, items, delivery_loc, create_grid.OBSTACLES)
        
        if final_path:
            print(f"optimal route found: {len(final_path)-1} total steps.")
            create_grid.draw_grid_base(create_grid.SCREEN, robot_start, items, delivery_loc, create_grid.OBSTACLES, set(), []) 
            create_grid.draw_lines(create_grid.SCREEN, final_path)
            pygame.display.flip()
            
            pygame.display.set_caption("mission Completed")
            print("mission Completed")
        else:
            print("Route not found")

        mission_complete = True
    while True:
        create_grid.handle_pygame_events()
        create_grid.CLOCK.tick(10)

if __name__ == "__main__":
    main()