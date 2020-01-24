import pygame
from a_star_algorithm import AStarAlgorithm

RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

WIDTH = 900
HEIGHT = 900
MARGIN = 5


class Board(object):
    def __init__(self, screen, a_star):
        self.size = ((WIDTH - len(a_star.BOARD[0]) * MARGIN) // len(a_star.BOARD[0]),
                     (HEIGHT - len(a_star.BOARD) * MARGIN) // len(a_star.BOARD))
        self.a_star = a_star
        self.screen = screen
        for row in self.a_star.BOARD:
            for node in row:
                pygame.draw.rect(screen, WHITE, [(MARGIN + self.size[0]) * node.x + MARGIN,
                                                 (MARGIN + self.size[1]) * node.y + MARGIN,
                                                 self.size[0],
                                                 self.size[1]])

        pygame.draw.rect(screen, BLUE, [(MARGIN + self.size[0]) * self.a_star.end_node.x + MARGIN,
                                        (MARGIN + self.size[1]) * self.a_star.end_node.y + MARGIN,
                                        self.size[0],
                                        self.size[1]])
        pygame.draw.rect(screen, BLUE, [(MARGIN + self.size[0]) * self.a_star.start_node.x + MARGIN,
                                        (MARGIN + self.size[1]) * self.a_star.start_node.y + MARGIN,
                                        self.size[0],
                                        self.size[1]])

    def update(self):
        for node in self.a_star.open_nodes:
            pygame.draw.rect(screen, GREEN, [(MARGIN + self.size[0]) * node.x + MARGIN,
                                             (MARGIN + self.size[1]) * node.y + MARGIN,
                                             self.size[0],
                                             self.size[1]])
        for node in self.a_star.closed_nodes:
            pygame.draw.rect(screen, RED, [(MARGIN + self.size[0]) * node.x + MARGIN,
                                           (MARGIN + self.size[1]) * node.y + MARGIN,
                                           self.size[0],
                                           self.size[1]])

    def print_obstacle(self, pos):
        x, y = (pos[1] * len(self.a_star.BOARD[0]) // WIDTH,
                pos[0] * len(self.a_star.BOARD) // HEIGHT)
        self.a_star.add_obstacles(x, y)
        pygame.draw.rect(screen, BLACK, [(MARGIN + self.size[0]) * y + MARGIN,
                                         (MARGIN + self.size[1]) * x + MARGIN,
                                         self.size[0],
                                         self.size[1]])

    def print_path(self):
        path = self.a_star.backtrack_path()
        for node in path:
            pygame.draw.rect(screen, BLUE, [(MARGIN + self.size[0]) * node.x + MARGIN,
                                            (MARGIN + self.size[1]) * node.y + MARGIN,
                                            self.size[0],
                                            self.size[1]])


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    pygame.display.set_caption("AStart Algorithm")
    clock = pygame.time.Clock()

    a_star = AStarAlgorithm(50, 50, start=(10, 0), end=(14, 30))
    board = Board(screen, a_star)

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
                board.print_obstacle(pos)
        if start_algorithm and not a_star.path_found:
            a_star.algorithm_loop()
            board.update()
            if a_star.path_found:
                board.print_path()
        pygame.display.flip()
        clock.tick(60)
