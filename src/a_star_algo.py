import heapq
from helper import *
def get_neighbors(grid, node):
    current, prev_direction = node
    x, y = current
    neighbors = []

    # Define possible moves
    directions = {
        "up": (0, -1),
        "down": (0, 1),
        "left": (-1, -0),
        "right": (1, 0)
    }

    # Check the cell value at the current position
    if grid[y][x] == 3:
        # Allowed all directions for grid cell with value 3
        allowed_directions = ["up", "down", "left", "right"]
    elif ((y%2 == 0) and prev_direction in ["up", "down"]) and (grid[y][x] in [0 , 3]) :
        allowed_directions = [prev_direction]
    elif prev_direction is None:
        # Starting position, can move only up or down
        allowed_directions = ["up", "down"]
    elif prev_direction in ["up", "right"]:
        # Previous direction was up or right, can only move right
        allowed_directions = ["right"]
    elif prev_direction in ["down", "left"]:
        # Previous direction was down or left, can only move left
        allowed_directions = ["left"]
    else:
        allowed_directions = []  # default empty list if no directions are allowed

    # Calculate neighbors based on allowed directions
    for direction in allowed_directions:
        dx, dy = directions[direction]
        new_x, new_y = x + dx, y + dy

        # Ensure new coordinates are within grid bounds
        if 0 <= new_x < len(grid[0]) and 0 <= new_y < len(grid):
            neighbors.append(((new_x, new_y), direction))
    return neighbors

def a_star(grid, start, goal):
    # Initialize open and closed lists

    open_list = []
    closed_list = set()
    came_from = {}  # Dictionary to store the parent of each node for path reconstruction

    # Initialize start node
    start_node = start  # (coordinates, direction)
    g_costs = {start_node: 0}
    f_costs = {start_node: manhattan_distance(start_node, goal)}

    # Add start node to open list with initial f-cost
    heapq.heappush(open_list, (f_costs[start_node], start_node))

    # Main loop
    while open_list:
        # Get node with lowest f-cost
        _, current_node = heapq.heappop(open_list)

        current, prev_direction = current_node
        goal_position, _ = goal  # Unpack goal coordinates and ignore the direction
        # print('goal is ',prev_direction)
        if (current[0] == goal_position[0]  and 
            ((current[1] + 1 == goal_position[1] and prev_direction == 'right') or 
            (current[1] - 1 == goal_position[1] and prev_direction == 'left') or 
            is_intersection_and_above_below(current, grid, goal_position))):
            # print(current_node)  # Compare only coordinates, ignoring direction
            return reconstruct_path(came_from, current_node)  # Reconstruct the path from start to goal

        # Add current node to closed list
        closed_list.add(current_node)

        # Get neighbors
        neighbors = get_neighbors(grid, current_node)

        for neighbor in neighbors:
            if neighbor in closed_list:
                continue
            if (grid[current[1]][current[0]] == 3) and is_cell_in_margins(grid,current):
                cell_cost = len(grid)//8
            else:
                cell_cost = 1
            tentative_g_cost = g_costs[current_node] + cell_cost

            if neighbor not in g_costs or tentative_g_cost < g_costs[neighbor]:
                # Update costs and add to open list
                came_from[neighbor] = current_node  # Track the parent of the neighbor for path reconstruction
                g_costs[neighbor] = tentative_g_cost
                h_cost = manhattan_distance(neighbor, goal)
                f_cost = tentative_g_cost + h_cost
                f_costs[neighbor] = f_cost
                heapq.heappush(open_list, (f_cost, neighbor))

    # If no path found
    # print(reconstruct_path(came_from, current_node))
    return None

def reconstruct_path(came_from, current_node):
    path = [current_node]
    while current_node in came_from:
        current_node = came_from[current_node]
        path.append(current_node)
    path.reverse()  # Reverse the path to get it from start to goal
    return path


def a_star_multiple_goals(grid, start):
    # Identify all emergency services (goals)
    emergencies = []
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == 2:  # Emergency service marked as 2
                emergencies.append(((x, y), None))  # Add as (coordinates, direction)

    # print(f"Found {len(emergencies)} emergency services.")

    shortest_path = None
    shortest_length = float('inf')

    # Run A* for each emergency service location
    for goal in emergencies:
        path = a_star(grid, start, goal)
        if path and len(path) < shortest_length:
            shortest_path = path
            shortest_length = len(path)

    # Return the shortest path found, if any
    # if shortest_path:
    #     print(f"Shortest path to an emergency service: {shortest_path} with length {shortest_length}")
    # else:
    #     print("No path found to any emergency service.")
    
    return shortest_path


def find_all_shortest_paths(grid):
    """
    Finds the shortest path from each building to the nearest emergency service.
    Returns an array of shortest paths for each building.
    """
    buildings = []  # Array to store building positions
    shortest_paths = []  # Array to store the shortest paths for each building

    # Step 1: Locate all buildings
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == 1:  # Building marked as 1
                buildings.append((x, y))

    # print(f"Found {len(buildings)} buildings.")

    # Step 2: For each building, use BFS to find the shortest path to the nearest emergency service
    for building in buildings:
        # print(f"Calculating shortest path for building at {building}...")
        shortest_path = a_star_multiple_goals(grid, (building,None))  # Use BFS to get shortest path for the building
        if shortest_path:
            shortest_paths.append(shortest_path)  # Add the path to the list if found
        else:
            print(f"No path found to any emergency service for building at {building}.")

    return shortest_paths
