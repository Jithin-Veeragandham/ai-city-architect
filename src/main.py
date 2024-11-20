from local_search import *
from visualization import *

def main():
    best_grid, shortest_paths = hill_climbing()
    visualize_city_grid_with_offset_paths(best_grid, shortest_paths)

if __name__ == "__main__":
    main()