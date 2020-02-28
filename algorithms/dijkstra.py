from base import BaseNode, BaseAlgorithm
from itertools import chain
from sys import maxsize


class DijkstraNode(BaseNode):

    def __init__(self, x, y):
        super().__init__(x, y)
        self.d = maxsize


class Dijkstra(BaseAlgorithm):

    def __init__(self, rows=10, cols=10, start=(0, 0), end=(9, 9), board=False, node_type=DijkstraNode):
        super().__init__(rows, cols, start, end, board, node_type)
        self.start_node.d = 0
        self.open_nodes = list(chain.from_iterable([node for node in row if node.traversable] for row in self.BOARD))

    def algorithm_loop(self):
        """
        Perform one Dijkstra algorithm loop.
        :return: None
        """
        if not self.open_nodes:
            self.alg_end = True
            return None

        current = min(self.open_nodes, key=lambda node: node.d)
        self.board_array[current.y][current.x] = 6

        self.open_nodes.remove(current)
        self.closed_nodes.append(current)

        if current == self.end_node:
            self.path_found = True
            self.path = self._backtrack_path()
            self.alg_end = True

        if not current.neighbours:
            self._set_node_neighbours(current)

        for neighbour in current.neighbours:
            if neighbour.d > current.d + self._calc_cost(current, neighbour):
                neighbour.d = current.d + self._calc_cost(current, neighbour)
                neighbour.parent = current
                self.board_array[current.y][current.x] = 5


if __name__ == "__main__":
    alg = Dijkstra(100, 100, start=(0, 0), end=(99, 99))

    a = Dijkstra(board=[[2, 0, 0],
                        [0, 1, 1],
                        [0, 1, 0],
                        [0, 0, 3]])
    while not alg.alg_end:
        alg.algorithm_loop()
    print(alg.board_array)
