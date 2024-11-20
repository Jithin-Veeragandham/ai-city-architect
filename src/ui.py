import random
import pygame
import math 

def load_images(CELL_SIZE):
    """
    Loads images for each type of grid element (building, emergency service, etc.).
    Scales the images to fit within the grid cells.
    """
    print("Loading images...")
    images = {
        2: pygame.image.load('../res/emergency.png'),
        'I': pygame.image.load('../res/i.png'),
        'H': pygame.image.load('../res/h.png'),
        'V': pygame.image.load('../res/v.png'),
        'LV': pygame.image.load('../res/lv.png'),
        'RV': pygame.image.load('../res/rv.png'),
        'TH': pygame.image.load('../res/th.png'),
        'BH': pygame.image.load('../res/bh.png'),
        'TRC': pygame.image.load('../res/trc.png'),
        'BRC': pygame.image.load('../res/brc.png'),
        'TLC': pygame.image.load('../res/tlc.png'),
        'BLC': pygame.image.load('../res/blc.png'),
    }

    # Load multiple tree images
    tree_images = []
    for i in range(1, 11):
        try:
            img = pygame.image.load(f'../res/t{i}.png')
            tree_images.append(img)
        except pygame.error:
            print(f"Warning: Could not load t{i}.png")

    if not tree_images:
        # Fallback to original tree image if no new images could be loaded
        tree_images = [pygame.image.load('../res/tree.png')]

    images[0] = tree_images

    # Load multiple building images
    building_images = []
    for i in range(1, 10):  # Assuming you have building1.png through building5.png
        try:
            img = pygame.image.load(f'../res/b{i}.png')
            building_images.append(img)
        except pygame.error:
            print(f"Warning: Could not load b{i}.png")
    
    if not building_images:
        # Fallback to original building image if no new images could be loaded
        building_images = [pygame.image.load('./res/building.jpg')]
    
    # Store building images separately
    images['buildings'] = building_images
    
    # Scale all images to fit into the grid cells
    for key in images:
        if key == 'buildings':
            images['buildings'] = [pygame.transform.scale(img, (CELL_SIZE, CELL_SIZE)) 
                                 for img in images['buildings']]
        elif key == 0:
            images[0] = [pygame.transform.scale(img, (CELL_SIZE, CELL_SIZE)) 
                         for img in images[0]]
        else:
            images[key] = pygame.transform.scale(images[key], (CELL_SIZE, CELL_SIZE))
    
    print("Images loaded and scaled.")
    return images

class SmokeParticle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(2, 4)
        self.life = 1.0  # Start at full opacity
        self.fade_speed = random.uniform(0.02, 0.04)
        self.dx = random.uniform(-0.5, 0.5)
        self.dy = random.uniform(-0.5, 0.5)

class Vehicle:
    def __init__(self, start_pos, path, color, CELL_SIZE):
        self.path = path
        self.current_path_index = 0
        self.CELL_SIZE = CELL_SIZE
        self.position = [start_pos[0] * CELL_SIZE + CELL_SIZE/2, start_pos[1] * CELL_SIZE + CELL_SIZE/2]
        self.target_position = None
        self.speed = 1
        self.car_size = (20, 20)  # Size for the car image
        self.active = True
        self.color = color
        self.offset = CELL_SIZE * 0.25  # Offset for the car image
        self.current_offset_x = 0
        self.current_offset_y = 0
        self.current_direction = None
        self.car_image = pygame.image.load('../res/car.png')
        self.car_image = pygame.transform.scale(self.car_image, self.car_size)
        self.original_car_image = self.car_image  # Store original image for rotation
        self.smoke_particles = []
        self.smoke_timer = 0
        self.update_target()

    def calculate_direction(self, current, next_pos):
        dx = next_pos[0] - current[0]
        dy = next_pos[1] - current[1]
        if dx > 0: return "right"
        if dx < 0: return "left"
        if dy > 0: return "down"
        return "up"

    def rotate_car(self):
        if self.current_direction == "right":
            self.car_image = pygame.transform.rotate(self.original_car_image, -90)
        elif self.current_direction == "left":
            self.car_image = pygame.transform.rotate(self.original_car_image, 90)
        elif self.current_direction == "down":
            self.car_image = pygame.transform.rotate(self.original_car_image, 180)
        else:  # up
            self.car_image = pygame.transform.rotate(self.original_car_image, 0)

    def update_target(self):
        if self.current_path_index < len(self.path) - 1:
            current = self.path[self.current_path_index]
            next_pos = self.path[self.current_path_index + 1]
            
            new_direction = self.calculate_direction(current, next_pos)
            
            if new_direction == "right":
                self.current_offset_x = 0
                self.current_offset_y = self.offset
            elif new_direction == "left":
                self.current_offset_x = 0
                self.current_offset_y = -self.offset
            elif new_direction == "down":
                self.current_offset_x = -self.offset
                self.current_offset_y = 0
            else:  # up
                self.current_offset_x = self.offset
                self.current_offset_y = 0
            
            if new_direction != self.current_direction:
                self.current_direction = new_direction
                self.rotate_car()
            
            self.target_position = (
                next_pos[0] * self.CELL_SIZE + self.CELL_SIZE/2 + self.current_offset_x,
                next_pos[1] * self.CELL_SIZE + self.CELL_SIZE/2 + self.current_offset_y
            )

    def update_smoke(self):
        # Add new smoke particles
        self.smoke_timer += 1
        if self.smoke_timer >= 5:  # Add smoke every 5 frames
            self.smoke_timer = 0
            # Position smoke based on car's direction
            if self.current_direction == "right":
                smoke_x = self.position[0] + self.current_offset_x - 10
                smoke_y = self.position[1] + self.current_offset_y
            elif self.current_direction == "left":
                smoke_x = self.position[0] + self.current_offset_x + 10
                smoke_y = self.position[1] + self.current_offset_y
            elif self.current_direction == "down":
                smoke_x = self.position[0] + self.current_offset_x
                smoke_y = self.position[1] + self.current_offset_y - 10
            else:  # up
                smoke_x = self.position[0] + self.current_offset_x
                smoke_y = self.position[1] + self.current_offset_y + 10
            
            self.smoke_particles.append(SmokeParticle(smoke_x, smoke_y))

        # Update existing particles
        for particle in self.smoke_particles:
            particle.x += particle.dx
            particle.y += particle.dy
            particle.life -= particle.fade_speed
            
        # Remove dead particles
        self.smoke_particles = [p for p in self.smoke_particles if p.life > 0]

    def move(self):
        if not self.active or not self.target_position:
            return

        dx = self.target_position[0] - (self.position[0] + self.current_offset_x)
        dy = self.target_position[1] - (self.position[1] + self.current_offset_y)
        distance = math.sqrt(dx**2 + dy**2)

        if distance < self.speed:
            self.position[0] = self.target_position[0] - self.current_offset_x
            self.position[1] = self.target_position[1] - self.current_offset_y
            self.current_path_index += 1
            
            if self.current_path_index >= len(self.path) - 1:
                self.active = False
                return
            
            self.update_target()
        else:
            move_x = (dx / distance) * self.speed
            move_y = (dy / distance) * self.speed
            self.position[0] += move_x
            self.position[1] += move_y

def change_grid(grid):
    
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (i == 0 or i == len(grid) - 1) and (grid[i][j] != 'BH' or grid[i][j] != 'TH') and grid[i][j] == 3:
                grid[i][j] = 'H'

            if i % 2 == 0 and grid[i][j] == 0:
                grid[i][j] = 'H'

            if i % 2 == 0 and grid[i][j] == 3 and j != 0 and j != len(grid[i]) - 1 and i != 0 and i != len(grid) - 1:
                grid[i][j] = 'I'

            if i % 2 == 0 and j == 0:
                grid[i][j] = 'LV'

            if i % 2 == 0 and j == len(grid[i]) - 1:
                grid[i][j] = 'RV'

            if grid[i][j] == 'I' and i != 0 and i != len(grid) - 1:
                if grid[i-1][j] == 0:
                    grid[i-1][j] = 'V'
                    grid[i-2][j] = 'TH'
                if grid[i+1][j] == 0:
                    grid[i+1][j] = 'V'
                    grid[i+2][j] = 'BH'

            if i % 2 == 1 and (j == 0 or j == len(grid[i]) - 1):
                grid[i][j] = 'V'

            if i % 2 == 1 and grid[i][j] == 3 and i != len(grid) - 1 and i != 0 and j != 0 and j != len(grid[i]) - 1:
                grid[i][j] = 'V'
                grid[i-1][j] = 'TH'
                grid[i+1][j] = 'BH'

       
    grid[0][0] = 'TLC'
    grid[0][len(grid[0]) - 1] = 'TRC'
    grid[len(grid) - 1][0] = 'BLC'
    grid[len(grid) - 1][len(grid[0]) - 1] = 'BRC'

def visualize_city_grid_with_vehicles(grid, paths_with_directions, CELL_SIZE=40):
    paths = [] # path_with_directions
    for i in range(len(paths_with_directions)):
        path_with_directions = paths_with_directions[i]
        path_without_directions = []
        for j in range(len(path_with_directions)):
            path_without_directions.append(path_with_directions[j][0])
        paths.append(path_without_directions)

    change_grid(grid)
    check_paths(grid, paths)
    
    images = load_images(CELL_SIZE)

    pygame.init()

    screen = pygame.display.set_mode((len(grid) * CELL_SIZE, len(grid) * CELL_SIZE))
    pygame.display.set_caption("City Layout with Vehicles")
    
    # Define a list of light, distinct background colors for buildings
    building_bg_colors = [
        (255, 223, 223),  # Light red
        (223, 255, 223),  # Light green
        (223, 223, 255),  # Light blue
        (255, 255, 223),  # Light yellow
        (255, 223, 255),  # Light magenta
        (223, 255, 255),  # Light cyan
    ]

    # Create a mapping for building positions to their randomly chosen images
    building_image_map = {}
    building_colors_map = {}
    tree_images_map = {}
    for y in range(len(grid)):
        for x in range(len(grid)):
            if grid[y][x] == 1:
                building_image_map[(x, y)] = random.choice(images['buildings'])
                building_colors_map[(x, y)] = random.choice(building_bg_colors)
            elif grid[y][x] == 0:
                tree_images_map[(x, y)] = random.choice(images[0])

    
    clock = pygame.time.Clock()
    running = True
    building_border_color = (100, 100, 100)
    
    path_colors = [
        (255, 0, 0),    # Red
        (0, 0, 255),    # Blue
        (255, 165, 0),  # Orange
        (128, 0, 128),  # Purple
        (0, 128, 0),    # Dark Green
        (255, 20, 147), # Pink
        (0, 255, 255),  # Cyan
        (255, 215, 0),  # Gold
        (139, 69, 19),  # Brown
        (75, 0, 130),   # Indigo
    ]
    
    building_colors = {}
    vehicles = []
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                cell_x = mouse_x // CELL_SIZE
                cell_y = mouse_y // CELL_SIZE
                
                if grid[cell_y][cell_x] == 1:
                    building_key = (cell_x, cell_y)
                    if building_key not in building_colors:
                        building_colors[building_key] = path_colors[len(building_colors) % len(path_colors)]
                    
                    for path in paths:
                        if path[0] == (cell_x, cell_y):
                            vehicles.append(Vehicle((cell_x, cell_y), path, building_colors[building_key], CELL_SIZE))
        
        screen.fill((34, 139, 34))  # Dark gray background
        
        # Draw grid
        for y in range(len(grid)):
            for x in range(len(grid)):
                cell_value = grid[y][x]
                if cell_value == 1:
                    # Draw building background and border
                    cell_rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(screen, building_colors_map[(x, y)], cell_rect)
                    pygame.draw.rect(screen, building_border_color, cell_rect, 2)
                    
                    # Calculate position to center the smaller building image
                    building_img = building_image_map[(x, y)]
                    img_x = x * CELL_SIZE + (CELL_SIZE - building_img.get_width()) // 2
                    img_y = y * CELL_SIZE + (CELL_SIZE - building_img.get_height()) // 2
                    screen.blit(building_img, (img_x, img_y))

                elif cell_value == 0:
                    # Use the pre-mapped random tree image for this position
                    screen.blit(tree_images_map[(x, y)], (x * CELL_SIZE, y * CELL_SIZE)) 

                elif cell_value in images:
                    screen.blit(images[cell_value], (x * CELL_SIZE, y * CELL_SIZE))

                elif cell_value == 1:
                    pygame.draw.rect(screen, building_border_color, cell_rect, 2)
                
        
        # Rest of the visualization code remains the same...
        for vehicle in vehicles:
            if vehicle.active:
                vehicle.move()
                vehicle.update_smoke()
                
                for particle in vehicle.smoke_particles:
                    alpha = int(255 * particle.life)
                    smoke_surface = pygame.Surface((particle.size, particle.size), pygame.SRCALPHA)
                    pygame.draw.circle(smoke_surface, (128, 128, 128, alpha), 
                                    (particle.size//2, particle.size//2), particle.size//2)
                    screen.blit(smoke_surface, (int(particle.x), int(particle.y)))
                
                car_x = int(vehicle.position[0] + vehicle.current_offset_x - vehicle.car_size[0]/2)
                car_y = int(vehicle.position[1] + vehicle.current_offset_y - vehicle.car_size[1]/2)
                screen.blit(vehicle.car_image, (car_x, car_y))
        
        vehicles = [v for v in vehicles if v.active]
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

def check_paths(grid, paths):
    for path in paths:
        for i in range(len(path) - 1):
            if grid[path[i][1]][path[i][0]] == 0:
                grid[path[i][1]][path[i][0]] = 'V'
                grid[path[i-1][1]][path[i][0]] = 'TH'
                grid[path[i+1][1]][path[i][0]] = 'BH'

    