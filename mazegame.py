import random
import networkx as nx
import tkinter as tk

class MazeBlocks:
    WALL = 1
    PASSAGE = 0

# Generate maze with random obstacles ensuring solvability
def gen(size: int, obstacle_chance: float = 0.2) -> list[list[int]]:
    maze_map = [[MazeBlocks.PASSAGE] * size for _ in range(size)]
    
    # Place random obstacles, but keep start (0, 0) and goal (size-1, size-1) open
    for r in range(size):
        for c in range(size):
            if (r, c) not in [(0, 0), (size-1, size-1)] and random.random() < obstacle_chance:
                maze_map[r][c] = MazeBlocks.WALL

    return maze_map

# Convert maze to a graph for pathfinding
def maze_to_graph(maze):
    G = nx.Graph()
    size = len(maze)

    for r in range(size):
        for c in range(size):
            if maze[r][c] == MazeBlocks.PASSAGE:
                G.add_node((r, c))
                if r + 1 < size and maze[r + 1][c] == MazeBlocks.PASSAGE:
                    G.add_edge((r, c), (r + 1, c))
                if c + 1 < size and maze[r][c + 1] == MazeBlocks.PASSAGE:
                    G.add_edge((r, c), (r, c + 1))

    return G

# A* Pathfinding
def astar(graph, start, goal):
    try:
        path = nx.astar_path(graph, start, goal, heuristic=lambda a, b: abs(a[0] - b[0]) + abs(a[1] - b[1]))
        return path
    except nx.NetworkXNoPath:
        return None

# Check if the generated maze is solvable
def ensure_solvable_maze(size: int, obstacle_chance: float):
    while True:
        maze = gen(size, obstacle_chance)
        graph = maze_to_graph(maze)
        start = (0, 0)
        goal = (size - 1, size - 1)
        path = astar(graph, start, goal)
        if path:  # Found a valid path
            return maze, path

# GUI for the maze
class MazeGUI:
    def __init__(self, root, maze, path):
        self.root = root
        self.maze = maze
        self.path = path
        self.size = len(maze)
        self.cell_size = 60
        self.canvas = tk.Canvas(root, width=self.size * self.cell_size, height=self.size * self.cell_size)
        self.canvas.pack()
        
        # Adjust images to fit the grid size
        self.robot_image = tk.PhotoImage(file="robot.png")
        self.treasure_image = tk.PhotoImage(file="treasure2.png")
        
        # Scale the images based on cell size
        self.robot_image = self.robot_image.subsample(self.robot_image.width() // self.cell_size, 
                                                      self.robot_image.height() // self.cell_size)
        self.treasure_image = self.treasure_image.subsample(self.treasure_image.width() // self.cell_size, 
                                                            self.treasure_image.height() // self.cell_size)
        
        self.draw_maze()

    def draw_maze(self):
        for r in range(self.size):
            for c in range(self.size):
                x1 = c * self.cell_size
                y1 = r * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                if self.maze[r][c] == MazeBlocks.WALL:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="#191970") # MidNightBlue
                elif (r, c) in self.path:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="#98FB98") # PaleGreen
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="#F5F5F5", outline="#2F4F4F") # WhiteSmoke and DarkSlateGray

        # Draw robot at (0, 0) and treasure at (size-1, size-1)
        robot_x = self.cell_size // 2
        robot_y = self.cell_size // 2
        self.canvas.create_image(robot_x, robot_y, image=self.robot_image)

        treasure_x = (self.size - 1) * self.cell_size + self.cell_size // 2
        treasure_y = (self.size - 1) * self.cell_size + self.cell_size // 2
        self.canvas.create_image(treasure_x, treasure_y, image=self.treasure_image)

if __name__ == "__main__":
    size = 8  # 8x8 grid size
    obstacle_chance = 0.3  # 30% chance of placing an obstacle
    maze, path = ensure_solvable_maze(size, obstacle_chance)

    root = tk.Tk()
    gui = MazeGUI(root, maze, path)
    root.mainloop()
