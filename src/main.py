from a_star_algo import *
from grid_generation import *
from ui import *

GRID_WIDTH = 15
GRID_HEIGHT = 15
CELL_SIZE = 40
NUM_BUILDINGS = 7
NUM_EMERGENCY = 4

def main():

    grid_with_only_bordering_intersections = generate_city_grid_with_only_bordering_intersections(GRID_WIDTH, GRID_HEIGHT, 
                                                                                                  NUM_BUILDINGS, NUM_EMERGENCY)
    grid_with_intersections_randomly  = place_intersections_in_every_column_randomly(grid_with_only_bordering_intersections)
    shortest_paths = find_all_shortest_paths(grid_with_intersections_randomly)
    
    visualize_city_grid_with_vehicles(grid_with_intersections_randomly, shortest_paths, CELL_SIZE)

if __name__ == "__main__":
    main()