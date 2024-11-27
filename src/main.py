from local_search import *
from grid_generation import *
from genetic_algo import *
from visualization import *


def main():
    initial_grid = generate_city_grid_with_only_bordering_intersections()
    initial_grid_with_intersections = place_intersections_in_every_column_randomly(
        initial_grid)
    best_grid, shortest_paths = hill_climbing(
        initial_grid_with_intersections, max_iterations=1000)

    optimized_grid = genetic_algorithm(path_penalty=1, intersection_penalty=1000,
                                       population_size=10, generations=10, mutation_rate=0.1, initial_grid=initial_grid)
    short_paths = find_all_shortest_paths(optimized_grid)
    dir_path = os.path.join(
        rf"D:\NEU MS CS\FAI\Project\ai-city-architect\res\GeneticAlgorithm")

    save_city_grid(optimized_grid, short_paths, dir_path,
                   f"Final.png")


if __name__ == "__main__":
    """
    Entry point for the script. Executes the `main` function when the script is run directly.
    """
    main()
