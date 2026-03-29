
# AI Assignment (Group 22)
# Hitansh Chadha - 2022A8PS1255P
# Vedant Mathur - 2022A3PS0375P
# Krishna Raghunath - 2023A1PS0213P

from grid import create_grid
import pygame
import heapq

class AStarNode:
    def __init__(self, g_cost, h_cost, pos, collected, path, battery_left, score):
        self.g_cost = g_cost             
        self.h_cost = h_cost             
        self.f_cost = g_cost + h_cost    
        self.pos = pos
        self.collected = collected
        self.path = path
        self.battery_left = battery_left
        self.score = score

    def __lt__(self, other):
        if self.score != other.score:
            return self.score > other.score 
        if self.f_cost != other.f_cost:
            return self.f_cost < other.f_cost
        return self.battery_left > other.battery_left


def get_manhattan_distance(pos, delivery):
    return abs(pos[0] - delivery[0]) + abs(pos[1] - delivery[1])

def get_max_pr_item_manhattan(pos, uncollected_items, items_dict, delivery):
    if not uncollected_items:
        return get_manhattan_distance(pos, delivery)
        
    max_item = None
    max_score = -1
    
    for item in uncollected_items:
        if items_dict[item] > max_score:
            max_score = items_dict[item]
            max_item = item
            
    dist_to_item = get_manhattan_distance(pos, max_item)
    dist_item_to_delivery = get_manhattan_distance(max_item, delivery)
    
    return dist_to_item + dist_item_to_delivery

def a_star(screen, start, items_dict, delivery, obstacles, max_battery):
    target_items = frozenset(items_dict.keys())
    
    start_h = get_max_pr_item_manhattan(start, target_items, items_dict, delivery)
    start_node = AStarNode(0, start_h, start, frozenset(), [start], max_battery, 0)
    
    pq = [start_node]
    best_state_battery = {}
    
    best_score = -1
    best_path = None
    best_remaining_battery = -1
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while pq:
        create_grid.handle_pygame_events()
        current_node = heapq.heappop(pq)

        if current_node.pos == delivery:
            if current_node.score > best_score:
                best_score = current_node.score
                best_path = current_node.path
                best_remaining_battery = current_node.battery_left
                print(f"New best route found! Score: {best_score} | Battery: {best_remaining_battery}")
            

        state = (current_node.pos, current_node.collected)
        if state in best_state_battery and best_state_battery[state] >= current_node.battery_left:
            continue
        best_state_battery[state] = current_node.battery_left

        physical_explored = {s[0] for s in best_state_battery.keys()}
        physical_queue = [(node.pos, None) for node in pq] 
        
        create_grid.draw_grid_base(screen, start, list(target_items), delivery, obstacles, physical_explored, physical_queue)
        
        if len(current_node.path) > 1:
            create_grid.draw_lines(screen, current_node.path)
            
        pygame.display.set_caption(f"A* Manhattan (Max Prio) | Best Score: {best_score}")
        pygame.display.flip()
        create_grid.CLOCK.tick(create_grid.FPS)
       
        for dx, dy in directions:
            nx, ny = current_node.pos[0] + dx, current_node.pos[1] + dy
            
            if 0 <= nx < create_grid.GRID_SIZE and 0 <= ny < create_grid.GRID_SIZE and (nx, ny) not in obstacles:
                
                new_battery = current_node.battery_left - 1
                
                survival_dist = get_manhattan_distance((nx, ny), delivery)
                if new_battery < survival_dist:
                    continue 

                next_collected = current_node.collected
                new_score = current_node.score
                
                if (nx, ny) in target_items and (nx, ny) not in current_node.collected:
                    next_collected = current_node.collected | frozenset([(nx, ny)])
                    new_score += items_dict[(nx, ny)] 

                h_cost = get_max_pr_item_manhattan((nx, ny), target_items - next_collected, items_dict, delivery)

                new_g = current_node.g_cost + 1
                new_path = current_node.path + [(nx, ny)]
                
                new_node = AStarNode(new_g, h_cost, (nx, ny), next_collected, new_path, new_battery, new_score)
                heapq.heappush(pq, new_node)

    return best_path, best_remaining_battery, best_score


def main():
    test_cases = [
        {
            "difficulty": "easy",
            "start": (0, 0),
            "items": {(2, 2): 10},
            "delivery": (4, 4),
            "obstacles": [(1, 2), (2, 1), (3, 3)],
            "battery": 20 # Plenty of battery
        },
        {
            "difficulty": "medium",
            "start": (0, 0),
            "items": {(8, 2): 50, (2, 8): 20},
            "delivery": (9, 9),
            "obstacles": [(4, y) for y in range(0, 8)],
            # Battery is strictly limited. It takes ~18 steps to get ONE item and reach delivery.
            "battery": 25 
        },
        {
            "difficulty": "hard",
            "start": (0, 0),
            "items": {(2, 7): 50, (8, 2): 10, (0, 9): 100},
            "delivery": (9, 9),
            "obstacles": [(x, 5) for x in range(2, 10)] + [(5, y) for y in range(0, 4)] + [(2, 8), (3, 8), (4, 8)],
            "battery": 35 # High battery, but a massive maze to navigate
        }
    ]

    for index, tc in enumerate(test_cases):
        difficulty = tc["difficulty"]
        robot_start = tc["start"]
        items_with_priorities = tc["items"]
        delivery_loc = tc["delivery"]
        obstacles = tc["obstacles"]
        battery_capacity = tc["battery"]

        print(f"\n{difficulty} Test Case")

        final_path, rem_battery, final_score = a_star(
            create_grid.SCREEN, 
            robot_start, 
            items_with_priorities, 
            delivery_loc, 
            obstacles,
            battery_capacity
        )
        
        #drawing final path
        if final_path:
            
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
            pygame.display.set_caption(f"{difficulty} FAILED: Cannot reach delivery.")

        if index < len(test_cases) - 1:
            pygame.time.wait(5000)

    pygame.display.set_caption("All Test Cases Completed.")
    
    while True:
        create_grid.handle_pygame_events()
        create_grid.CLOCK.tick(10)

if __name__ == "__main__":
    main()