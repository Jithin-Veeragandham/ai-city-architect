from grid_generation import *
from a_star_algo import *
from grid_generation import *
from objective import calculate_fitness
from visualization import save_city_grid
import os
import copy
import random
from datetime import datetime
from copy import deepcopy


def hill_climbing(max_iterations=200):
    """
    Implements the hill climbing algorithm to optimize the placement of intersections in a city grid.

    Steps:
    1. Generates an initial grid with intersections and calculates the initial fitness score.
    2. Iteratively generates neighboring configurations and evaluates their fitness scores.
    3. Accepts a new configuration if it improves the fitness score.
    4. Saves the grid visualization at each step for progress tracking.

    Parameters:
        max_iterations (int): Maximum number of iterations for the algorithm.

    Returns:
        tuple: The optimized grid and the corresponding paths after hill climbing.
    """
    initial_grid = generate_city_grid_with_only_bordering_intersections()
    initial_grid_with_intersections  = place_intersections_in_every_column_randomly(initial_grid)
    current_grid = copy.deepcopy(initial_grid_with_intersections)
    current_paths = find_all_shortest_paths(current_grid)
    initial_fitness_scores = calculate_fitness(current_grid, current_paths)
    current_score = sum(initial_fitness_scores.values()) / len(initial_fitness_scores)

    dir_path = os.path.join(rf"/Users/shreycshah/Desktop/Coursework/Fall24/CS5100/Project/UrbanAItect/res",
                            datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
    os.mkdir(dir_path)
    save_city_grid(initial_grid_with_intersections, current_paths, dir_path, "hill_climbing_initial.png")

    for _ in range(max_iterations):
        print(f"Iteration {_}")
        new_grid = generate_neighbor(current_grid)
        new_paths = find_all_shortest_paths(new_grid)
        fitness_scores = calculate_fitness(new_grid, new_paths)
        new_grid = best_path_retention(current_grid, new_grid, current_paths, new_paths)
        new_paths = find_all_shortest_paths(new_grid)
        fitness_scores = calculate_fitness(new_grid, new_paths)

        new_score = sum(fitness_scores.values()) / len(initial_fitness_scores)

        # If the new configuration is better, accept it
        if new_score < current_score:
            print(f"Accepted new configuration with score {new_score} at iteration {_}")

            current_grid = new_grid
            current_score = new_score
            current_paths = new_paths
            save_city_grid(new_grid, new_paths, dir_path, f"iter{_}_cost_{current_score}.png")

        # Optionally print progress
        # print(f"Iteration {_}: Current Score = {current_score}")

    return current_grid, current_paths


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
    new_grid = copy.deepcopy(grid)
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
