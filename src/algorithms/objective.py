def calculate_fitness(grid, shortest_paths):
    """
    Calculates fitness scores for the given grid and its corresponding shortest paths.
    The fitness score for each path is determined by a combination of path length and 
    the number of intersections within the path, weighted by penalties.

    Parameters:
        grid (list[list[int]]): The 2D city grid.
        shortest_paths (list[list[tuple]]): A list of shortest paths, where each path is a list of nodes.

    Returns:
        dict: A dictionary mapping the starting node (building position) of each path to its fitness score.

    Fitness Calculation:
    - `path_length`: The total number of steps in the path.
    - `intersection_count`: The number of intersections (value 3 in the grid) along the path.
    - `path_penalty`: A constant penalty factor for path length.
    - `intersection_penalty`: A penalty proportional to the grid size for each intersection encountered.
    - `fitness = path_penalty * path_length + intersection_penalty * intersection_count`
    """
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

        path_penalty = 1
        intersection_penalty = len(grid) // 8
        # Fitness calculation for the current path
        fitness = path_penalty * path_length + intersection_penalty * intersection_count
        fitness_scores[path[0][0]] = fitness

    return fitness_scores