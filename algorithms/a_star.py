class Node(object):
    def __init__(self, x, y):
        """
        Node object.
        :param int x:   y-coordinate
        :param int y:   x-coordinate
        """
        self.x = x
        self.y = y
        self.traversable = True
        self.g_cost = 0  # temp
        self.h_cost = None
        self.parent = None
        self.neighbours = None

    def __repr__(self):
        return "Node({},{})".format(self.x, self.y)


class AStar(object):
    def __init__(self, rows=10, cols=10, start=(0, 0), end=(9, 9), board=False):
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
            self.BOARD = [[Node(x, y) for x in range(len(board[0]))] for y in range(len(board))]
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
            if not self.start_node or not self.end_node:
                raise AttributeError("No start/end node specified!")
        else:
            self.BOARD = [[Node(x, y) for x in range(rows)] for y in range(cols)]

            self.len_x = len(self.BOARD[0])
            self.len_y = len(self.BOARD)
            self.board_array = [[0 for _ in range(self.len_x)] for _ in range(self.len_y)]

            self.start_node = self.BOARD[start[1]][start[0]]
            self.board_array[start[1]][start[0]] = 2

            self.end_node = self.BOARD[end[1]][end[0]]
            self.board_array[end[1]][end[0]] = 3

        self.start_node.h_cost = self._calc_cost(self.start_node)
        self.open_nodes.append(self.start_node)

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

    def algorithm_loop(self):
        """
        Perform one A* algorithm loop
        :return: None
        """
        if self.path_found or not self.open_nodes:
            self.path = self.backtrack_path()
            self.alg_end = True
            return None

        self.open_nodes.sort(key=lambda t: t.h_cost)
        current = min(self.open_nodes, key=lambda t: t.g_cost + t.h_cost)

        self.open_nodes.remove(current)
        self.closed_nodes.append(current)

        if current == self.end_node:
            self.path_found = True
            self.path = self.backtrack_path()
            self.alg_end = True
            return None

        self.board_array[current.y][current.x] = 6
        if not current.neighbours:
            self._set_node_neighbours(current)

        for neighbour in current.neighbours:

            if not neighbour.traversable or neighbour in self.closed_nodes:
                continue

            if neighbour not in self.open_nodes or self._calc_cost(neighbour,
                                                                   current) + current.g_cost < neighbour.g_cost:
                neighbour.g_cost = self._calc_cost(neighbour, current) + current.g_cost
                if not neighbour.h_cost:
                    neighbour.h_cost = self._calc_cost(neighbour)
                neighbour.parent = current
                if neighbour not in self.open_nodes:
                    self.open_nodes.append(neighbour)
                    self.board_array[neighbour.y][neighbour.x] = 5

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
                self.board_array[current.parent.y][current.parent.x] = 4
                current = current.parent
        self.board_array[self.start_node.y][self.start_node.x] = 2
        self.board_array[self.end_node.y][self.end_node.x] = 3
        return path

    def add_obstacles(self, x, y):
        """
        Add obstacle in given (x,y) position
        :return: None
        """
        self.BOARD[y][x].traversable = False
        self.board_array[y][x] = 1


if __name__ == "__main__":
    a = AStar(board=[[2, 0, 0],
                     [0, 1, 1],
                     [0, 1, 0],
                     [0, 0, 3]])
    while not a.alg_end:
        a.algorithm_loop()
    print(a.board_array)
