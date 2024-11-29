from copy import deepcopy
import random
from algorithms.objective import calculate_fitness

def manhattan_distance(node1, node2):
    """
    Calculates the Manhattan distance between two nodes.
    The Manhattan distance is the sum of the absolute differences between 
    the x and y coordinates of two points, ignoring direction.

    Parameters:
        node1 (tuple): The first node as ((x, y), direction).
        node2 (tuple): The second node as ((x, y), direction).

    Returns:
        int: The Manhattan distance between the two nodes.
    """
    # Extract coordinates from each node
    (x1, y1), _ = node1  # node1 has (coordinates, direction)
    (x2, y2), _ = node2  # node2 has (coordinates, direction)
    return abs(x1 - x2) + abs(y1 - y2)


def is_intersection_and_above_below(current,grid,goal):
   """
    Determines if the current cell is an intersection and is directly 
    above or below the goal cell.

    Parameters:
        current (tuple): The current cell's coordinates as (x, y).
        grid (list[list[int]]): The 2D grid representing the environment.
        goal (tuple): The goal cell's coordinates as (x, y).

    Returns:
        bool: True if the current cell is an intersection (value 3) and is 
              directly above or below the goal cell, False otherwise.
    """
   return (grid[current[1]][current[0]]==3  and 
           ((current[1] == goal[1] - 1) or (current[1] == goal[1] + 1)))

def is_cell_in_margins(grid, cell):
    """
    Checks whether a cell is located in the margins (edges) of the grid.

    Parameters:
        grid (list[list[int]]): The 2D grid as a list of lists.
        cell (tuple): The cell to check, represented as (row, column).

    Returns:
        bool: True if the cell is located in the margins (top row, bottom row, 
              left column, or right column), False otherwise.
    """
    rows = len(grid)
    cols = len(grid[0])
    row, col = cell

    # Check if the cell is in the margins
    return row == 0 or row == rows - 1 or col == 0 or col == cols - 1


def generate_neighbor(grid):
    """
    Generates a neighboring grid configuration by randomly moving intersections 
    and ensuring the total number of intersections remains consistent.

    Steps:
    1. Identifies all intersections and randomly selects one to move.
    2. Finds empty cells to move the intersection and adjusts the grid.
    3. Ensures the total number of intersections matches the target by adding or removing intersections as needed.

    Parameters:
        grid (list[list[int]]): The current city grid.

    Returns:
        list[list[int]]: A new grid configuration with adjusted intersections.
    """
    new_grid = deepcopy(grid)
    target_intersections = len(new_grid) + 1

    # Find all intersections
    intersections = [
        (y, x) for y in range(1, len(new_grid) - 1)
               for x in range(1, len(new_grid[0]) - 1)
               if new_grid[y][x] == 3
    ]

    if intersections:
        # Randomly select an intersection to move
        y, x = random.choice(intersections)

        # Find empty cells (0) to move to
        empty_cells = [
            (new_y, new_x) for new_y in range(1, len(new_grid) - 1)
                           for new_x in range(1, len(new_grid[0]) - 1)
                           if (new_grid[new_y][new_x] == 0 and
                               new_y % 2 != 0)  # Satisfies y % 2 != 0
        ]

        if empty_cells:
            # Move the intersection to a random empty cell
            new_y, new_x = random.choice(empty_cells)
            new_grid[y][x] = 0  # Remove from the current position
            new_grid[new_y][new_x] = 3  # Place at the new position

    # Recalculate the number of intersections
    intersections = [
        (y, x) for y in range(1, len(new_grid) - 1)
               for x in range(1, len(new_grid[0]) - 1)
               if new_grid[y][x] == 3
    ]

    current_intersections = len(intersections)

    # Add intersections if needed
    if current_intersections < target_intersections:
        empty_cells = [
            (new_y, new_x) for new_y in range(1, len(new_grid) - 1)
                           for new_x in range(1, len(new_grid[0]) - 1)
                           if new_grid[new_y][new_x] == 0
        ]
        while current_intersections < target_intersections and empty_cells:
            new_y, new_x = random.choice(empty_cells)
            new_grid[new_y][new_x] = 3
            empty_cells.remove((new_y, new_x))
            current_intersections += 1

    # Remove intersections if needed
    elif current_intersections > target_intersections:
        while current_intersections > target_intersections:
            y, x = random.choice(intersections)
            new_grid[y][x] = 0
            intersections.remove((y, x))
            current_intersections -= 1

    return new_grid


def best_path_retention(grid, new_grid, paths, new_paths):
    """
    Retains the best path configuration between the current and new grids by comparing fitness scores.
    Updates the grid to include only intersections from the paths with the best fitness.

    Steps:
    1. Compares fitness scores of paths from the current and new grids for each building.
    2. Retains the best path and merges its intersections into the final grid.
    3. Resets all intersections in the merged grid before applying the selected configurations.

    Parameters:
        grid (list[list[int]]): The current city grid.
        new_grid (list[list[int]]): The new city grid configuration.
        paths (list[list[tuple]]): Paths from the current grid.
        new_paths (list[list[tuple]]): Paths from the new grid.

    Returns:
        list[list[int]]: The merged grid with updated intersections based on the best paths.
    """
    # Initialize merged grid as a deep copy of the old grid
    old_paths_dict= {}
    for path in paths:
        old_paths_dict[path[0][0]] = path
    new_paths_dict = {}
    for path in new_paths:
        new_paths_dict[path[0][0]] = path
    merged_grid = deepcopy(grid)
    for i in range(1,len(merged_grid)-1):
        for j in range(1,len(merged_grid[0])-1):
            if merged_grid[i][j] == 3:
                merged_grid[i][j] = 0
    # Replace all 3s in merged grid with 0s

    current_fitness_scores = calculate_fitness(grid, paths)
    new_fitness_scores = calculate_fitness(new_grid, new_paths)
    # print('current_fitness_scores:', current_fitness_scores)
    # print('new_fitness_scores:', new_fitness_scores)
    
    # Dictionary to store selected paths and grids
    selected_config = {}

    # Iterate through each building in old_paths_dict
    for building, old_path in old_paths_dict.items():
        # Get the corresponding new path
        new_path = new_paths_dict.get(building, None)
        
        # Calculate fitness for old and new paths
        old_fitness = current_fitness_scores.get(building, float('inf'))
        new_fitness = new_fitness_scores.get(building, float('inf'))
        
        # Compare fitness scores and update the selected configuration
        if old_fitness <= new_fitness:
            selected_config[building] = (grid, old_path)
        else:
            selected_config[building] = (new_grid, new_path)
    # print(selected_config)
    for building, (selected_grid, selected_path) in selected_config.items():
        for step in selected_path:
            coord, _ = step  # Each step is ((x, y), 'direction')
            x, y = coord
            # Use the value from the selected grid at the given coordinate
            merged_grid[x][y] = selected_grid[x][y]
  
    return merged_grid