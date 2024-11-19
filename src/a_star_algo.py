import heapq
from helper import *

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

            tentative_g_cost = g_costs[current_node] + 1

            if neighbor not in g_costs or tentative_g_cost < g_costs[neighbor]:
                # Update costs and add to open list
                came_from[neighbor] = current_node  # Track the parent of the neighbor for path reconstruction
                g_costs[neighbor] = tentative_g_cost
                h_cost = manhattan_distance(neighbor, goal)
                f_cost = tentative_g_cost + h_cost
                f_costs[neighbor] = f_cost
                heapq.heappush(open_list, (f_cost, neighbor))

    # If no path found
    print(reconstruct_path(came_from, current_node))
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

    print(f"Found {len(emergencies)} emergency services.")

    shortest_path = None
    shortest_length = float('inf')

    # Run A* for each emergency service location
    for goal in emergencies:
        path = a_star(grid, start, goal)
        if path and len(path) < shortest_length:
            shortest_path = path
            shortest_length = len(path)

    # Return the shortest path found, if any
    if shortest_path:
        print(f"Shortest path to an emergency service: {shortest_path} with length {shortest_length}")
    else:
        print("No path found to any emergency service.")
    
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

    print(f"Found {len(buildings)} buildings.")

    # Step 2: For each building, use BFS to find the shortest path to the nearest emergency service
    for building in buildings:
        print(f"Calculating shortest path for building at {building}...")
        shortest_path = a_star_multiple_goals(grid, (building,None))  # Use BFS to get shortest path for the building
        if shortest_path:
            shortest_paths.append(shortest_path)  # Add the path to the list if found
        else:
            print(f"No path found to any emergency service for building at {building}.")

    return shortest_paths
