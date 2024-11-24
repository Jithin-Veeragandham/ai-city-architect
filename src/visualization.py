from grid_constants import CELL_SIZE
from PIL import Image, ImageDraw
import os


def load_images(cell_size):
    """
    Loads images for each type of grid element (building, emergency service, etc.).
    Scales the images to fit within the grid cells using Pillow.
    """
    print("Loading images...")
    images = {
        1: Image.open("project py files\\ai-city-architect\\res\\building.jpg").resize(
            (cell_size, cell_size)
        ),  # Building image (JPEG format)
        2: Image.open("project py files\\ai-city-architect\\res\\emergency.png").resize(
            (cell_size, cell_size)
        ),  # Emergency service image (PNG format)
    }
    print("Images loaded and scaled.")
    return images


def save_city_grid(grid, paths, dir_name, output_file_name, cell_size=30):
    """
    Visualizes the grid with buildings, emergency services, roads, and paths using Pillow.
    Draws paths on top of intersections for better visualization.
    """
    # Load images
    images = load_images(cell_size)

    # Define colors
    intersection_color = (52, 251, 152)  # Green
    road_color = (169, 169, 169)  # Gray
    road_border_color = (255, 255, 255)  # White
    border_thickness = 3  # Thickness of the road border
    
    # Path colors
    path_colors = [(255, 0, 0), (0, 0, 255), (255, 165, 0), (255, 255, 0), 
                   (0, 255, 255), (255, 0, 255), (128, 0, 128), (0, 128, 128), 
                   (255, 192, 203), (0, 100, 0), (139, 69, 19), (75, 0, 130), 
                   (128, 128, 128), (100, 149, 237), (199, 21, 133)]
    
    path_thickness = 6  # Border thickness for paths
    max_offset = 3  # Maximum offset to avoid overlapping

    # Image dimensions
    grid_size = len(grid)
    image_size = (grid_size * cell_size, grid_size * cell_size)

    # Create a blank image and drawing object
    img = Image.new("RGB", image_size, (128, 128, 128))  # Gray background
    draw = ImageDraw.Draw(img)

    # Draw the grid elements (roads, intersections, buildings, emergency services)
    for y in range(grid_size):
        for x in range(grid_size):
            top_left = (x * cell_size, y * cell_size)
            bottom_right = (top_left[0] + cell_size, top_left[1] + cell_size)
            
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
            path_top_left = (x * cell_size + offset_x, y * cell_size + offset_y)
            path_bottom_right = (
                path_top_left[0] + cell_size - max_offset,
                path_top_left[1] + cell_size - max_offset,
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
    print(f"City grid visualization saved as {full_path}")