import pygame
import random

# Initialize Pygame
pygame.init()

# Set the dimensions of the game window
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400

# Set the dimensions of the grid
GRID_WIDTH = 20
GRID_HEIGHT = 20

# Set the colors for the tiles
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]

# Set the time for each level
TIME_PER_LEVEL = 60

# Set the number of levels
NUM_LEVELS = 3

#how often boxes move
GRID_UPDATE_INTERVAL = 1000  # 1000 milliseconds

# Nuke
bomb_active = False
bomb_radius = 0
bomb_max_radius = 5 * (GRID_WIDTH // 2)

#move spectrum boxes randomly
def update_grid_positions(grids):
    new_grids = []
    for grid in grids:
        x = random.randint(0, WINDOW_WIDTH // GRID_WIDTH - 1)
        y = random.randint(0, WINDOW_HEIGHT // GRID_HEIGHT - 1)
        new_grids.append((x, y))
    return new_grids

# Define a function to draw the grid
def draw_grid(surface):
    for i in range(0, WINDOW_WIDTH, GRID_WIDTH):
        pygame.draw.line(surface, (255, 255, 255), (i, 0), (i, WINDOW_HEIGHT))
    for j in range(0, WINDOW_HEIGHT, GRID_HEIGHT):
        pygame.draw.line(surface, (255, 255, 255), (0, j), (WINDOW_WIDTH, j))

# Define a function to generate a random color
def random_color():
    return random.choice(COLORS)

# Define a function to create a new level
def new_level(level):
    # Set the number of grids for this level
    num_grids = level * 2

    # Create a list of grids
    grids = []
    for i in range(num_grids):
        # Generate a random position for the grid
        x = random.randint(0, WINDOW_WIDTH // GRID_WIDTH - 1)
        y = random.randint(0, WINDOW_HEIGHT // GRID_HEIGHT - 1)

        # Add the grid to the list
        grids.append((x, y))

    # Set the time for this level
    time = TIME_PER_LEVEL - level * 5

    return grids, time

#End Splash
def show_end_screen(screen, score):
    screen.fill((0, 0, 0))
    
    final_font = pygame.font.SysFont(None, 50)
    final_text = final_font.render("Game Over!", True, (255, 255, 255))
    final_rect = final_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 30))
    if pygame.display.get_init():
        screen.blit(final_text, final_rect)
    
    score_font = pygame.font.SysFont(None, 30)
    score_text = score_font.render("Final Score: {}".format(score), True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 20))
    if pygame.display.get_init():
        screen.blit(score_text, score_rect)
    
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()



# Create the game window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Spectrum Sprint")

# Set the clock for the game
clock = pygame.time.Clock()

# Set the current level
level = 1

# Create the first level
grids, time_left = new_level(level)

# Create the player
player_pos = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
player_color = (255, 255, 255)

# Set the initial score
score = 0

# Initialize start_time
start_time = pygame.time.get_ticks()

#Splash Screen
splash_font = pygame.font.SysFont(None, 50)
splash_text = splash_font.render("Spectrum Sprint", True, (255, 255, 255))
splash_rect = splash_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
press_font = pygame.font.SysFont(None, 30)
press_text = press_font.render("Press Space to Begin", True, (255, 255, 255))
press_rect = press_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 50))

# Show the splash screen
screen.fill((0, 0, 0))
screen.blit(splash_text, splash_rect)
screen.blit(press_text, press_rect)
pygame.display.update()

# Wait for the player to press space
waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            waiting = False


# Initialize font
font = pygame.font.SysFont(None, 30)

running = True
game_over = False

# Initialize last_grid_update
last_grid_update = pygame.time.get_ticks()

# Start the game loop
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Nuke
            if event.key == pygame.K_SPACE:
                bomb_active = True
                bomb_radius = 0

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player_pos = (max(player_pos[0] - GRID_WIDTH, 0), player_pos[1])
    if keys[pygame.K_RIGHT]:
        player_pos = (min(player_pos[0] + GRID_WIDTH, WINDOW_WIDTH - GRID_WIDTH), player_pos[1])
    if keys[pygame.K_UP]:
        player_pos = (player_pos[0], max(player_pos[1] - GRID_HEIGHT, 0))
    if keys[pygame.K_DOWN]:
        player_pos = (player_pos[0], min(player_pos[1] + GRID_HEIGHT, WINDOW_HEIGHT - GRID_HEIGHT))

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the grids
    for grid in grids:
        x = grid[0] * GRID_WIDTH
        y = grid[1] * GRID_HEIGHT
        color = random_color()
        pygame.draw.rect(screen, color, (x, y, GRID_WIDTH, GRID_HEIGHT))

    # Draw the player
    pygame.draw.circle(screen, player_color, player_pos, GRID_WIDTH // 2)

    # Draw the grid lines
    draw_grid(screen)

    # Update the screen
    pygame.display.update()

    # Check for collision with the grids
    for grid in grids:
        x = grid[0] * GRID_WIDTH
        y = grid[1] * GRID_HEIGHT
        if player_pos[0] + GRID_WIDTH // 2 > x and player_pos[0] - GRID_WIDTH // 2 < x + GRID_WIDTH and \
            player_pos[1] + GRID_HEIGHT // 2 > y and player_pos[1] - GRID_HEIGHT // 2 < y + GRID_HEIGHT:
            grids.remove(grid)
            score += 1


    if bomb_active:
        bomb_radius += 8  # Increase the bomb radius

        # Add these lines to draw the expanding bomb circle
        if bomb_radius <= bomb_max_radius:
            pygame.draw.circle(screen, (255, 255, 255), player_pos, bomb_radius, 2)

        # Check for collision between the bomb circle and the glowing boxes
        grids_copy = grids.copy()
        for grid in grids_copy:
            x = grid[0] * GRID_WIDTH + GRID_WIDTH // 2
            y = grid[1] * GRID_HEIGHT + GRID_HEIGHT // 2
            distance = ((player_pos[0] - x)**2 + (player_pos[1] - y)**2)**0.5
            if distance <= bomb_radius:
                grids.remove(grid)
                score += 1

    pygame.display.update()  # Update the display again to show the bomb circle

    if bomb_radius > bomb_max_radius:  # If the bomb has reached its maximum radius, deactivate it
        bomb_active = False

    # Update the display again to show the bomb circle
    pygame.display.update()
    clock.tick(60)  # Control the speed of the bomb's expansion

    current_time = pygame.time.get_ticks()
    if current_time - last_grid_update >= GRID_UPDATE_INTERVAL:
        grids = update_grid_positions(grids)
        last_grid_update = current_time


    # Check if the level is over
    if not grids:
        level += 1
        if level > NUM_LEVELS:
            show_end_screen(screen, score)
            pygame.quit()
            quit
        else:
            grids, time_left = new_level(level)
            start_time = pygame.time.get_ticks()  # Reset the start_time for the new level

    # Update the timer
    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
    time_left = TIME_PER_LEVEL - elapsed_time
    if time_left <= 0:
        game_over = True
        running = False

    # Check if the level is over
    if not grids:
        level += 1
        if level > NUM_LEVELS:
            game_over = True
            running = False
        else:
            grids, time_left = new_level(level)
            start_time = pygame.time.get_ticks()  # Reset the start_time for the new level


# Print the final score and show the end screen
if game_over:
    show_end_screen(screen, score)

# Quit the game
pygame.quit()
quit()
