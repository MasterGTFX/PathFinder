import unittest
from a_star_algorithm import AStarAlgorithm


class TestStringMethods(unittest.TestCase):

    def test_3x3_no_obstacles(self):
        a = AStarAlgorithm(array_board=[[2, 0, 0],
                                        [0, 0, 0],
                                        [0, 0, 3]])
        while not a.path_found:
            a.algorithm_loop()
        self.assertEqual(a.board_to_2d_list(), [[2, 0, 0],
                                                [0, 4, 0],
                                                [0, 0, 3]])

    def test_3x3_with_obstacles(self):
        a = AStarAlgorithm(array_board=[[2, 0, 0],
                                        [1, 1, 0],
                                        [0, 0, 3]])
        while not a.path_found:
            a.algorithm_loop()
        self.assertEqual(a.board_to_2d_list(), [[2, 4, 0],
                                                [1, 1, 4],
                                                [0, 0, 3]])

    def test_4x3_no_obstacles(self):
        a = AStarAlgorithm(array_board=[[2, 0, 0],
                                        [0, 0, 0],
                                        [0, 0, 0],
                                        [0, 0, 3]])
        while not a.path_found:
            a.algorithm_loop()
        self.assertEqual(a.board_to_2d_list(), [[2, 0, 0],
                                                [0, 4, 0],
                                                [0, 0, 4],
                                                [0, 0, 3]])

    def test_4x3_with_obstacles(self):
        a = AStarAlgorithm(array_board=[[2, 0, 0],
                                        [1, 1, 0],
                                        [1, 1, 0],
                                        [0, 0, 3]])
        while not a.path_found:
            a.algorithm_loop()
        self.assertEqual(a.board_to_2d_list(), [[2, 4, 0],
                                                [1, 1, 4],
                                                [1, 1, 4],
                                                [0, 0, 3]])

    def test_3x4_no_obstacles(self):
        a = AStarAlgorithm(array_board=[[2, 0, 0, 0],
                                        [0, 0, 0, 0],
                                        [0, 0, 0, 3]])
        while not a.path_found:
            a.algorithm_loop()
        self.assertEqual(a.board_to_2d_list(), [[2, 0, 0, 0],
                                                [0, 4, 0, 0],
                                                [0, 0, 4, 3]])

    def test_3x4_with_obstacles(self):
        a = AStarAlgorithm(array_board=[[2, 0, 0, 0],
                                        [1, 1, 1, 0],
                                        [0, 0, 0, 3]])
        while not a.path_found:
            a.algorithm_loop()
        self.assertEqual(a.board_to_2d_list(), [[2, 4, 4, 0],
                                                [1, 1, 1, 4],
                                                [0, 0, 0, 3]])


if __name__ == '__main__':
    unittest.main()
