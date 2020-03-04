from base import BaseNode, BaseAlgorithm


class ANode(BaseNode):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.g_cost = 0  # temp
        self.h_cost = None

    def __repr__(self):
        return "ANode({},{})".format(self.x, self.y)

    def __str__(self):
        return "{}, {}".format(self.g_cost, self.h_cost)

class AStar(BaseAlgorithm):

    def __init__(self, rows=10, cols=10, start=(0, 0), end=(9, 9), board=False, node_type=ANode):
        super().__init__(rows, cols, start, end, board, node_type)
        self.start_node.h_cost = self._calc_cost(self.start_node)
        self.open_nodes.append(self.start_node)

    def algorithm_loop(self):
        """
        Perform one A* algorithm loop.
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
            self.path = self._backtrack_path()
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

    def move_start_node(self, x, y):
        """
        Move start node to a given (x,y) position
        :return: None
        """
        self.board_array[self.start_node.y][self.start_node.x] = 0
        self.board_array[y][x] = 2

        self.open_nodes.remove(self.start_node)
        self.open_nodes.append(self.BOARD[y][x])

        self.start_node = self.BOARD[y][x]
        self.start_node.h_cost = self._calc_cost(self.start_node)

    def move_end_node(self, x, y):
        """
        Move start node to a given (x,y) position
        :return: None
        """
        self.board_array[self.end_node.y][self.end_node.x] = 0
        self.board_array[y][x] = 3

        self.end_node = self.BOARD[y][x]


if __name__ == "__main__":
    a = AStar(board=[[2, 0, 0],
                     [0, 1, 1],
                     [0, 1, 0],
                     [0, 0, 3]])
    while not a.alg_end:
        a.algorithm_loop()
    print(a.board_array)
