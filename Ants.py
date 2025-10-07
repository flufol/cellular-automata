import pygame
import sys
import colorsys

BACKGROUND_COLOR = (255, 255, 255)
GRID_COLOR = (0, 0, 0)
CELL_COLOR = ()
ANT_COLOR = (0, 255, 0)

MIN_ZOOM = 0.2
MAX_ZOOM = 5.0

DIRECTIONS = [
  (0, -1),   # 0 = up
  (1,  0),   # 1 = right
  (0,  1),   # 2 = down
  (-1, 0),   # 3 = left
]

canvas_width, canvas_height = 1200, 1200
pixel_width = 100

camera_offset = [0.0, 0.0]
zoom = 1.0
panning = False
last_mouse_pos = (0, 0)

cell_size = 30

generation = 0

grid: dict[tuple[int, int]: int] = {}
ant: tuple[int, int] = (0, 0)
ant_direction = 0

rule = "RL"
rule_len = 0

simulate_ant = False
simulation_speed = 10

pygame.init()
screen = pygame.display.set_mode((canvas_width, canvas_height))
pygame.display.set_caption("Ants")
clock = pygame.time.Clock()

font = pygame.font.SysFont('Consolas', 24)
text_color = (0, 0, 0)
margin = 10


def generate_state_colors(rule_string):
    n = len(rule_string)
    colors = []
    for i in range(n):
        h = i / n
        r, g, b = colorsys.hsv_to_rgb(h, 1.0, 1.0)
        colors.append((int(r*255), int(g*255), int(b*255)))
    return colors

colors = generate_state_colors(rule)

def draw_cells():
    scaled_size = cell_size * zoom
    scaled_size = int(round(scaled_size))

    for pos in grid:
        x, y = pos[0], pos[1]
        wx, wy = x * cell_size, y * cell_size
        sx = (wx * zoom) - camera_offset[0]
        sy = (wy * zoom) - camera_offset[1]

        pygame.draw.rect(screen, colors[grid.get(pos)], (round(sx), round(sy), scaled_size, scaled_size))

    wx, wy = ant[0] * cell_size, ant[1] * cell_size
    sx = (wx * zoom) - camera_offset[0]
    sy = (wy * zoom) - camera_offset[1]
    pygame.draw.rect(screen, ANT_COLOR, (round(sx), round(sy), scaled_size, scaled_size))


def draw_grid():
    scaled_size = cell_size * zoom

    x_start = - (camera_offset[0] % scaled_size)
    y_start = - (camera_offset[1] % scaled_size)

    x = x_start
    while x < canvas_width:
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, canvas_height))
        x += scaled_size

    y = y_start
    while y < canvas_height:
        pygame.draw.line(screen, GRID_COLOR, (0, y), (canvas_width, y))
        y += scaled_size


def simulate():
    global grid, ant, rule, generation, ant_direction, rule_len

    state = grid.get(ant, 0)
    turn_direction = rule[state]

    if turn_direction == 'R':
        ant_direction = (ant_direction + 1) % 4
    elif turn_direction == "L":
        ant_direction = (ant_direction - 1) % 4

    grid[ant] = (state + 1) % rule_len

    x, y = ant[0], ant[1]
    x += DIRECTIONS[ant_direction][0]
    y += DIRECTIONS[ant_direction][1]
    ant = (x, y)

    generation += 1


def render_text():
    text_gen = font.render(f"Gen: {generation}", True, text_color)
    text_gen_rect = text_gen.get_rect()
    text_gen_rect.topright = (canvas_width - margin, margin)

    text_rule = font.render(f"Rule: {rule}", True, text_color)
    text_rule_rect = text_rule.get_rect()
    text_rule_rect.topleft = (margin, margin)

    text_speed = font.render(f"speed: {simulation_speed}", True, text_color)
    text_speed_rect = text_speed.get_rect()
    text_speed_rect.midtop = (canvas_width // 2, margin)
    screen.blit(text_gen, text_gen_rect)
    screen.blit(text_rule, text_rule_rect)
    screen.blit(text_speed, text_speed_rect)


def start():
    global grid, colors, rule, generation, ant_direction, simulate_ant, running, ant, rule_len

    running = False
    ant = (0, 0)
    grid.clear()
    rule = input("What is the rule: ").upper()
    rule_len = len(rule)
    colors = generate_state_colors(rule)
    generation = 0
    ant_direction = 0
    simulate_ant = True
    running = True


if __name__ == "__main__":
    start()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEWHEEL:
                mx, my = pygame.mouse.get_pos()

                wx = (mx + camera_offset[0]) / zoom
                wy = (my + camera_offset[1]) / zoom

                zoom *= 1.0 + event.y * 0.1
                zoom = max(MIN_ZOOM, min(MAX_ZOOM, zoom))

                camera_offset[0] = wx * zoom - mx
                camera_offset[1] = wy * zoom - my

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
                panning = True
                last_mouse_pos = event.pos

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 2:
                panning = False

            elif event.type == pygame.MOUSEMOTION and panning:
                dx = event.pos[0] - last_mouse_pos[0]
                dy = event.pos[1] - last_mouse_pos[1]
                camera_offset[0] -= dx
                camera_offset[1] -= dy
                last_mouse_pos = event.pos

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    simulation_speed += 1
                elif event.key == pygame.K_DOWN and simulation_speed > 1:
                    simulation_speed -= 1
                elif event.key == pygame.K_RIGHT and simulate_ant == False:
                    simulate()
                elif event.key == pygame.K_SPACE:
                    simulate_ant = not simulate_ant

                elif event.key == pygame.K_BACKSPACE:
                    start()

        if simulate_ant:
            for i in range(simulation_speed):
                simulate()

        screen.fill(BACKGROUND_COLOR)
        draw_cells()
        draw_grid()

        render_text()

        pygame.display.flip()
        clock.tick(60)

pygame.quit()
sys.exit()
