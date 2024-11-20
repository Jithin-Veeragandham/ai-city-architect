from grid_generation import *
from a_star_algo import *
from grid_generation import *
from objective import calculate_fitness

def hill_climbing():
    initial_grid = generate_city_grid_with_only_bordering_intersections()
    initial_grid_with_intersections  = place_intersections_in_every_column_randomly(initial_grid)
    shortest_paths = find_all_shortest_paths(initial_grid_with_intersections)
    initial_fitness_scores = calculate_fitness(initial_grid_with_intersections, shortest_paths)
    print(f"Initial fitness scores: {initial_fitness_scores}")

    for i in range(HILL_CLIMBING_MAX_ITERATIONS):
        pass

    return initial_grid_with_intersections, shortest_paths