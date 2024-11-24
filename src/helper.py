
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
    elif (y%2 == 0) and prev_direction in ["up", "down"]:
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

def manhattan_distance(node1, node2):
    # Extract coordinates from each node
    (x1, y1), _ = node1  # node1 has (coordinates, direction)
    (x2, y2), _ = node2  # node2 has (coordinates, direction)
    return abs(x1 - x2) + abs(y1 - y2)


def is_intersection_and_above_below(current,grid,goal):
   return (grid[current[1]][current[0]]==3  and 
           ((current[1] == goal[1] - 1) or (current[1] == goal[1] + 1)))