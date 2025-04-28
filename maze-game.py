import pygame
import sys
import heapq
from collections import defaultdict
import random

# Initialize Pygame
pygame.init()

# Constants
CELL_SIZE = 40  # Increased for better visibility
GRID_WIDTH = 15
GRID_HEIGHT = 12
SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH + 300  # Added space for algorithm info
SCREEN_HEIGHT = max(CELL_SIZE * GRID_HEIGHT, 600)
MOVEMENT_DELAY = 200  # Milliseconds between moves

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (147, 112, 219)
ORANGE = (255, 165, 0)
LIGHT_BLUE = (173, 216, 230)
GRAY = (128, 128, 128)

class MazeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Maze Escape - Dijkstra Algorithm Visualization")
        self.clock = pygame.time.Clock()
        self.maze = self.generate_maze()
        self.npc_pos = self.find_start()
        self.exit_pos = self.place_exit()
        self.path = []
        self.visited_nodes = set()
        self.current_distances = {}
        self.previous = {}
        self.found_path = False
        self.current_node = None
        self.current_neighbors = []
        self.algorithm_steps = []
        self.step_description = ""
        
    def generate_maze(self):
        # Initialize maze with walls
        maze = [[1 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        
        def carve_path(x, y):
            maze[y][x] = 0
            directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
            random.shuffle(directions)
            
            for dx, dy in directions:
                new_x, new_y = x + dx, y + dy
                if (0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT 
                    and maze[new_y][new_x] == 1):
                    if random.random() < 0.3:  # 30% chance for extra path
                        for alt_dx, alt_dy in directions:
                            alt_x, alt_y = x + alt_dx, y + alt_dy
                            if (0 <= alt_x < GRID_WIDTH and 0 <= alt_y < GRID_HEIGHT 
                                and maze[alt_y][alt_x] == 1):
                                maze[y + alt_dy//2][x + alt_dx//2] = 0
                    maze[y + dy//2][x + dx//2] = 0
                    carve_path(new_x, new_y)
        
        start_x, start_y = GRID_WIDTH//4, GRID_HEIGHT//4
        carve_path(start_x, start_y)
        return maze
    
    def find_start(self):
        for y in range(GRID_HEIGHT-3, GRID_HEIGHT-1):
            for x in range(1, 3):
                if self.maze[y][x] == 0:
                    return (x, y)
        return (1, GRID_HEIGHT-2)
    
    def place_exit(self):
        for y in range(1, 3):
            for x in range(GRID_WIDTH-3, GRID_WIDTH-1):
                if self.maze[y][x] == 0:
                    return (x, y)
        return (GRID_WIDTH-2, 1)
    
    def get_neighbors(self, pos):
        x, y = pos
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        neighbors = []
        
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if (0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT 
                and self.maze[new_y][new_x] == 0):
                neighbors.append((new_x, new_y))
        
        return neighbors
    
    def dijkstra_step(self):
        if not hasattr(self, 'pq'):
            # Initialize Dijkstra's algorithm
            self.current_distances = defaultdict(lambda: float('inf'))
            self.current_distances[self.npc_pos] = 0
            self.pq = [(0, self.npc_pos)]
            self.visited_nodes = set()
            self.previous = {}
            self.algorithm_steps.append("Initializing Dijkstra's Algorithm:")
            self.algorithm_steps.append(f"Set distance to start node {self.npc_pos} = 0")
            self.algorithm_steps.append("All other distances set to infinity")
        
        if self.pq and not self.found_path:
            # Get the node with minimum distance
            current_distance, current = heapq.heappop(self.pq)
            self.current_node = current
            
            if current not in self.visited_nodes:
                self.visited_nodes.add(current)
                self.algorithm_steps.append(f"\nExploring node {current}")
                self.algorithm_steps.append(f"Current distance: {current_distance}")
                
                if current == self.exit_pos:
                    self.found_path = True
                    self.path = []
                    curr = self.exit_pos
                    while curr in self.previous:
                        self.path.append(curr)
                        curr = self.previous[curr]
                    self.path.append(self.npc_pos)
                    self.path.reverse()
                    self.algorithm_steps.append("\nPath found! Reconstructing shortest path:")
                    self.algorithm_steps.append(f"Total distance: {current_distance}")
                    self.algorithm_steps.append(f"Path: {' -> '.join(str(p) for p in self.path)}")
                    return True
                
                # Check all neighbors
                neighbors = self.get_neighbors(current)
                self.current_neighbors = neighbors
                self.algorithm_steps.append(f"Checking neighbors: {neighbors}")
                
                for neighbor in neighbors:
                    distance = current_distance + 1
                    
                    if distance < self.current_distances[neighbor]:
                        self.current_distances[neighbor] = distance
                        self.previous[neighbor] = current
                        heapq.heappush(self.pq, (distance, neighbor))
                        self.algorithm_steps.append(f"Updated distance to {neighbor} = {distance}")
        
        return False
    
    def draw_algorithm_info(self):
        info_x = CELL_SIZE * GRID_WIDTH + 20
        info_y = 20
        line_height = 25
        font = pygame.font.Font(None, 24)
        
        # Draw algorithm status box
        status_box = pygame.Surface((280, SCREEN_HEIGHT - 40))
        status_box.fill(LIGHT_BLUE)
        self.screen.blit(status_box, (info_x, info_y))
        
        # Draw title
        title = font.render("Dijkstra's Algorithm Status", True, BLACK)
        self.screen.blit(title, (info_x + 10, info_y + 10))
        
        # Draw current node info
        if self.current_node:
            curr_text = f"Current Node: {self.current_node}"
            text = font.render(curr_text, True, BLACK)
            self.screen.blit(text, (info_x + 10, info_y + 40))
            
            dist_text = f"Distance: {self.current_distances.get(self.current_node, 'inf')}"
            text = font.render(dist_text, True, BLACK)
            self.screen.blit(text, (info_x + 10, info_y + 65))
        
        # Draw latest algorithm steps
        y_offset = info_y + 100
        for step in self.algorithm_steps[-15:]:  # Show last 15 steps
            text = font.render(step, True, BLACK)
            self.screen.blit(text, (info_x + 10, y_offset))
            y_offset += line_height
    
    def draw(self):
        self.screen.fill(WHITE)
        
        # Draw maze
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if self.maze[y][x] == 1:
                    pygame.draw.rect(self.screen, BLACK, rect)
                else:
                    # Draw distance values for empty cells
                    if (x, y) in self.current_distances:
                        dist = self.current_distances[(x, y)]
                        if dist != float('inf'):
                            font = pygame.font.Font(None, 20)
                            text = font.render(str(dist), True, GRAY)
                            text_rect = text.get_rect(center=(x * CELL_SIZE + CELL_SIZE//2,
                                                            y * CELL_SIZE + CELL_SIZE//2))
                            self.screen.blit(text, text_rect)
        
        # Draw visited nodes
        for node in self.visited_nodes:
            if node != self.npc_pos and node != self.exit_pos:
                rect = pygame.Rect(node[0] * CELL_SIZE, node[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, PURPLE, rect, 2)
        
        # Draw current neighbors
        for neighbor in self.current_neighbors:
            if neighbor != self.exit_pos:
                rect = pygame.Rect(neighbor[0] * CELL_SIZE, neighbor[1] * CELL_SIZE,
                                 CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, ORANGE, rect, 2)
        
        # Draw current path
        if self.found_path and self.path:
            for pos in self.path[1:]:
                if pos != self.exit_pos:
                    rect = pygame.Rect(pos[0] * CELL_SIZE, pos[1] * CELL_SIZE,
                                     CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(self.screen, YELLOW, rect)
        
        # Draw exit and NPC
        exit_rect = pygame.Rect(self.exit_pos[0] * CELL_SIZE, self.exit_pos[1] * CELL_SIZE,
                              CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(self.screen, GREEN, exit_rect)
        
        npc_rect = pygame.Rect(self.npc_pos[0] * CELL_SIZE, self.npc_pos[1] * CELL_SIZE,
                             CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(self.screen, RED, npc_rect)
        
        # Draw algorithm information
        self.draw_algorithm_info()
        
        pygame.display.flip()
    
    def run(self):
        running = True
        pathfinding_delay = 500  # Increased delay to better show the algorithm
        last_pathfinding_time = 0
        
        while running:
            current_time = pygame.time.get_ticks()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Reset
                        self.__init__()
                    elif event.key == pygame.K_SPACE:  # Pause/Resume
                        pathfinding_delay = 0 if pathfinding_delay else 500
            
            # Run Dijkstra step with delay
            if not self.found_path and current_time - last_pathfinding_time >= pathfinding_delay:
                self.dijkstra_step()
                last_pathfinding_time = current_time
            
            # Move NPC if path is found
            if self.found_path and self.path and current_time - last_pathfinding_time >= MOVEMENT_DELAY:
                if len(self.path) > 1:
                    self.path.pop(0)
                    self.npc_pos = self.path[0]
                    last_pathfinding_time = current_time
            
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

# Create and run the game
if __name__ == "__main__":
    game = MazeGame()
    game.run()
