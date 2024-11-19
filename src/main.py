from a_star_algo import *
from grid_generation import *
from visualization import *

GRID_WIDTH = 15
GRID_HEIGHT = 15
CELL_SIZE = 30 
NUM_BUILDINGS = 7
NUM_EMERGENCY = 4

def main():

    grid = generate_city_grid(GRID_WIDTH, GRID_HEIGHT, NUM_BUILDINGS, NUM_EMERGENCY)
    shortest_paths = find_all_shortest_paths(grid)
    visualize_city_grid_with_offset_paths(grid, shortest_paths, CELL_SIZE)

if __name__ == "__main__":
    main()