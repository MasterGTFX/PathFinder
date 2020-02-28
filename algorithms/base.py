from abc import abstractmethod


class BaseNode(object):
    def __init__(self, x, y):
        """
        Node object.
        :param int x:   y-coordinate
        :param int y:   x-coordinate
        """
        self.x = x
        self.y = y
        self.traversable = True
        self.parent = None
        self.neighbours = None

    def __repr__(self):
        return "Node({},{})".format(self.x, self.y)


class BaseAlgorithm(object):
    def __init__(self, rows=10, cols=10, start=(0, 0), end=(9, 9), board=False, node_type=BaseNode):
        """
        Creating object that contains board for algorithm. Each element in board is Node
        :param int rows:    Number of rows
        :param int cols:    Number of columns
        :param (int,int) start:   Start node [(x-coordinate, y-coordinate)]
        :param (int,int) end:   End node [(x-coordinate, y-coordinate)]
        :param [[]] board:    (oprtional) 2d Int Array [1-obstacle, 2-start node, 3-end node]
        """
        self.open_nodes = []
        self.closed_nodes = []
        self.path_found = False
        self.alg_end = False

        if board:
            self.BOARD = [[node_type(x, y) for x in range(len(board[0]))] for y in range(len(board))]
            self.board_array = board
            self.len_x = len(self.BOARD[0])
            self.len_y = len(self.BOARD)
            for y in range(len(board)):
                for x in range(len(board[0])):
                    if board[y][x] == 1:
                        self.BOARD[y][x].traversable = False
                    elif board[y][x] == 2:
                        self.start_node = self.BOARD[y][x]
                    elif board[y][x] == 3:
                        self.end_node = self.BOARD[y][x]
                    elif board[y][x] in [4, 5, 6]:
                        self.board_array[y][x] = 0
            if not self.start_node or not self.end_node:
                raise AttributeError("No start/end node specified!")
        else:
            self.BOARD = [[node_type(x, y) for x in range(rows)] for y in range(cols)]

            self.len_x = len(self.BOARD[0])
            self.len_y = len(self.BOARD)
            self.board_array = [[0 for _ in range(self.len_x)] for _ in range(self.len_y)]

            self.start_node = self.BOARD[start[1]][start[0]]
            self.board_array[start[1]][start[0]] = 2

            self.end_node = self.BOARD[end[1]][end[0]]
            self.board_array[end[1]][end[0]] = 3

    abstractmethod

    def algorithm_loop(self):
        """
        Perform one algorithm loop
        """

    def add_obstacle(self, x, y):
        """
        Add obstacle in given (x,y) position
        :return: None
        """
        self.BOARD[y][x].traversable = False
        self.board_array[y][x] = 1

    def remove_obstacle(self, x, y):
        """
        Add obstacle in given (x,y) position
        :return: None
        """
        self.BOARD[y][x].traversable = True
        self.board_array[y][x] = 0

    @abstractmethod
    def move_start_node(self, x, y):
        """
        Move start node to a given (x,y) position
        :return: None
        """

    @abstractmethod
    def move_end_node(self, x, y):
        """
        Move end node to a given (x,y) position
        :return: None
        """

    def move_node(self, x, y, node):
        """
        Move node(start/end only) to a given (x.y) position
        :param x: x-coordinate
        :param y: y-coordinate
        :param node: Node to be moved (start/end)
        :return: None
        """
        if node is self.start_node:
            self.move_start_node(x, y)
        elif node is self.end_node:
            self.move_end_node(x, y)
        else:
            print("WARNING: can move only start/end.\n"
                  "TIP: Use add/remove obstacles to modify board")

    def _set_node_neighbours(self, node):
        """
        Returns node neighbours that are traversable
        :return list of traversable nodes
        """
        all_neighbours = [self.BOARD[node.y + y][node.x + x] for x in reversed(range(-1, 2)) for y in
                          reversed(range(-1, 2))
                          if 0 <= node.x + x < self.len_x and 0 <= node.y + y < self.len_y]
        non_traversable_neighbours = []
        for neighbour in all_neighbours:
            if not neighbour.traversable:
                non_traversable_neighbours.append(neighbour)
            elif neighbour.x != node.x and neighbour.y != node.y:
                x_diff = neighbour.x - node.x
                y_diff = neighbour.y - node.y
                if not self.BOARD[node.y + y_diff][node.x].traversable and \
                        not self.BOARD[node.y][node.x + x_diff].traversable:
                    non_traversable_neighbours.append(neighbour)
        node.neighbours = [neighbour for neighbour in all_neighbours if neighbour not in non_traversable_neighbours]

    def _calc_cost(self, current, destination=None):
        """
        TBC
        :param current:
        :param destination:
        :return:
        """
        if not destination:
            destination = self.end_node
        distance = abs(destination.x - current.x) + abs(destination.y - current.y)
        return distance

    def _backtrack_path(self, current=None):
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
                self.board_array[current.parent.y][current.parent.x] = 4
                current = current.parent
        self.board_array[self.start_node.y][self.start_node.x] = 2
        self.board_array[self.end_node.y][self.end_node.x] = 3
        return path

    def add_obstacle(self, x, y):
        """
        Add obstacle in given (x,y) position
        :return: None
        """
        self.BOARD[y][x].traversable = False
        self.board_array[y][x] = 1
