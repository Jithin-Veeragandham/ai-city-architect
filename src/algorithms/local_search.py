import os
from copy import deepcopy
from datetime import datetime
from algorithms.a_star_algo import find_all_shortest_paths
from utils.helper import generate_neighbor, best_path_retention
from algorithms.cost_function import calculate_fitness
from visuals.visualization import save_city_grid
from utils.grid_generation import place_intersections_in_every_column_randomly
from grid_constants import RES_DIR


def hill_climbing(grid, max_iterations=200):
    """
    Implements the hill climbing algorithm to optimize the placement of intersections in a city grid.

    Steps:
    1. Iteratively generates neighboring configurations and evaluates their fitness scores.
    2. Accepts a new configuration if it improves the fitness score.
    3. Saves the grid visualization at each step for progress tracking.

    Parameters:
        grid (list[list[int]]): The initial city grid with intersections.
        max_iterations (int): Maximum number of iterations for the algorithm.

    Returns:
        tuple: The optimized grid and the corresponding paths after hill climbing.
    """
    grid = place_intersections_in_every_column_randomly(grid)
    current_grid = deepcopy(grid)
    current_paths = find_all_shortest_paths(current_grid)
    initial_fitness_scores = calculate_fitness(current_grid, current_paths)
    current_score = sum(initial_fitness_scores.values()) / len(initial_fitness_scores)

    dir_path = os.path.join(RES_DIR, "hill_climbing_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
    os.mkdir(dir_path)
    save_city_grid(grid, current_paths, dir_path,current_score, "hill_climbing_initial.png")

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
            save_city_grid(new_grid, new_paths, dir_path,current_score, f"iter{_}_cost_{current_score}.png")

        # Optionally print progress
        # print(f"Iteration {_}: Current Score = {current_score}")

    return current_grid, current_paths, current_score
