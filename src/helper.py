def manhattan_distance(node1, node2):
    """
    Calculates the Manhattan distance between two nodes.
    The Manhattan distance is the sum of the absolute differences between 
    the x and y coordinates of two points, ignoring direction.

    Parameters:
        node1 (tuple): The first node as ((x, y), direction).
        node2 (tuple): The second node as ((x, y), direction).

    Returns:
        int: The Manhattan distance between the two nodes.
    """
    # Extract coordinates from each node
    (x1, y1), _ = node1  # node1 has (coordinates, direction)
    (x2, y2), _ = node2  # node2 has (coordinates, direction)
    return abs(x1 - x2) + abs(y1 - y2)


def is_intersection_and_above_below(current,grid,goal):
   """
    Determines if the current cell is an intersection and is directly 
    above or below the goal cell.

    Parameters:
        current (tuple): The current cell's coordinates as (x, y).
        grid (list[list[int]]): The 2D grid representing the environment.
        goal (tuple): The goal cell's coordinates as (x, y).

    Returns:
        bool: True if the current cell is an intersection (value 3) and is 
              directly above or below the goal cell, False otherwise.
    """
   return (grid[current[1]][current[0]]==3  and 
           ((current[1] == goal[1] - 1) or (current[1] == goal[1] + 1)))

def is_cell_in_margins(grid, cell):
    """
    Checks whether a cell is located in the margins (edges) of the grid.

    Parameters:
        grid (list[list[int]]): The 2D grid as a list of lists.
        cell (tuple): The cell to check, represented as (row, column).

    Returns:
        bool: True if the cell is located in the margins (top row, bottom row, 
              left column, or right column), False otherwise.
    """
    rows = len(grid)
    cols = len(grid[0])
    row, col = cell

    # Check if the cell is in the margins
    return row == 0 or row == rows - 1 or col == 0 or col == cols - 1