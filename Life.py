import pygame # type: ignore
import random

BACKGROUND_COLOR = (15, 10, 10)
GRID_LINES_COLOR = (29, 29, 29)
CELL_COLOR = (134, 203, 146)

canvas_width, canvas_height = 1000, 1000
pixel_width = 100

simulate_game = False
generation = 0
population = 0

zoom_level = 1.0
zoom_increment = 0.1

is_panning = False
pan_start_pos = (0, 0)
offset = [0, 0]

grid = {}

pygame.init()
screen = pygame.display.set_mode((canvas_width, canvas_height))
pygame.display.set_caption("Life")
clock = pygame.time.Clock()


def draw_grid():
    screen.fill(BACKGROUND_COLOR)
    for (x, y) in grid:
        x_pos = x * get_cell_size() + offset[0]
        y_pos = y * get_cell_size() + offset[1]

        pygame.draw.rect(screen, CELL_COLOR, (x_pos, y_pos, get_cell_size(), get_cell_size()))



def simulate():
    global grid, generation, population

    # Create new grid for next generation
    next_grid = {}

    for (x, y) in grid:
        live_neighbors = count_cell_live_neighbors(x, y) # Get amount of live neighbors

        if live_neighbors == 2 or live_neighbors == 3:
            next_grid[(x, y)] = 1

        for i in get_cell_neighbors(x, y): # Check all neighbors
            if i not in grid: # Check if the neighbor is a 1 (alive)
                live_neighbors = count_cell_live_neighbors(i[0], i[1]) # Check that neighbors amount of neighbors
                if live_neighbors == 3:
                    next_grid[i] = 1 # Set that neighbor to 1 (alive) if it has 3 neighbors

    grid = next_grid # Set the grid to the new generation grid
    generation += 1
    population = len(grid)


def get_cell_neighbors(x, y):
    neighbors = []
    for i in range(x - 1, x + 2):
        for j in range(y - 1, y + 2):
            if (i, j) != (x, y):  # Exclude the cell itself
                neighbors.append((i, j))
    return neighbors


def count_cell_live_neighbors(x, y):
    neighbors = get_cell_neighbors(x, y)
    live_neighbors = 0
    for i in neighbors:
        if i in grid:
            live_neighbors += 1
    return live_neighbors


def draw_cell(x, y):
    grid[(x, y)] = 1


def erase_cell(x, y):
    if (x, y) in grid:
        del grid[(x, y)]


def get_cell_size():
    return int(pixel_width * zoom_level)


def zoom_in():
    global zoom_level
    zoom_level = min(zoom_level + zoom_increment, 3.0)


def zoom_out():
    global zoom_level
    zoom_level = max(zoom_level - zoom_increment, 0.1)



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                simulate_game = not simulate_game
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Scroll wheel up
                zoom_in()
            elif event.button == 5:  # Scroll wheel down
                zoom_out()
            elif event.button == 2:  # Middle mouse button
                  is_panning = True
                  pan_start_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
          if event.button == 2:  # Middle mouse button
              is_panning = False
        elif event.type == pygame.MOUSEMOTION:
            mouse_position = event.pos
            if is_panning:
                dx = mouse_position[0] - pan_start_pos[0]
                dy = mouse_position[1] - pan_start_pos[1]
                offset[0] += dx
                offset[1] += dy
                pan_start_pos = mouse_position

    draw_grid()

    # Draw grid lines
    for x in range(offset[0] % get_cell_size(), canvas_width, get_cell_size()):
        pygame.draw.line(screen, GRID_LINES_COLOR, (x, 0), (x, canvas_height))
    for y in range(offset[1] % get_cell_size(), canvas_height, get_cell_size()):
        pygame.draw.line(screen, GRID_LINES_COLOR, (0, y), (canvas_width, y))


    if not simulate_game:
        pygame.draw.rect(screen, (255, 0, 0), (10, 10, 15, 15))
        mouse_buttons = pygame.mouse.get_pressed()

        x, y = pygame.mouse.get_pos()
        grid_x = (x - offset[0]) // get_cell_size()
        grid_y = (y - offset[1]) // get_cell_size()

        if mouse_buttons[0]:
            draw_cell(grid_x, grid_y)
        elif mouse_buttons[2]:
            erase_cell(grid_x, grid_y)

    else:
        simulate()
        pygame.draw.rect(screen, (3, 255, 11), (10, 10, 15, 15))

    print(grid)
    pygame.display.flip()
    clock.tick(20)
