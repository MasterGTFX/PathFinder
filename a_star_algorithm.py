import math


class Node(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.traversable = True
        self.g_cost = 999999999999999  # temp
        self.h_cost = None
        self.parent = None

    def __repr__(self):
        return "Node({},{})".format(self.x, self.y)


class AStar(object):
    def __init__(self, width=10, length=10, start=(0, 0), end=(9, 9)):
        self.BOARD = [[Node(x, y) for y in range(width)] for x in range(length)]
        self.open_nodes = []
        self.closed_nodes = []
        self.start_node = self.BOARD[start[0]][start[1]]
        self.end_node = self.BOARD[end[0]][end[1]]

        self.start_node.h_cost = self.calc_cost(self.start_node)
        self.open_nodes.append(self.start_node)

        self.path_found = False

    def calc_cost(self, current, destination=None):
        if not destination:
            destination = self.end_node
        distance = math.sqrt((destination.x - current.x) ** 2 + (destination.y - current.y) ** 2)
        return distance

    def algorithm_loop(self):
        if self.path_found:
            return None

        self.open_nodes.sort(key=lambda t: t.h_cost)
        current = min(self.open_nodes, key=lambda t: t.g_cost + t.h_cost)

        self.open_nodes.remove(current)
        self.closed_nodes.append(current)

        if current == self.end_node:
            self.path_found = True
        for neighbour in [self.BOARD[current.x + x][current.y + y]
                          for x in reversed(range(-1, 2)) if 0 <= current.x + x < len(self.BOARD[0])
                          for y in reversed(range(-1, 2)) if 0 <= current.y + y < len(self.BOARD)]:
            if not neighbour.traversable or neighbour in self.closed_nodes:
                continue

            if neighbour not in self.open_nodes or self.calc_cost(neighbour, current) < neighbour.g_cost:
                neighbour.g_cost = self.calc_cost(neighbour, current)
                if not neighbour.h_cost:
                    neighbour.h_cost = self.calc_cost(neighbour)
                neighbour.parent = current
                if neighbour not in self.open_nodes:
                    self.open_nodes.append(neighbour)

    def backtrack_path(self, current=None):
        path = []
        if self.path_found:
            if not current:
                current = self.end_node
            while current.parent:
                path.append(current.parent)
                current = current.parent
        return path

    def print_board(self):
        for row in self.BOARD:
            for node in row:
                if not node.traversable:
                    print("S", end="")
                elif node in self.closed_nodes:
                    print("X", end="")
                elif node in self.open_nodes:
                    print("O", end="")
                else:
                    print("?", end="")
            print()

    def add_obstacles(self, x, y):
        self.BOARD[x][y].traversable = False


if __name__ == "__main__":
    a = AStar(4, 4, start=(0, 0), end=(3, 3))
    a.add_obstacles(1,1)
    while not a.path_found:
        a.algorithm_loop()
    print(a.backtrack_path())
    a.print_board()
