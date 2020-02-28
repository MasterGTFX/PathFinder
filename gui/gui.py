import pygame
from algorithms import AStar, Dijkstra

pygame.init()

DARK_RED = (139, 0, 0)
MEDIUM_BLUE = (0, 0, 205)
FOREST_GREEN = (34, 139, 34)
BLACK = (0, 0, 0)
GRAY = (105, 105, 105)
GOLD = (255, 215, 0)
ORANGE = (255, 165, 0)
WHITE = (255, 255, 255)
WHITE_SMOKE = (235, 235, 235)
COLORS = {0: WHITE, 1: GRAY, 2: GOLD, 3: ORANGE, 4: MEDIUM_BLUE, 5: FOREST_GREEN, 6: DARK_RED}

WIDTH = 600
HEIGHT = 666
BOARD_HEIGHT = int(0.90 * HEIGHT)
BOARD_MARGIN = HEIGHT - BOARD_HEIGHT
NODE_MARGIN = 2

FONT = pygame.font.SysFont("comicsansms", int(min([WIDTH, HEIGHT]) / 50))
NODES_TEXT = True


class BoardObject(object):

    def __init__(self, screen, alg=AStar()):
        self.alg = alg
        self.board_size = (len(self.alg.board_array[0]), len(self.alg.board_array))
        self.size = ((WIDTH - self.board_size[0] * NODE_MARGIN) // self.board_size[0],
                     (BOARD_HEIGHT - self.board_size[1] * NODE_MARGIN) // self.board_size[1])
        self.start_node = (0, 0)
        self.end_node = (board_size[0] - 1, board_size[1] - 1)
        self.screen = screen

        self.update()

    def draw_node(self, x, y, color):
        if color == WHITE:
            if x % 2 == 0 and y % 2 == 0:
                color = WHITE_SMOKE

        node = pygame.draw.rect(screen, color, [(NODE_MARGIN + self.size[0]) * x + NODE_MARGIN,
                                                (NODE_MARGIN + self.size[1]) * y + NODE_MARGIN + BOARD_MARGIN,
                                                self.size[0],
                                                self.size[1]])

        if NODES_TEXT:
            if color in [FOREST_GREEN, DARK_RED, MEDIUM_BLUE]:
                # node_text = f"{self.alg.BOARD[y][x].g_cost}, {self.alg.BOARD[y][x].h_cost}"
                # node_text = repr(self.alg.BOARD[y][x])
                node_text = ""
                text_surface = FONT.render(node_text, True, BLACK)
                screen.blit(text_surface,
                            (node.centerx - text_surface.get_width() // 2,
                             node.centery - text_surface.get_height() // 2))
            elif color is GOLD:
                text_surface = FONT.render("START", True, BLACK)
                screen.blit(text_surface,
                            (node.centerx - text_surface.get_width() // 2,
                             node.centery - text_surface.get_height() // 2))
            elif color is ORANGE:
                text_surface = FONT.render("END", True, BLACK)
                screen.blit(text_surface,
                            (node.centerx - text_surface.get_width() // 2,
                             node.centery - text_surface.get_height() // 2))

    def update(self):
        for y in range(len(self.alg.board_array)):
            for x in range(len(self.alg.board_array[0])):
                if self.alg.BOARD[y][x] not in [self.alg.start_node, self.alg.end_node]:
                    color = COLORS[self.alg.board_array[y][x]]
                    self.draw_node(x, y, color)
                elif self.alg.BOARD[y][x] == self.alg.start_node:
                    self.draw_node(x, y, GOLD)
                else:
                    self.draw_node(x, y, ORANGE)

    def _convert_mouse_pos_to_cords(self, pos):
        x, y = (pos[0] * len(self.alg.board_array[0]) // WIDTH,
                (pos[1] - BOARD_MARGIN) * len(self.alg.board_array) // BOARD_HEIGHT)
        return x, y

    def add_obstacle(self, pos):
        x, y = self._convert_mouse_pos_to_cords(pos)
        if self.alg.BOARD[y][x] not in [self.alg.start_node, self.alg.end_node]:
            self.alg.add_obstacle(x, y)
            self.update()

    def remove_obstacle(self, pos):
        x, y = self._convert_mouse_pos_to_cords(pos)
        if self.alg.BOARD[y][x] not in [self.alg.start_node, self.alg.end_node]:
            self.alg.remove_obstacle(x, y)
            self.draw_node(x, y, WHITE)

    def move_start_or_end_node(self, from_pos, to_pos):
        old_x, old_y = self._convert_mouse_pos_to_cords(from_pos)
        old_node = self.alg.BOARD[old_y][old_x]
        new_x, new_y = self._convert_mouse_pos_to_cords(to_pos)
        self.alg.move_node(new_x, new_y, old_node)


class BoardScreen:
    running = True
    start_algorithm = False

    def __init__(self, board_object):
        self.board_object = board_object
        self.clock = pygame.time.Clock()
        self.moving_pos = [None, None]
        self.moving_node = False

    def __call__(self, *args, **kwargs):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.start_algorithm = True
                        if self.board_object.alg.path_found:
                            self.board_object.alg = Algorithm(board=self.board_object.alg.board_array)
                elif event.type == pygame.VIDEORESIZE:
                    # TBC
                    global NODE_MARGIN, WIDTH, HEIGHT, FONT, FONT_MARGIN, BOARD_HEIGHT, BOARD_MARGIN
                    WIDTH = event.w
                    HEIGHT = event.h
                    BOARD_HEIGHT = int(0.95 * HEIGHT)
                    BOARD_MARGIN = HEIGHT - BOARD_HEIGHT
                    FONT = pygame.font.SysFont("comicsansms", int(min([WIDTH, HEIGHT]) / 50))

                    self.board_object.size = (
                        (WIDTH - self.board_object.board_size[0] * NODE_MARGIN) // self.board_object.board_size[0],
                        (BOARD_HEIGHT - self.board_object.board_size[1] * NODE_MARGIN) // self.board_object.board_size[
                            1])
                    self.board_object.screen = pygame.display.set_mode(event.dict['size'], pygame.RESIZABLE)

                    self.board_object.screen.fill(BLACK)
                    self.board_object.update()


            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()
            if mouse_pos[1] >= BOARD_MARGIN:
                if mouse_click[0]:
                    self.board_object.add_obstacle(mouse_pos)
                if mouse_click[2]:
                    self.board_object.remove_obstacle(mouse_pos)
                if mouse_click[1]:
                    if not self.moving_node:
                        self.moving_pos[0] = mouse_pos
                        self.moving_node = True
                        self.board_object.screen.fill(GOLD)
                        self.board_object.update()
                elif self.moving_node:
                    self.moving_pos[1] = mouse_pos
                    if self.board_object.alg.path_found:
                        self.board_object.alg = Algorithm(board=self.board_object.alg.board_array)
                    self.board_object.move_start_or_end_node(self.moving_pos[0], self.moving_pos[1])
                    self.moving_pos = [None, None]
                    self.moving_node = False
                    self.board_object.screen.fill(BLACK)
                    self.board_object.update()

            if self.start_algorithm and not self.board_object.alg.path_found:
                self.board_object.alg.algorithm_loop()
                self.board_object.update()

            pygame.display.flip()
            self.clock.tick(60)

    def _reset(self):
        pass


if __name__ == "__main__":
    screen = pygame.display.set_mode([WIDTH, HEIGHT], pygame.RESIZABLE)
    pygame.display.set_caption("AStart Algorithm")
    # Algorithm = AStar
    Algorithm = Dijkstra

    board_size = (10, 10)
    alg = Algorithm(board_size[0], board_size[1], start=(0, 0), end=(board_size[0] - 1, board_size[1] - 1))

    board_object = BoardObject(screen, alg)
    board_screen = BoardScreen(board_object)

    board_screen()
