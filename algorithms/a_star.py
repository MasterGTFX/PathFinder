import math


class Node(object):
    def __init__(self, y, x):
        """
        Node object.
        :param int y:   x-coordinate
        :param int x:   y-coordinate
        """
        self.y = y
        self.x = x
        self.traversable = True
        self.g_cost = 0  # temp
        self.h_cost = None
        self.parent = None

    def __repr__(self):
        return "Node({},{})".format(self.x, self.y)


class AStarAlgorithm(object):
    def __init__(self, rows=10, cols=10, start=(0, 0), end=(9, 9), array_board=False):
        """
        Creating object that contains board for algorithm. Each element in board is Node
        :param int rows:    Number of rows
        :param int cols:    Number of columns
        :param (int,int) start:   Start node [(x-coordinate, y-coordinate)]
        :param (int,int) end:   End node [(x-coordinate, y-coordinate)]
        :param [[]] array_board:    (oprtional) 2d Int Array [1-obstacle, 2-start node, 3-end node]
        """
        self.open_nodes = []
        self.closed_nodes = []
        self.path_found = False
        self.alg_end = False
        if array_board:
            self.BOARD = [[Node(y, x) for x in range(len(array_board[0]))] for y in range(len(array_board))]
            for y in range(len(array_board)):
                for x in range(len(array_board[0])):
                    if array_board[y][x] == 1:
                        self.BOARD[y][x].traversable = False
                    elif array_board[y][x] == 2:
                        self.start_node = self.BOARD[y][x]
                    elif array_board[y][x] == 3:
                        self.end_node = self.BOARD[y][x]
            if not self.start_node or not self.end_node:
                raise AttributeError("No start/end node specified!")
        else:
            self.BOARD = [[Node(y, x) for x in range(rows)] for y in range(cols)]
            self.start_node = self.BOARD[start[1]][start[0]]
            self.end_node = self.BOARD[end[1]][end[0]]

        self.start_node.h_cost = self.calc_cost(self.start_node)
        self.open_nodes.append(self.start_node)

    def calc_cost(self, current, destination=None):
        """
        TBC
        :param current:
        :param destination:
        :return:
        """
        if not destination:
            destination = self.end_node
        distance = math.sqrt((destination.x - current.x) ** 2 + (destination.y - current.y) ** 2)
        return distance

    def algorithm_loop(self):
        """
        Perform one A* algorithm loop
        :return: None
        """
        if self.path_found or not self.open_nodes:
            self.alg_end = True
            return None
        self.open_nodes.sort(key=lambda t: t.h_cost)
        current = min(self.open_nodes, key=lambda t: t.g_cost + t.h_cost)

        self.open_nodes.remove(current)
        self.closed_nodes.append(current)

        if current == self.end_node:
            self.path_found = True
            self.alg_end = True

        for neighbour in [self.BOARD[current.y + y][current.x + x] for x in reversed(range(-1, 2)) for y in
                          reversed(range(-1, 2))
                          if 0 <= current.x + x < len(self.BOARD[0]) and 0 <= current.y + y < len(self.BOARD)]:

            if not neighbour.traversable or neighbour in self.closed_nodes:
                continue

            if neighbour not in self.open_nodes or self.calc_cost(neighbour, current) + current.g_cost < neighbour.g_cost:
                neighbour.g_cost = self.calc_cost(neighbour, current) + current.g_cost
                if not neighbour.h_cost:
                    neighbour.h_cost = self.calc_cost(neighbour)
                neighbour.parent = current
                if neighbour not in self.open_nodes:
                    self.open_nodes.append(neighbour)

    def backtrack_path(self, current=None):
        """
        Backtrack node (based on their parent value)
        :param current: (optional) backtrack from specific node
        :return: list
        """
        path = []
        if self.path_found:
            if not current:
                current = self.end_node
                path.append(self.end_node)
            while current.parent:
                path.append(current.parent)
                current = current.parent
        return path

    def board_to_2d_list(self, print_board=False):
        """
        Convert board to 2d array, where 0-not used Node, 1-Obstacle, 2-Start Node, 3-End Node, 4-Node in path
        :param print_board:
        :return:
        """
        cols = len(self.BOARD)
        rows = len(self.BOARD[0])
        if self.path_found:
            path = self.backtrack_path()
        board_list = [[0 for _ in range(rows)] for _ in range(cols)]
        for x in range(rows):
            for y in range(cols):
                current_node = self.BOARD[y][x]
                if not current_node.traversable:
                    board_list[y][x] = 1
                elif current_node is self.start_node:
                    board_list[y][x] = 2
                elif current_node is self.end_node:
                    board_list[y][x] = 3
                elif self.path_found and current_node in path:
                    board_list[y][x] = 4
        if print_board:
            for x in board_list:
                print(*x, sep='')
        return board_list

    def add_obstacles(self, x, y):
        self.BOARD[x][y].traversable = False


if __name__ == "__main__":
    a = AStarAlgorithm(array_board=[[2, 0, 0],
                                    [0, 1, 1],
                                    [0, 1, 0],
                                    [0, 0, 3]])
    while not a.alg_end:
        a.algorithm_loop()
    a.board_to_2d_list(print_board=True)
