from utils.grid_generation import generate_city_grid_with_only_bordering_intersections
from algorithms.local_search import local_search_algorithm
from algorithms.genetic_algo import genetic_algorithm
import pandas as pd
import os
from grid_constants import RES_DIR


def main():
    local_search_scores = []
    genetic_algorithm_scores = []
    for _ in range(50):
        print("******************* Combat: ", _)
        initial_grid = generate_city_grid_with_only_bordering_intersections()
        
        best_grid, shortest_paths, local_cost = local_search_algorithm(initial_grid, max_iterations=400)
        local_search_scores.append(local_cost)

        optimized_grid, short_paths, genetic_cost = genetic_algorithm( population_size=10, generations=40, 
                                                                        mutation_rate=0.2, initial_grid=initial_grid)
        genetic_algorithm_scores.append(genetic_cost)
        
        print("Final cost after hill climbing: ", local_cost)
        print("Final cost after genetic algorithm: ", genetic_cost)
    
    comparision_df = pd.DataFrame({
    "iteration": list(range(1, 51)),
    "local_search_best_score": local_search_scores,
    "genetic_algorithm_best_score": genetic_algorithm_scores})

    local_better = sum(comparision_df["local_search_best_score"]<comparision_df["genetic_algorithm_best_score"])
    genetic_better = sum(comparision_df["local_search_best_score"]>comparision_df["genetic_algorithm_best_score"])

    print("Number of iterations where Local Search outperformed Genetic Algorithm:", local_better)
    print("Number of iterations where Genetic Algorithm outperformed Local Search:", genetic_better)

    comparision_df.to_csv(os.path.join(RES_DIR,"comparision.csv"), index=False)
    

if __name__ == "__main__":
    """
    Entry point for the script. Executes the `main` function when the script is run directly.
    """
    main()
