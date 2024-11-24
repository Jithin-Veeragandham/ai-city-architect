from grid_generation import *
from a_star_algo import *
from grid_generation import *
from objective import calculate_fitness
from visualization import save_city_grid
import os
from datetime import datetime
import copy

def hill_climbing(max_iterations=200):

    initial_grid = generate_city_grid_with_only_bordering_intersections()
    initial_grid_with_intersections  = place_intersections_in_every_column_randomly(initial_grid)
    current_grid = copy.deepcopy(initial_grid_with_intersections)
    current_paths = find_all_shortest_paths(current_grid)
    initial_fitness_scores = calculate_fitness(current_grid, current_paths)
    current_score = sum(initial_fitness_scores.values()) / len(initial_fitness_scores)
    print(f"Initial fitness scores: {initial_fitness_scores}")

    dir_path = os.path.join(os.getcwd(), "project py files\\ai-city-architect\\res","hill_climbing_"+datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
    os.mkdir(dir_path)
    save_city_grid(initial_grid_with_intersections, current_paths, dir_path, "hill_climbing_initial.png")

    for _ in range(max_iterations):
        print(f"Iteration {_}")
        new_grid = generate_neighbor(current_grid)
        new_paths = find_all_shortest_paths(new_grid)
        fitness_scores = calculate_fitness(new_grid, new_paths)
        new_score = sum(fitness_scores.values()) / len(initial_fitness_scores)

        # If the new configuration is better, accept it
        if new_score < current_score:
            print(f"Accepted new configuration with score {new_score}")
            current_grid = new_grid
            current_score = new_score
            current_paths = new_paths
            save_city_grid(new_grid, new_paths, dir_path, f"hill_climbing_iter{_}_accepted.png")

        # Optionally print progress
        print(f"Iteration {_}: Current Score = {current_score}")

    return current_grid, current_paths

def generate_neighbor(grid):
    """
    Generates a new grid configuration by randomly moving an intersection.
    """
    import random
    new_grid = copy.deepcopy(grid)

    # Find all intersections
    intersections = [
        (y, x) for y in range(1,len(new_grid)-1) 
               for x in range(1,len(new_grid[0])-1) 
               if new_grid[y][x] == 3
    ]

    if not intersections:
        return new_grid  # No intersections to move

    # Randomly select an intersection to move
    y, x = random.choice(intersections)

    # Find empty cells (0) to move to
    empty_cells = [
        (new_y, new_x) for new_y in range(len(new_grid)) 
                       for new_x in range(len(new_grid[0])) 
                       if new_grid[new_y][new_x] == 0
    ]

    if not empty_cells:
        return new_grid  # No valid moves
  
    # Move the intersection to a random empty cell
    new_y, new_x = random.choice(empty_cells)
    new_grid[y][x] = 0  # Remove from the current position
    new_grid[new_y][new_x] = 3  # Place at the new position

    return new_grid