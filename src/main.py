from local_search import *
from grid_generation import *


def main():
    initial_grid = generate_city_grid_with_only_bordering_intersections()
    initial_grid_with_intersections  = place_intersections_in_every_column_randomly(initial_grid)
    best_grid, shortest_paths = hill_climbing(initial_grid_with_intersections, max_iterations=1000)


if __name__ == "__main__":
    """
    Entry point for the script. Executes the `main` function when the script is run directly.
    """
    main()