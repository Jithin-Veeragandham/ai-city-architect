import pygame
from constants import CELL_SIZE

def load_images():
    """
    Loads images for each type of grid element (building, emergency service, etc.).
    Scales the images to fit within the grid cells.
    """
    print("Loading images...")
    images = {
        1: pygame.image.load('res/building.jpg'),           # Building image (jpeg format)
        2: pygame.image.load('res/emergency.png')           # Emergency service image (png format)
        # You can add more images for roads and intersections here
    }
    
    # Scale all images to fit into the grid cells
    for key in images:
        images[key] = pygame.transform.scale(images[key], (CELL_SIZE, CELL_SIZE))
    
    print("Images loaded and scaled.")
    return images

def visualize_city_grid_with_offset_paths(grid, paths):
    """ 
    Visualizes the grid with buildings, emergency services, and roads using PyGame.
    Also visualizes the shortest paths between buildings and emergency services, each in a unique color with slight offsets for overlapping paths.
    """
    images = load_images()
    pygame.init()  # Initialize PyGame
    screen = pygame.display.set_mode((len(grid) * CELL_SIZE, len(grid) * CELL_SIZE))  # Set screen size
    pygame.display.set_caption("City Layout with Offset Paths")  # Window title

    clock = pygame.time.Clock()  # Set up the clock for controlling frame rate
    running = True  # Game loop control variable

    # Define a list of colors for the paths, avoiding green (the intersection color)
    path_colors = [(255, 0, 0), (0, 0, 255), (255, 165, 0), (255, 255, 0), 
                   (0, 255, 255), (255, 0, 255), (128, 0, 128), (0, 128, 128), 
                   (255, 192, 203), (0, 100, 0), (139, 69, 19), (75, 0, 130), 
                   (128, 128, 128), (100, 149, 237), (199, 21, 133)]

    path_thickness = 6  # Set the thickness for paths
    max_offset = 3  # Set maximum offset for paths to avoid overflowing outside the cell
    road_color = (169, 169, 169)  # Gray for roads
    road_border_color = (255, 255, 255)  # White for road borders
    border_thickness = 3  # Thickness of the white border

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Quit the game if the close button is pressed
                running = False

        screen.fill((128, 128, 128))  # Gray background

        # Draw the grid using images (building, emergency services, etc.)
        for y in range(len(grid)):
            for x in range(len(grid)):
                cell_value = grid[y][x]
                if cell_value in images:  # If the cell has a corresponding image (building or emergency)
                    screen.blit(images[cell_value], (x * CELL_SIZE, y * CELL_SIZE))  # Draw the image
                elif cell_value == 3:  # If the cell is an intersection
                    pygame.draw.rect(screen, (52, 251, 152), (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))  # Draw intersections in green
                elif cell_value == 0:  # Draw roads with a border
                    # Draw the white border for the road
                    pygame.draw.rect(screen, road_border_color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                    # Draw the inner part of the road (smaller than the cell to show the border)
                    pygame.draw.rect(screen, road_color, 
                                     (x * CELL_SIZE + border_thickness, 
                                      y * CELL_SIZE + border_thickness, 
                                      CELL_SIZE - 2 * border_thickness, 
                                      CELL_SIZE - 2 * border_thickness))

        # Draw the paths in different colors with slight offsets for overlapping paths
        for i, path in enumerate(paths):
            path_color = path_colors[i % len(path_colors)]  # Cycle through colors if there are more paths than colors
            for (coord, direction) in path:
                x,y=coord
                if grid[y][x] != 1 and grid[y][x] != 2:  # Only color if it's a road (0), to avoid coloring buildings, emergency services, or intersections
                    # Calculate the offset based on the index of the path to avoid overlap
                    offset_x = (i % max_offset) * 2  # Offset in x-direction
                    offset_y = (i % max_offset) * 2  # Offset in y-direction
                    
                    # Ensure the rectangle fits within the cell and apply a small offset
                    pygame.draw.rect(
                        screen, 
                        path_color, 
                        (x * CELL_SIZE + offset_x, y * CELL_SIZE + offset_y, CELL_SIZE - max_offset, CELL_SIZE - max_offset),
                        path_thickness
                    )

        pygame.display.flip()  # Update the display
        clock.tick(30)  # Control the frame rate (30 FPS)
    pygame.quit()  # Properly shut down PyGame
