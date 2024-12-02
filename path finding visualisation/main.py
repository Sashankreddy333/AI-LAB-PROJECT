import pygame
import button
import tile
from queue import PriorityQueue


LBROWN = (171, 112, 61)
DBROWN = (121, 63, 13)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
YELLOW = (255, 255, 0)


def create_grid(rows, width):
    grid = []
    gap = width // rows
    for x in range(rows):
        grid.append([])
        for y in range(rows):
            current_tile = tile.Tile(x, y, gap, rows)
            grid[x].append(current_tile)
    return grid


def update_grid_neighbors(grid, allow_diagonal):
    for row in grid:
        for square in row:
            square.updateNeighbors(grid, allow_diagonal)


def render_window(win, grid, rows, width, buttons, ui_text):
    win.fill(LBROWN)
    for row in grid:
        for square in row:
            square.draw(win)
    draw_grid_lines(win, rows, width)
    for button in buttons:
        button.draw(win)
    for text in ui_text:
        win.blit(text, (400, 800))
    pygame.display.update()


def draw_grid_lines(win, rows, width):
    gap = width // rows
    for i in range(rows + 1):
        pygame.draw.line(win, DBROWN, (0, i * gap), (width, i * gap), width=2)
    for j in range(rows + 1):
        pygame.draw.line(win, DBROWN, (j * gap, 0), (j * gap, width), width=2)


def get_mouse_position(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col


WIN_WIDTH = 800
WIN = pygame.display.set_mode((WIN_WIDTH + 200, WIN_WIDTH + 50))
pygame.display.set_caption("Algorithm Visualization")

aStarDiagonalButtonImg = pygame.image.load('resources/Diag.png').convert_alpha()
aStarNonDiagonalButtonImg = pygame.image.load('resources/NonDiag.png').convert_alpha()
resetButtonImg = pygame.image.load('resources/reset.png').convert_alpha()
spaceimage = pygame.image.load('resources/space.png').convert_alpha()



def a_star_pathfinding(draw, grid, start, end):
    open_set = PriorityQueue()
    count = 0
    open_set.put((0, count, start))
    came_from = {}

    g_score = {square: float("inf") for row in grid for square in row}
    g_score[start] = 0
    f_score = {square: float("inf") for row in grid for square in row}
    f_score[start] = manhattan_distance(start.getPos(), end.getPos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return None

        current_tile = open_set.get()[2]
        open_set_hash.remove(current_tile)

        if current_tile == end:
            construct_path(came_from, end, draw)
            end.setEnd()
            start.setStart()
            return True

        for neighbor in current_tile.neighbors:
            temp_g_score = g_score[current_tile] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current_tile
                g_score[neighbor] = temp_g_score
                smell_heuristic = neighbor.smell_intensity  
                f_score[neighbor] = temp_g_score + manhattan_distance(neighbor.getPos(), end.getPos()) + smell_heuristic*1.5
                print(f"Tile: ({neighbor.row}, {neighbor.col}) - "
                  f"Manhattan: {manhattan_distance(neighbor.getPos(), end.getPos())}, "
                  f"Smell: {smell_heuristic}, "
                  f"f_score: {f_score[neighbor]}")

                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.setOpen()

        draw()
        if current_tile != start:
            current_tile.setClosed()

    return False


def manhattan_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return abs(x1 - x2) + abs(y1 - y2)


def construct_path(came_from, current_tile, draw):
    while current_tile in came_from:
        current_tile = came_from[current_tile]
        current_tile.setPath()
        draw()


def check_valid_bounds(row, col, total_rows):
    return not (row >= total_rows or row < 0 or col >= total_rows or col < 0)


def reset_search_area(grid):
    for row in grid:
        for square in row:
            if square.color not in [BLUE, PURPLE, BLACK]:
                square.reset()
    return grid


def main(win, width):
    rows = 40
    grid = create_grid(rows, width)

    for row in grid:
        for tile in row:
            tile.initializeAllNeighbors(grid)

    start = None
    end = None
    is_running = True
    rotten_tiles = []

    diagonal_button = button.Button(850, 25, aStarDiagonalButtonImg)
    non_diagonal_button = button.Button(850, 100, aStarNonDiagonalButtonImg)
    reset_button = button.Button(850, 700, resetButtonImg)

    ui_buttons = [diagonal_button, non_diagonal_button, reset_button]
    ui_text = [spaceimage]

    while is_running:
        render_window(win, grid, rows, width, ui_buttons, ui_text)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_mouse_position(pos, rows, width)
                if check_valid_bounds(row, col, rows):
                    current_tile = grid[row][col]
                    if not start and current_tile != end:
                        start = current_tile
                        start.setStart()
                    elif not end and current_tile != start:
                        end = current_tile
                        end.setEnd()
                    elif current_tile != start and current_tile != end:
                        current_tile.setWall()

                elif diagonal_button.isActivated() and start and end:
                    update_grid_neighbors(grid, True)
                    a_star_pathfinding(lambda: render_window(win, grid, rows, width, ui_buttons, ui_text), grid, start, end)

                elif non_diagonal_button.isActivated() and start and end:
                    update_grid_neighbors(grid, False)
                    a_star_pathfinding(lambda: render_window(win, grid, rows, width, ui_buttons, ui_text), grid, start, end)

                elif reset_button.isActivated():
                    grid = create_grid(rows, width)
                    start = None
                    end = None
                    for row in grid:
                        for tile in row:
                            tile.initializeAllNeighbors(grid)
                    rotten_tiles.clear()


            
            if pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_mouse_position(pos, rows, width)
                if check_valid_bounds(row, col, rows):
                    current_tile = grid[row][col]
                    current_tile.reset()
                    if current_tile == start:
                        start = None
                    elif current_tile == end:
                        end = None

            
            if pygame.mouse.get_pressed()[1]:
                pos = pygame.mouse.get_pos()
                row, col = get_mouse_position(pos, rows, width)
                if check_valid_bounds(row, col, rows):
                    current_tile = grid[row][col]
                    if current_tile not in rotten_tiles and not current_tile.isWall() and not current_tile.isStart() and not current_tile.isEnd():
                        current_tile.setRotten()
                        rotten_tiles.append(current_tile)
                        current_tile.propagateSmell(grid)

    pygame.quit()

main(WIN, WIN_WIDTH)