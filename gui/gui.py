import pygame
from algorithms import AStar, Dijkstra

pygame.init()

DARK_RED = (139, 0, 0)
MEDIUM_BLUE = (0, 0, 205)
FOREST_GREEN = (34, 139, 34)
BLACK = (0, 0, 0)
GRAY = (105, 105, 105)
LIGHT_GRAY = (211,211,211)
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
BUTTON_MARGIN = 5

FONT = pygame.font.SysFont("comicsansms", int(min([WIDTH, HEIGHT]) / 50))
TEXT_ON_NODES = True
RUNNING = True


class Board:
    start_algorithm = False
    moving_pos = [None, None]
    moving_node = False

    def __init__(self, screen, alg=AStar()):
        self.alg = alg
        self.board_size = (len(self.alg.board_array[0]), len(self.alg.board_array))
        self.size = ((WIDTH - self.board_size[0] * NODE_MARGIN) // self.board_size[0],
                     (BOARD_HEIGHT - self.board_size[1] * NODE_MARGIN) // self.board_size[1])
        self.start_node = (0, 0)
        self.end_node = (board_size[0] - 1, board_size[1] - 1)
        self.screen = screen

        self.update_all()

    def draw_node(self, x, y, color):
        if color == WHITE:
            if x % 2 == 0 and y % 2 == 0:
                color = WHITE_SMOKE

        node_rect = pygame.draw.rect(screen, color, [(NODE_MARGIN + self.size[0]) * x + NODE_MARGIN,
                                                     (NODE_MARGIN + self.size[1]) * y + NODE_MARGIN + BOARD_MARGIN,
                                                     self.size[0],
                                                     self.size[1]])

        if TEXT_ON_NODES:
            node_text_rect = self._get_node_text(x, y, color, node_rect)
            pygame.display.update([node_rect, node_text_rect])
        else:
            pygame.display.update(node_rect)

    def update_all(self):
        for y in range(len(self.alg.board_array)):
            for x in range(len(self.alg.board_array[0])):
                if self.alg.BOARD[y][x] not in [self.alg.start_node, self.alg.end_node]:
                    color = COLORS[self.alg.board_array[y][x]]
                    self.draw_node(x, y, color)
                elif self.alg.BOARD[y][x] == self.alg.start_node:
                    self.draw_node(x, y, GOLD)
                else:
                    self.draw_node(x, y, ORANGE)

    def add_obstacle(self, pos):
        x, y = self._convert_mouse_pos_to_cords(pos)
        if self.alg.BOARD[y][x] not in [self.alg.start_node, self.alg.end_node]:
            self.alg.add_obstacle(x, y)
            self.update_all()

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

    def _get_node_text(self, x, y, color, node_rect):
        node_text_rect = None
        if color in [FOREST_GREEN, DARK_RED, MEDIUM_BLUE]:
            # node_text = f"{self.alg.BOARD[y][x].g_cost}, {self.alg.BOARD[y][x].h_cost}"
            node_text = str(self.alg.BOARD[y][x])
            text_surface = FONT.render(node_text, True, BLACK)
            node_text_rect = screen.blit(text_surface,
                                         (node_rect.centerx - text_surface.get_width() // 2,
                                          node_rect.centery - text_surface.get_height() // 2))

        elif color is GOLD:
            text_surface = FONT.render("START", True, BLACK)
            node_text_rect = screen.blit(text_surface,
                                         (node_rect.centerx - text_surface.get_width() // 2,
                                          node_rect.centery - text_surface.get_height() // 2))
        elif color is ORANGE:
            text_surface = FONT.render("END", True, BLACK)
            node_text_rect = screen.blit(text_surface,
                                         (node_rect.centerx - text_surface.get_width() // 2,
                                          node_rect.centery - text_surface.get_height() // 2))
        return node_text_rect

    def _convert_mouse_pos_to_cords(self, pos):
        x, y = (pos[0] * len(self.alg.board_array[0]) // WIDTH,
                (pos[1] - BOARD_MARGIN) * len(self.alg.board_array) // BOARD_HEIGHT)
        return x, y

    def __call__(self, **kwargs):
        for event in kwargs.get('events'):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.start_algorithm = True
                    if self.alg.path_found:
                        self.alg = Algorithm(board=self.alg.board_array)

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        if mouse_pos[1] >= BOARD_MARGIN:
            if mouse_click[0]:
                self.add_obstacle(mouse_pos)
            if mouse_click[2]:
                self.remove_obstacle(mouse_pos)
            if mouse_click[1]:
                if not self.moving_node:
                    self.moving_pos[0] = mouse_pos
                    self.moving_node = True

            elif self.moving_node:
                self.moving_pos[1] = mouse_pos
                if self.alg.path_found:
                    self.alg = Algorithm(board=self.alg.board_array)
                self.move_start_or_end_node(self.moving_pos[0], self.moving_pos[1])
                self.moving_pos = [None, None]
                self.moving_node = False
                self.update_all()

        if self.start_algorithm and not self.alg.path_found:
            self.alg.algorithm_loop()
            self.update_all()

    def _reset(self):
        pass


class Menu:
    def __init__(self, screen):
        self.bkg = pygame.draw.rect(screen, LIGHT_GRAY, [0, 0, WIDTH, BOARD_MARGIN])
        self.start_btn = pygame.draw.rect(screen, DARK_RED,
                                          [BUTTON_MARGIN, BUTTON_MARGIN,
                                           int(WIDTH / 10) - BUTTON_MARGIN * 2, BOARD_MARGIN - BUTTON_MARGIN * 2])
        self.end_btn = pygame.draw.rect(screen, GRAY,
                                        [BUTTON_MARGIN + int(WIDTH / 2), BUTTON_MARGIN,
                                         int(WIDTH / 10) - BUTTON_MARGIN * 2, BOARD_MARGIN - BUTTON_MARGIN * 2])

        pygame.display.update([self.bkg, self.start_btn, self.end_btn])

    def __call__(self, events, **kwargs):
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[1] < BOARD_MARGIN:
            mouse_click = pygame.mouse.get_pressed()
            if mouse_click[0]:
                if self.start_btn.collidepoint(mouse_pos):
                    print("START")


def resize(event, board):
    # TBC
    global WIDTH, HEIGHT, BOARD_HEIGHT, BOARD_MARGIN, FONT
    WIDTH = event.w
    HEIGHT = event.h
    BOARD_HEIGHT = int(0.95 * HEIGHT)
    BOARD_MARGIN = HEIGHT - BOARD_HEIGHT
    FONT = pygame.font.SysFont("comicsansms", int(min([WIDTH, HEIGHT]) / 50))

    board.size = (
        (WIDTH - board.board_size[0] * NODE_MARGIN) // board.board_size[0],
        (BOARD_HEIGHT - board.board_size[1] * NODE_MARGIN) // board.board_size[
            1])
    board.screen = pygame.display.set_mode(event.dict['size'], pygame.RESIZABLE)

    screen_bkg = screen.fill(BLACK)
    pygame.display.update(screen_bkg)

    board.update_all()


if __name__ == "__main__":
    screen = pygame.display.set_mode([WIDTH, HEIGHT], pygame.RESIZABLE)
    pygame.display.set_caption("AStart Algorithm")
    screen_bkg = screen.fill(BLACK)
    pygame.display.update(screen_bkg)

    # Algorithm = AStar
    Algorithm = Dijkstra

    board_size = (10, 10)
    alg = Algorithm(board_size[0], board_size[1], start=(0, 0), end=(board_size[0] - 1, board_size[1] - 1))

    board = Board(screen, alg)
    menu = Menu(screen)

    clock = pygame.time.Clock()

    while RUNNING:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                RUNNING = False
            elif event.type == pygame.VIDEORESIZE:
                resize(event, board)
                menu = Menu(screen)

        menu(events=events)
        board(events=events)

        clock.tick(60)
