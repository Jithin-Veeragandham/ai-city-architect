import random
from copy import deepcopy
from datetime import datetime
import os
from algorithms.a_star_algo import find_all_shortest_paths
from utils.helper import generate_neighbor, best_path_retention
from utils.grid_generation import place_intersections_in_every_column_randomly
from visuals.visualization import save_city_grid_with_annotation, combine_images, remove_images_by_prefix
from algorithms.cost_function import calculate_fitness
from grid_constants import RES_DIR


def initialize_population(size, initial_grid):
    """
    Initializes a population of grids for evolutionary algorithms by creating variations
    of the initial grid. Intersections are placed randomly in each grid to create diversity.

    Parameters:
        size (int): The number of grids in the population.
        initial_grid (list[list[int]]): The initial grid to serve as a base for population creation.

    Returns:
        list[list[list[int]]]: A list of grids, each representing a member of the population.
    """
    population = []
    for i in range(size):
        grid = deepcopy(initial_grid)
        grid_with_intersections = place_intersections_in_every_column_randomly(
            grid)
        population.append(grid_with_intersections)

    # print(f"Initialized population of size {size}.")
    return population


def select_best_grids(population, fitness_scores, num_selected):
    """
    Selects the best grids based on their average fitness scores.

    Steps:
    1. Computes the average fitness score for each grid in the population.
    2. Sorts the grids in ascending order of average fitness scores (lower is better).
    3. Selects the top num_selected grids for the next generation.

    Parameters:
        population (list[list[list[int]]]): The current population of grids.
        fitness_scores (list[dict]): A list of fitness score dictionaries for each grid in the population.
                                     Each dictionary maps buildings to their fitness scores.
        num_selected (int): The number of grids to select for the next generation.

    Returns:
        tuple: 
            - list[list[list[int]]]: The selected grids.
            - list[float]: The average fitness scores of the selected grids.
    """
    avg_fitness_scores = []
    for grid, fitness_dict in zip(population, fitness_scores):
        avg_fitness = sum(fitness_dict.values()) / len(fitness_dict)
        avg_fitness_scores.append((grid, avg_fitness))

    # Sort by average fitness (ascending)
    sorted_population = sorted(avg_fitness_scores, key=lambda x: x[1])

    # Select the best grids
    selected_population = [grid for grid,
                           _ in sorted_population[:num_selected]]
    avg_fitness = [fitness for _, fitness in sorted_population[:num_selected]]

    return selected_population, avg_fitness


def genetic_algorithm(population_size, generations, mutation_rate, initial_grid):
    """
    Implements a genetic algorithm to optimize city grid configurations for better fitness scores.
    Includes elitism to preserve the best grid across generations.

    Steps:
    1. Initializes a population of grids with random variations.
    2. Iteratively improves the population over a specified number of generations:
       - Evaluates fitness for all grids in the population.
       - Selects the top-performing grids based on fitness scores.
       - Creates a new population using crossover (best path retention) and mutation.
       - Preserves the best grid in each generation (elitism).
    3. Visualizes and logs the grids and fitness scores for each generation.
    4. Returns the globally best grid and its shortest paths.

    Parameters:
        population_size (int): The number of grids in the population.
        generations (int): The number of generations to evolve the population.
        mutation_rate (float): The probability of mutating a grid in the population.
        initial_grid (list[list[int]]): The initial grid used to create the initial population.

    Returns:
        tuple:
            - list[list[int]]: The globally best grid configuration.
            - list[list[tuple]]: The shortest paths corresponding to the best grid.
    """
    population = initialize_population(population_size, initial_grid)
    best_fitness = float('inf')  # Initialize with a very high fitness score

    dir_path = os.path.join(
        RES_DIR, "genetic_algorithm_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
    os.mkdir(dir_path)
    for generation in range(generations):
        fitness_scores = []
        for grid in population:
            shortest_paths = find_all_shortest_paths(grid)
            fitness = calculate_fitness(grid, shortest_paths)
            fitness_scores.append(fitness)

        # Select the best grids
        selected_population, avg_fitness = select_best_grids(
            population, fitness_scores, num_selected=6)

        # Identify the best grid in the current generation
        current_best_index = avg_fitness.index(min(avg_fitness))
        current_best_grid = selected_population[current_best_index]
        current_best_fitness = avg_fitness[current_best_index]

        image_paths = []

        # Visualize the selected grids
        for i, grid in enumerate(selected_population):
            shortest_paths = find_all_shortest_paths(grid)
            annotated_path = save_city_grid_with_annotation(
                grid, shortest_paths, dir_path, f"generation_{generation+1}grid{i+1}.png", avg_fitness[i]
            )
            image_paths.append(annotated_path)

            print(
                f"Generation {generation + 1}, Grid {i + 1} (Fitness: {avg_fitness[i]})")

        combine_images(image_paths, os.path.join(
            dir_path, f"Generation_{generation+1}_summary.png"))
        remove_images_by_prefix(dir_path, "generation_")

        # Create a new population with the best grid explicitly included
        new_population = []  # Start with the best grid

        while len(new_population) < population_size:
            parent1, parent2 = random.sample(selected_population, 2)

            parent1_paths = find_all_shortest_paths(parent1)

            parent2_paths = find_all_shortest_paths(parent2)

            child = best_path_retention(
                parent1, parent2, parent1_paths, parent2_paths)

            new_population.append(child)

        combined_population = selected_population + new_population

        population = [
            generate_neighbor(grid) if (
                grid not in selected_population and random.random() < mutation_rate) else grid
            for grid in combined_population
        ]

        # Log the best fitness of the generation
        print(
            f"Generation {generation + 1}: Best Fitness = {current_best_fitness}")
        best_fitness = current_best_fitness

    short_paths = find_all_shortest_paths(current_best_grid)

    return current_best_grid, short_paths, best_fitness
