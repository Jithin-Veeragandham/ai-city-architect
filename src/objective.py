from constants import PATH_PENALTY, INTERSECTION_PENALTY

def calculate_fitness(grid, shortest_paths):
    fitness_scores = {}

    for i, path in enumerate(shortest_paths):
        # Path length
        path_length = len(path)

        # Intersection count for the current path
        intersection_count = 0
        for (y, x), direction in path:
            # Check bounds and if not on the border
            if 0 <= y < len(grid) and 0 <= x < len(grid[0]):  # Ensure within grid bounds
                if 0 < y < len(grid) - 1 and 0 < x < len(grid[0]) - 1:  # Not on border
                    if grid[y][x] == 3:  # Check if the cell value is 3
                        intersection_count += 1

        # Fitness calculation for the current path
        fitness = PATH_PENALTY * path_length + INTERSECTION_PENALTY * intersection_count
        fitness_scores[i] = fitness

    return fitness_scores