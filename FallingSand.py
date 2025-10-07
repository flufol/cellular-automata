import pygame
import random

dark_background = (2, 1, 10)
dark_colors = [(4, 5, 46), (20, 1, 82) , (34, 0, 124)]
dark_weights = [9, 0.5, 0.5]
light_background = (241, 247, 237)
light_colors = [(241, 145, 67), (255, 119, 61) , (245, 85, 54)]
light_weights = [2, 2, 7]

dark_mode = False

canvas_width, canvas_height = 1000, 1000
pixel_width = 10

pygame.init()
screen = pygame.display.set_mode((canvas_width, canvas_height))
pygame.display.set_caption("Sand Sim")
clock = pygame.time.Clock()

cols = int(canvas_height / pixel_width)
rows = int(canvas_width / pixel_width)
grid = [[0 for i in range(cols)] for j in range(rows)]
velocity_grid = [[0.0 for i in range(cols)] for j in range(rows)]

gravity = 0.1


def get_random_color():
    return random.choices(dark_colors, dark_weights)[0] if dark_mode else random.choices(light_colors, light_weights)[0]


def get_background_color():
    return dark_background if dark_mode else light_background


def switch_color_mode():
    global dark_mode, grid
    dark_mode = not dark_mode
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] != 0:
                grid[i][j] = get_random_color()


def draw_grid():
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] != 0:
                x = i * pixel_width
                y = j * pixel_width
                pygame.draw.rect(screen, grid[i][j], (x, y, pixel_width, pixel_width)) # Draw the a square to the cell


def update_grid():
    next_grid = [[0 for i in range(cols)] for j in range(rows)]
    next_velocity_grid = [[0.0 for i in range(cols)] for j in range(rows)]
    visited = [[False for _ in range(cols)] for _ in range(rows)]

    global grid, velocity_grid
    for j in range(cols):
        for i in range(rows):
            state = grid[i][j]
            velocity = velocity_grid[i][j]
            has_moved = False
            if state != 0:
                direction = random.choice([-1, 1])
                below_state, below_right_state, below_leftt_state = None, None, None
                new_position = int(j + velocity)
                for y in range(new_position, j, -1):

                    if y < cols:
                        below_state = grid[i][y]

                        if i + direction >= 0 and i + direction <= rows - 1:
                            below_right_state = grid[i + direction][y]
                        elif i - direction >= 0 and i - direction <= rows - 1:
                            below_leftt_state = grid[i - direction][y]

                    if below_state == 0 and not visited[i][y]:
                        next_grid[i][y] = state
                        next_velocity_grid[i][y] = velocity + gravity
                        visited[i][y] = True
                        has_moved = True
                        break
                    elif below_right_state == 0 and not visited[i + direction][y]:
                        next_grid[i + direction][y] = state
                        next_velocity_grid[i + direction][y] = velocity + gravity
                        visited[i + direction][y] = True
                        has_moved = True
                        break
                    elif below_leftt_state == 0 and not visited[i - direction][y]:
                        next_grid[i - direction][y] = state
                        next_velocity_grid[i - direction][y] = velocity + gravity
                        visited[i - direction][y] = True
                        has_moved = True
                        break
            if state != 0 and not has_moved:
                next_grid[i][j] = state
                next_velocity_grid[i][j] = velocity + gravity
                visited[i][j] = True


    grid = next_grid
    velocity_grid = next_velocity_grid


def draw_cell(row, col):
    random_col = get_random_color()
    grid[row][col] = random_col
    velocity_grid[row][col] = 1


def draw_chunk(row, col, size):
    length = size // 2
    for i in range(-length, length):
        for j in range(-length, length):
            draw_cell(row + i, col + j)


def erase_cell(row, col):
    grid[row][col] = 0


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                switch_color_mode()

    mouse_buttons = pygame.mouse.get_pressed()
    if mouse_buttons[0]:
        x, y = pygame.mouse.get_pos()
        row, col = x // pixel_width, y // pixel_width
        draw_cell(row, col)
    elif mouse_buttons[2]:
        x, y = pygame.mouse.get_pos()
        row, col = x // pixel_width, y // pixel_width
        draw_chunk(row, col, 10)

    screen.fill(get_background_color())

    draw_grid()
    update_grid()

    pygame.display.flip()
    clock.tick(30)
