from utils.grid_generation import generate_city_grid_with_only_bordering_intersections
from algorithms.local_search import local_search_algorithm
from algorithms.genetic_algo import genetic_algorithm

def main():
    initial_grid = generate_city_grid_with_only_bordering_intersections()
    
    best_grid, shortest_paths, local_cost = local_search_algorithm(initial_grid, max_iterations=100)

    optimized_grid, short_paths, genetic_cost = genetic_algorithm( population_size=10, generations=10, 
                                                                    mutation_rate=0.2, initial_grid=initial_grid)
    
    print("Final cost after hill climbing: ", local_cost)
    # print("Final cost after genetic algorithm: ", genetic_cost)
    

if __name__ == "__main__":
    """
    Entry point for the script. Executes the `main` function when the script is run directly.
    """
    main()
