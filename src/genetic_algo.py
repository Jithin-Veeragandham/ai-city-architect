import random
from copy import deepcopy
import random
import heapq
import pygame
import random
from a_star_algo import *
from grid_generation import *
from helper import *
from visualization import *

from PIL import Image, ImageDraw, ImageFont


def calculate_fitness(grid, shortest_paths, path_penalty, intersection_penalty):
    """
    Calculate fitness scores for paths on a grid.
    """
    fitness_scores = {}

    for i, path in enumerate(shortest_paths, start=1):
        path_length = len(path)
        intersection_count = 0

        for (y, x), direction in path:
            if 0 <= y < len(grid) and 0 <= x < len(grid[0]) and 0 < y < len(grid) - 1 and 0 < x < len(grid[0]) - 1:
                if grid[y][x] == 3:  # Intersection
                    intersection_count += 1

        fitness = path_penalty * path_length + intersection_penalty * intersection_count
        fitness_scores[f"Path {i}"] = fitness

    return fitness_scores


def initialize_population(size, initial_grid):
    """
    Initialize a population by modifying the initial grid.
    """
    population = []
    for i in range(size):
        grid = deepcopy(initial_grid)
        grid_with_intersections = place_intersections_in_every_column_randomly(
            grid)
        population.append(grid_with_intersections)

    print(f"Initialized population of size {size}.")
    return population


def select_best_grids(population, fitness_scores, num_selected):
    """
    Select grids with the best (lowest) average fitness scores.
    """
    avg_fitness_scores = []
    for grid, fitness_dict in zip(population, fitness_scores):
        avg_fitness = sum(fitness_dict.values()) / len(fitness_dict)
        avg_fitness_scores.append((grid, avg_fitness))

    # Sort by average fitness (ascending)
    sorted_population = sorted(avg_fitness_scores, key=lambda x: x[1])

    # Select the best grids
    selected_population = [grid for grid,
                           _ in sorted_population[:num_selected]]
    avg_fitness = [fitness for _, fitness in sorted_population[:num_selected]]

    return selected_population, avg_fitness


# def crossover(grid1, grid2):
#     """
#     Create a child grid by combining two parent grids.
#     """
#     child_grid = []
#     for row1, row2 in zip(grid1, grid2):
#         child_row = [random.choice([cell1, cell2])
#                      for cell1, cell2 in zip(row1, row2)]
#         child_grid.append(child_row)
#     return child_grid


# def mutate(grid):
#     """
#     Randomly modify a grid while preserving the intersection count.
#     """
#     new_grid = deepcopy(grid)
#     intersections = [
#         (y, x) for y in range(1, len(new_grid) - 1)
#         for x in range(1, len(new_grid[0]) - 1) if new_grid[y][x] == 3
#     ]

#     if intersections:
#         y, x = random.choice(intersections)
#         new_grid[y][x] = 0  # Remove intersection

#         empty_cells = [
#             (new_y, new_x) for new_y in range(1, len(new_grid) - 1)
#             for new_x in range(1, len(new_grid[0]) - 1)
#             if new_grid[new_y][new_x] == 0
#         ]
#         if empty_cells:
#             new_y, new_x = random.choice(empty_cells)
#             new_grid[new_y][new_x] = 3  # Add a new intersection

#     return new_grid


def mutate(grid):
    """
    Randomly modify a grid while preserving the border intersections.
    """
    new_grid = deepcopy(grid)
    target_intersections = len(new_grid) + 1

    # Find all intersections
    intersections = [
        (y, x) for y in range(1, len(new_grid) - 1)
        for x in range(1, len(new_grid[0]) - 1)
        if new_grid[y][x] == 3
    ]

    if intersections:
        # Randomly select an intersection to move
        y, x = random.choice(intersections)

        # Find empty cells (0) to move to
        empty_cells = [
            (new_y, new_x) for new_y in range(1, len(new_grid) - 1)
            for new_x in range(1, len(new_grid[0]) - 1)
            if (new_grid[new_y][new_x] == 0 and
                new_y % 2 != 0)  # Satisfies y % 2 != 0
        ]

        if empty_cells:
            # Move the intersection to a random empty cell
            new_y, new_x = random.choice(empty_cells)
            new_grid[y][x] = 0  # Remove from the current position
            new_grid[new_y][new_x] = 3  # Place at the new position

    # Recalculate the number of intersections
    intersections = [
        (y, x) for y in range(1, len(new_grid) - 1)
        for x in range(1, len(new_grid[0]) - 1)
        if new_grid[y][x] == 3
    ]

    current_intersections = len(intersections)

    # Add intersections if needed
    if current_intersections < target_intersections:
        empty_cells = [
            (new_y, new_x) for new_y in range(1, len(new_grid) - 1)
            for new_x in range(1, len(new_grid[0]) - 1)
            if new_grid[new_y][new_x] == 0
        ]
        while current_intersections < target_intersections and empty_cells:
            new_y, new_x = random.choice(empty_cells)
            new_grid[new_y][new_x] = 3
            empty_cells.remove((new_y, new_x))
            current_intersections += 1

    # Remove intersections if needed
    elif current_intersections > target_intersections:
        while current_intersections > target_intersections:
            y, x = random.choice(intersections)
            new_grid[y][x] = 0
            intersections.remove((y, x))
            current_intersections -= 1

    return new_grid


def crossover(grid1, grid2):
    """
    Create a child grid by combining two parent grids while preserving border intersections.
    """
    child_grid = []
    for y in range(len(grid1)):
        child_row = []
        for x in range(len(grid1[0])):
            # Preserve border intersections
            if y == 0 or y == len(grid1) - 1 or x == 0 or x == len(grid1[0]) - 1:
                child_row.append(grid1[y][x])  # Always take parent1's border
            else:
                # Combine cells from both parents for non-border cells
                child_row.append(random.choice([grid1[y][x], grid2[y][x]]))
        child_grid.append(child_row)
    return child_grid


def save_city_grid_with_annotation(grid, shortest_paths, output_dir, filename, fitness, text_color="red", text_scale=1):
    """
    Saves a city grid with paths and annotations in one step.

    Parameters:
    - grid: The grid to save.
    - shortest_paths: Paths to overlay on the grid.
    - output_dir: Directory to save the output.
    - filename: Name of the file.
    - fitness: The fitness score to annotate.
    - text_color: Color of the annotation text.
    - text_scale: Scale factor for the text size.
    """
    # Visualize the grid and paths
    grid_image_path = os.path.join(output_dir, filename)
    # Generates a base grid visualization
    save_city_grid(grid, shortest_paths, output_dir, filename)

    # Open the image for annotation
    with Image.open(grid_image_path) as img:
        draw = ImageDraw.Draw(img)

        # Load a font with adjustable size
        font_size = 75 * text_scale  # Adjust base size
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except IOError:
            # Fallback to default font if arial.ttf is unavailable
            font = ImageFont.load_default()

        text = f"Best Fitness: {fitness:.2f}"

        # Annotate directly on the image
        text_position = (10 * text_scale, 10 * text_scale)
        draw.text(text_position, text, fill=text_color, font=font)

        # Save the final annotated image
        annotated_path = f"{grid_image_path}_fitness.png"
        img.save(annotated_path)

    # Optionally delete the unannotated version
    os.remove(grid_image_path)  # Clean up the intermediate grid image
    return annotated_path


def combine_images(image_paths, output_path, images_per_row=3, spacing=10):
    """
    Combine multiple images into a single composite image with spacing between images.

    Parameters:
    - image_paths: List of image file paths.
    - output_path: File path to save the combined image.
    - images_per_row: Number of images per row.
    - spacing: Space (in pixels) between images.
    """
    images = [Image.open(img_path) for img_path in image_paths]
    widths, heights = zip(*(img.size for img in images))

    # Determine grid size, including spacing
    max_width = max(widths)
    max_height = max(heights)
    num_rows = (len(images) + images_per_row - 1) // images_per_row

    # Calculate total canvas dimensions
    canvas_width = images_per_row * max_width + (images_per_row - 1) * spacing
    canvas_height = num_rows * max_height + (num_rows - 1) * spacing

    # Create a blank canvas
    composite = Image.new("RGB", (canvas_width, canvas_height), "white")

    # Paste each image onto the canvas with spacing
    for index, img in enumerate(images):
        x = (index % images_per_row) * (max_width + spacing)
        y = (index // images_per_row) * (max_height + spacing)
        composite.paste(img, (x, y))

    composite.save(output_path)


def remove_images_by_prefix(directory, prefix):
    """
    Remove all files in the specified directory that start with the given prefix.

    Parameters:
    - directory: Path to the directory.
    - prefix: The prefix to match files.
    """
    try:
        for filename in os.listdir(directory):
            if filename.startswith(prefix):
                file_path = os.path.join(directory, filename)
                if os.path.isfile(file_path):  # Ensure it's a file
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
    except Exception as e:
        print(f"Error: {e}")


def genetic_algorithm(path_penalty, intersection_penalty, population_size, generations, mutation_rate, initial_grid):
    """
    Main genetic algorithm.
    """
    population = initialize_population(population_size, initial_grid)

    for generation in range(generations):
        fitness_scores = []
        for grid in population:
            shortest_paths = find_all_shortest_paths(grid)
            fitness = calculate_fitness(
                grid, shortest_paths, path_penalty, intersection_penalty)
            fitness_scores.append(fitness)

        # Select the best grids
        selected_population, avg_fitness = select_best_grids(
            population, fitness_scores, num_selected=6)

        dir_path = os.path.join(
            rf"D:\NEU MS CS\FAI\Project\ai-city-architect\res\GeneticAlgorithm")
        image_paths = []
        # Debug: Visualize the best grid (if visualization tools exist)
        for i, grid in enumerate(selected_population):
            shortest_paths = find_all_shortest_paths(grid)
            # visualize_grid_with_paths_pil(
            #     grid,
            #     shortest_paths,
            #     output_dir='img',
            #     filename_prefix=f'generation_{generation+1}_grid_{i+1}'
            # )
            # grid_path = os.path.join(
            #     dir_path, f"generation_{generation+1}_grid_{i+1}.png")
            # save_city_grid(grid, shortest_paths, dir_path,
            #                f"generation_{generation+1}_grid_{i+1}.png")
            annotated_path = save_city_grid_with_annotation(
                grid, shortest_paths, dir_path, f"generation_{generation+1}_grid_{i+1}.png", avg_fitness[i]
            )

            image_paths.append(annotated_path)

            print(
                f"Generation {generation + 1}, Grid {i + 1} (Fitness: {avg_fitness[i]})")
        combine_images(image_paths, os.path.join(
            dir_path, f"Generation_{generation+1}_summary.png"))
        directory = r"D:\NEU MS CS\FAI\Project\ai-city-architect\res\GeneticAlgorithm"

        prefix = "generation_"
        remove_images_by_prefix(directory, prefix)
        # Create new population via crossover
        new_population = []
        while len(new_population) < population_size:
            parent1, parent2 = random.sample(selected_population, 2)
            child = crossover(parent1, parent2)
            new_population.append(child)

        # Apply mutation
        population = [mutate(grid) if random.random() <
                      mutation_rate else grid for grid in new_population]

        # Log best fitness of the generation
        print(
            f"Generation {generation + 1}: Best Fitness = {min(avg_fitness)}")

    # Return the best grid
    best_index = avg_fitness.index(min(avg_fitness))
    return selected_population[best_index]
