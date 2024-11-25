


def manhattan_distance(node1, node2):
    # Extract coordinates from each node
    (x1, y1), _ = node1  # node1 has (coordinates, direction)
    (x2, y2), _ = node2  # node2 has (coordinates, direction)
    return abs(x1 - x2) + abs(y1 - y2)


def is_intersection_and_above_below(current,grid,goal):
   return (grid[current[1]][current[0]]==3  and 
           ((current[1] == goal[1] - 1) or (current[1] == goal[1] + 1)))

def is_cell_in_margins(grid, cell):
    """
    Determines if a cell is in the margins (edges) of the grid.

    Args:
        grid (list of list of int): The grid as a 2D list.
        cell (tuple): The cell to check, represented as (row, column).

    Returns:
        bool: True if the cell is in the margins, False otherwise.
    """
    rows = len(grid)
    cols = len(grid[0])
    row, col = cell

    # Check if the cell is in the margins
    return row == 0 or row == rows - 1 or col == 0 or col == cols - 1