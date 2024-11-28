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
from objective import *
from local_search import *

from PIL import Image, ImageDraw, ImageFont
dir_path = os.path.join(
    rf"D:\NEU MS CS\FAI\Project\ai-city-architect\res\GeneticAlgorithm")


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
                    # print(f"Deleted: {file_path}")
    except Exception as e:
        print(f"Error: {e}")


def genetic_algorithm(population_size, generations, mutation_rate, initial_grid):
    """
    Main genetic algorithm with elitism to preserve the best grid.
    """
    population = initialize_population(population_size, initial_grid)
    best_grid = None
    best_fitness = float('inf')  # Initialize with a very high fitness score

    for generation in range(generations):
        fitness_scores = []
        for grid in population:
            shortest_paths = find_all_shortest_paths(grid)
            fitness = calculate_fitness(grid, shortest_paths)
            fitness_scores.append(fitness)

        # Select the best grids
        selected_population, avg_fitness = select_best_grids(
            population, fitness_scores, num_selected=6)

        # Identify the best grid in the current generation
        current_best_index = avg_fitness.index(min(avg_fitness))
        current_best_grid = selected_population[current_best_index]
        current_best_fitness = avg_fitness[current_best_index]

        # Update the global best grid if the current best is better
        if current_best_fitness < best_fitness:
            best_grid = current_best_grid
            best_fitness = current_best_fitness

        image_paths = []

        # Visualize the selected grids
        for i, grid in enumerate(selected_population):
            shortest_paths = find_all_shortest_paths(grid)
            annotated_path = save_city_grid_with_annotation(
                grid, shortest_paths, dir_path, f"generation_{generation+1}_grid_{i+1}.png", avg_fitness[i]
            )
            image_paths.append(annotated_path)

            print(
                f"Generation {generation + 1}, Grid {i + 1} (Fitness: {avg_fitness[i]})")

        combine_images(image_paths, os.path.join(
            dir_path, f"Generation_{generation+1}_summary.png"))
        remove_images_by_prefix(dir_path, "generation_")

        # Create a new population with the best grid explicitly included
        new_population = []  # Start with the best grid
        while len(new_population) < population_size:
            parent1, parent2 = random.sample(selected_population, 2)
            parent1_paths = find_all_shortest_paths(parent1)
            parent2_paths = find_all_shortest_paths(parent2)
            child = best_path_retention(
                parent1, parent2, parent1_paths, parent2_paths)
            new_population.append(child)

        # Apply mutation
        population = [generate_neighbor(grid) if random.random() <
                      mutation_rate else grid for grid in new_population]

        # Log the best fitness of the generation
        print(
            f"Generation {generation + 1}: Best Fitness = {current_best_fitness}")
    short_paths = find_all_shortest_paths(current_best_grid)
    # Return the globally best grid
    return best_grid, short_paths
