from local_search import *
from grid_generation import *
from genetic_algo import *


def main():
    initial_grid = generate_city_grid_with_only_bordering_intersections()
    initial_grid_with_intersections = place_intersections_in_every_column_randomly(
        initial_grid)
    best_grid, shortest_paths = hill_climbing(
        initial_grid_with_intersections, max_iterations=300)

    optimized_grid, short_paths = genetic_algorithm(
        population_size=10, generations=50, mutation_rate=0.2, initial_grid=initial_grid)


if __name__ == "__main__":
    """
    Entry point for the script. Executes the `main` function when the script is run directly.
    """
    main()
