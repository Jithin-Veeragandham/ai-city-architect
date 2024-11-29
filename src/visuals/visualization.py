from PIL import Image, ImageDraw, ImageFont
import os
from grid_constants import RES_DIR


def load_images(cell_size):
    """
    Loads and resizes images representing grid elements (e.g., buildings, emergency services).
    Uses Pillow to open images and scale them to fit the specified cell size.

    Parameters:
        cell_size (int): The size of each grid cell in pixels.

    Returns:
        dict: A dictionary mapping grid element values (e.g., 1 for building, 2 for emergency service)
              to their corresponding resized Pillow Image objects.
    """
    # print("Loading images...")
    images = {
        1: Image.open(os.path.join(RES_DIR,"building.jpg")).resize((cell_size, cell_size)),  # Building image (JPEG format)
        2: Image.open(os.path.join(RES_DIR,"emergency.png")).resize((cell_size, cell_size)),  # Emergency service image (PNG format)
    }
    # print("Images loaded and scaled.")
    return images


def save_city_grid(grid, paths, dir_name, output_file_name):
    """
    Visualizes a city grid and its shortest paths using Pillow and saves the visualization as an image.

    Steps:
    1. Loads images for buildings and emergency services.
    2. Draws roads, intersections, and grid elements (buildings and emergency services) onto the image.
    3. Draws paths on top of the grid, differentiating them with colors and offsets to avoid overlap.
    4. Saves the final visualization to the specified directory and file name.

    Parameters:
        grid (list[list[int]]): The 2D grid representing the city. 
                                - 0: Roads
                                - 1: Buildings
                                - 2: Emergency services
                                - 3: Intersections
        paths (list[list[tuple]]): List of shortest paths, where each path is a list of nodes (coordinates and directions).
        dir_name (str): Directory where the image should be saved.
        output_file_name (str): Name of the output image file.

    Returns:
        None
    """
    # Load images
    CELL_SIZE = 80
    images = load_images(CELL_SIZE)

    # Define colors
    intersection_color = (52, 251, 152)  # Green
    road_color = (169, 169, 169)  # Gray
    road_border_color = (255, 255, 255)  # White
    border_thickness =  6 # Thickness of the road border
    
    # Path colors
    path_colors = [(255, 0, 0), (0, 0, 255), (255, 165, 0), (255, 255, 0), 
                   (0, 255, 255), (255, 0, 255), (128, 0, 128), (0, 128, 128), 
                   (255, 192, 203), (0, 100, 0), (139, 69, 19), (75, 0, 130), 
                   (128, 128, 128), (100, 149, 237), (199, 21, 133)]
    
    path_thickness = 6  # Border thickness for paths
    max_offset = 6  # Maximum offset to avoid overlapping

    # Image dimensions
    grid_size = len(grid)
    image_size = (grid_size * CELL_SIZE, grid_size * CELL_SIZE)

    # Create a blank image and drawing object
    img = Image.new("RGB", image_size, (128, 128, 128))  # Gray background
    draw = ImageDraw.Draw(img)

    # Draw the grid elements (roads, intersections, buildings, emergency services)
    for y in range(grid_size):
        for x in range(grid_size):
            top_left = (x * CELL_SIZE, y * CELL_SIZE)
            bottom_right = (top_left[0] + CELL_SIZE, top_left[1] + CELL_SIZE)
            
            if grid[y][x] == 3:  # Intersection
                draw.rectangle([top_left, bottom_right], fill=intersection_color)
            elif grid[y][x] == 0:  # Road
                # Draw road border
                draw.rectangle([top_left, bottom_right], fill=road_border_color)
                # Draw inner road
                inner_top_left = (top_left[0] + border_thickness, top_left[1] + border_thickness)
                inner_bottom_right = (bottom_right[0] - border_thickness, bottom_right[1] - border_thickness)
                draw.rectangle([inner_top_left, inner_bottom_right], fill=road_color)
            elif grid[y][x] in images:  # Buildings or emergency services
                # Paste the corresponding image
                img.paste(images[grid[y][x]], top_left)

    # Draw the paths (on top of all grid elements)
    for i, path in enumerate(paths):
        path_color = path_colors[i % len(path_colors)]  # Cycle through colors
        for (coord, direction) in path:
            x, y = coord
            # Calculate the offset to differentiate overlapping paths
            offset_x = (i % max_offset) * 2  # Offset in x-direction
            offset_y = (i % max_offset) * 2  # Offset in y-direction

            # Define the rectangle's corners for the hollow square
            path_top_left = (x * CELL_SIZE + offset_x, y * CELL_SIZE + offset_y)
            path_bottom_right = (
                path_top_left[0] + CELL_SIZE - max_offset,
                path_top_left[1] + CELL_SIZE - max_offset,
            )
            
            # Draw a hollow square (thick border only) for the path
            draw.rectangle(
                [path_top_left, path_bottom_right],
                outline=path_color,  # Border color
                width=path_thickness  # Border thickness
            )

    # Ensure the output directory exists
    os.makedirs(dir_name, exist_ok=True)

    # Save the image
    full_path = os.path.join(dir_name, output_file_name)
    img.save(full_path)
    # print(f"City grid visualization saved as {full_path}")

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
        font_size = 175 * text_scale  # Adjust base size
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