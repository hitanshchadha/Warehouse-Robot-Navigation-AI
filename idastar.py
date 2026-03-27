
# AI Assignment (Group 22)
# Hitansh Chadha - 2022A8PS1255P
# Vedant Mathur - 2022A3PS0375P
# Krishna Raghunath - 2023A1PS0213P

from grid import create_grid
import pygame

def get_mst_heuristic(pos, uncollected_items, delivery):
    nodes = [pos] + list(uncollected_items) + [delivery]
    if not uncollected_items:
        return abs(pos[0] - delivery[0]) + abs(pos[1] - delivery[1])  
    connected = {0}
    unconnected = set(range(1, len(nodes)))
    mst_cost = 0
    while unconnected:
        min_dist = float('inf')
        best_node = None
        for u in connected:
            for v in unconnected:
                dist = abs(nodes[u][0] - nodes[v][0]) + abs(nodes[u][1] - nodes[v][1])
                if dist < min_dist:
                    min_dist = dist
                    best_node = v
                    
        mst_cost += min_dist
        connected.add(best_node)
        unconnected.remove(best_node)
        
    return mst_cost

def ida_star_mst_optimizer(screen, start, items_dict, delivery, obstacles, max_battery):
    target_items = frozenset(items_dict.keys())
    bound = get_mst_heuristic(start, target_items, delivery)
    best_score = -1
    best_path = None
    best_remaining_battery = -1
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    visual_counter = [0] 

    while True:
        visited_states = {}

        def search(path, g, current_bound, collected, battery, current_score):
            nonlocal best_score, best_path, best_remaining_battery

            create_grid.handle_pygame_events()
            node = path[-1]
            h = get_mst_heuristic(node, target_items - collected, delivery)
            f = g + h
            
            visual_counter[0] += 1
            if visual_counter[0] % 5 == 0: 
                physical_explored = {s[0] for s in visited_states.keys()}
                physical_queue = [(node, None)] 
                
                create_grid.draw_grid_base(screen, start, list(target_items), delivery, obstacles, physical_explored, physical_queue)
                if len(path) > 1:
                    create_grid.draw_lines(screen, path)
                
                pygame.display.set_caption(f"IDA* | Bound: {current_bound} | F-Cost: {f} | Best Score: {best_score}")
                pygame.display.flip()
                create_grid.CLOCK.tick(create_grid.FPS)

            if f > current_bound:
                return f
                
            if node == delivery:
                if current_score > best_score:
                    best_score = current_score
                    best_path = list(path)
                    best_remaining_battery = battery
                    print(f"New best route found! Score: {best_score} | Battery: {best_remaining_battery}")
                
                if len(collected) == len(target_items):
                    return "FOUND"
            
            min_f = float('inf')
            
            for dx, dy in directions:
                nx, ny = node[0] + dx, node[1] + dy
                
                if 0 <= nx < create_grid.GRID_SIZE and 0 <= ny < create_grid.GRID_SIZE and (nx, ny) not in obstacles:
                    new_battery = battery - 1
                    
                    survival_dist = abs(nx - delivery[0]) + abs(ny - delivery[1])
                    if new_battery < survival_dist:
                        continue
                        
                    next_collected = collected
                    new_score = current_score
                    
                    if (nx, ny) in target_items and (nx, ny) not in collected:
                        next_collected = collected | frozenset([(nx, ny)])
                        new_score += items_dict[(nx, ny)]
                        
                    state = ((nx, ny), next_collected)
                    new_g = g + 1
                    
                    if state in visited_states and visited_states[state] <= new_g:
                        continue
                        
                    visited_states[state] = new_g
                    path.append((nx, ny))

                    res = search(path, new_g, current_bound, next_collected, new_battery, new_score)
                    
                    if res == "FOUND":
                        return "FOUND"
                    if res < min_f:
                        min_f = res
                        
                    path.pop() 
                    
            return min_f

        visited_states[(start, frozenset())] = 0
        t = search([start], 0, bound, frozenset(), max_battery, 0)
        
        if t == "FOUND":
            break
        if t == float('inf'):
            print("Search exhausted. Battery limits reached.")
            break
            
        create_grid.draw_grid_base(screen, start, list(target_items), delivery, obstacles, set(), [])
        pygame.display.flip()
        pygame.time.delay(300)  
        bound = t 

    return best_path, best_remaining_battery, best_score

def main():
    test_cases = [
        {
            "difficulty": "Easy",
            "start": (0, 0),
            "items": {(2, 2): 10},
            "delivery": (4, 4),
            "obstacles": [(1, 2), (2, 1), (3, 3)],
            "battery": 20 # Plenty of battery for a single item
        },
        {
            "difficulty": "Medium",
            "start": (0, 0),
            "items": {(8, 2): 50, (2, 8): 20},
            "delivery": (9, 9),
            "obstacles": [(4, y) for y in range(0, 8)],
            "battery": 45 # Enough battery to sweep both items and reach delivery if the MST path is optimal
        },
        {
            "difficulty": "Hard",
            "start": (0, 0),
            "items": {(2, 7): 50, (8, 2): 10, (0, 9): 100},
            "delivery": (9, 9),
            "obstacles": [(x, 5) for x in range(2, 10)] + [(5, y) for y in range(0, 4)] + [(2, 8), (3, 8), (4, 8)],
            "battery": 55 # A strict limit for navigating the maze and picking up all 3 items
        }
    ]

    for index, tc in enumerate(test_cases):
        difficulty = tc["difficulty"]
        robot_start = tc["start"]
        items_with_priorities = tc["items"]
        delivery_loc = tc["delivery"]
        obstacles = tc["obstacles"]
        battery_capacity = tc["battery"]

        print("Starting {difficulty} Test Case")

        final_path, rem_battery, final_score = ida_star_mst_optimizer(create_grid.SCREEN, robot_start, items_with_priorities, delivery_loc, obstacles,battery_capacity)
        
        if final_path:
            print(f"[{difficulty}] Search Complete!")
            print(f"Total Score: {final_score}")
            print(f"Steps Taken: {len(final_path)-1}")
            print(f"Battery Remaining: {rem_battery}")
            
            items_list = list(items_with_priorities.keys())
            create_grid.draw_grid_base(create_grid.SCREEN, robot_start, items_list, delivery_loc, obstacles, set(), []) 
            create_grid.draw_lines(create_grid.SCREEN, final_path)
            
            font = pygame.font.SysFont(None, 28)
            info_text = f" {difficulty} Case | Score: {final_score} | Battery Left: {rem_battery} "
            text_surface = font.render(info_text, True, (255, 255, 255), (0, 0, 0))
            
            screen_rect = create_grid.SCREEN.get_rect()
            text_rect = text_surface.get_rect(midbottom=(screen_rect.centerx, screen_rect.bottom - 10))
            
            create_grid.SCREEN.blit(text_surface, text_rect)
            
            pygame.display.set_caption(f"{difficulty} DONE! Max Score: {final_score} | Battery: {rem_battery}")
            pygame.display.flip()
        else:
            print(f"[{difficulty}] Error: Cannot reach delivery or battery exhausted.")
            pygame.display.set_caption(f"{difficulty} MISSION FAILED: Cannot reach delivery.")

        if index < len(test_cases) - 1:
            pygame.time.wait(5000)

    pygame.display.set_caption("All Test Cases Completed.")
    print("\nAll missions completed.")
    
    while True:
        create_grid.handle_pygame_events()
        create_grid.CLOCK.tick(10)

if __name__ == "__main__":
    main()