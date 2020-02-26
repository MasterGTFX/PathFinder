import pygame
from algorithms import AStar

RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

WIDTH = 900
HEIGHT = 900
MARGIN = 5


class BoardObject(object):

    def __init__(self, screen, alg=AStar()):
        self.alg = alg
        self.board = alg.board_array
        self.board_size = (len(self.board[0]), len(self.board))
        self.size = ((WIDTH - self.board_size[0] * MARGIN) // self.board_size[0],
                     (HEIGHT - self.board_size[1] * MARGIN) // self.board_size[1])
        self.start_node = (0, 0)
        self.end_node = (board_size[0] - 1, board_size[1] - 1)
        self.screen = screen

        for x in range(len(self.board)):
            for y in range(len(self.board[0])):
                self.draw_rect(x, y, WHITE)
        self.draw_rect(self.start_node[0], self.start_node[1], BLUE)
        self.draw_rect(self.end_node[0], self.end_node[1], BLUE)

    def draw_rect(self, x, y, color):
        pygame.draw.rect(screen, color, [(MARGIN + self.size[0]) * x + MARGIN,
                                         (MARGIN + self.size[1]) * y + MARGIN,
                                         self.size[0],
                                         self.size[1]])

    def update(self):
        for x in range(len(self.board)):
            for y in range(len(self.board)):
                if self.board[y][x] == 0:
                    color = WHITE
                if self.board[y][x] == 1:
                    color = BLACK
                if self.board[y][x] in [2, 3, 4]:
                    color = BLUE
                if self.board[y][x] == 5:
                    color = GREEN
                if self.board[y][x] == 6:
                    color = RED
                self.draw_rect(x, y, color)

    def add_obstacle(self, pos):
        y, x = (pos[1] * len(self.board[0]) // WIDTH,
                pos[0] * len(self.board) // HEIGHT)
        self.alg.add_obstacles(x, y)
        pygame.draw.rect(screen, BLACK, [(MARGIN + self.size[0]) * x + MARGIN,
                                         (MARGIN + self.size[1]) * y + MARGIN,
                                         self.size[0],
                                         self.size[1]])
        return x, y


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    pygame.display.set_caption("AStart Algorithm")
    clock = pygame.time.Clock()

    board_size = (20, 20)
    Algorithm = AStar
    alg = Algorithm(board_size[0], board_size[1], start=(0, 0), end=(board_size[0] - 1, board_size[1] - 1))
    board_object = BoardObject(screen, alg)

    running = True
    start_algorithm = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start_algorithm = True
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                board_object.add_obstacle(pos)
        if start_algorithm and not alg.path_found:
            board_object.alg.algorithm_loop()
            board_object.update()

        pygame.display.flip()
        clock.tick(60)
