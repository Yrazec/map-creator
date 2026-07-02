"""The Map Creator."""

import collections
import os
import pathlib
import random


class MapCreator:
    """The Map Creator class."""

    _TREASURE = '?'
    _FREE_SPACE = ' '
    _WALL = u'\u2588'

    def __init__(self, size: int) -> None:
        """
        Create MapCreator class instance.

        :param int size: the map size (square)
        """

        self._size = size if size % 2 == 1 else size + 1

    def generate_map(self) -> list[list[bool]]:
        """
        Generate whole map - self._size based.

        :return: the map - 2D grid of booleans
        """

        rows = cols = self._size
        grid = [[True for _ in range(cols)] for _ in range(rows)]

        inner_start = (1, 1)
        self._carve_path(row=inner_start[0], column=inner_start[1], rows=rows, cols=cols, grid=grid, visited=set())

        MapCreator._seal_all_borders(grid)
        MapCreator._add_entrance(grid)
        MapCreator._add_exit(grid, inner_start)

        return grid

    def _carve_path(
        self,
        row: int,
        column: int,
        rows: int,
        cols: int,
        grid: list[list[bool]],
        visited: set[tuple[int, int]]
    ) -> None:
        """
        Carve path in the 2D grid map.

        :param int row: the current row
        :param int column: the current column
        :param int rows: the rows number
        :param int cols: the columns number
        :param list[list[bool]] grid: the 2D map grid
        :param set[tuple[int, int]] visited: the visited set
        """

        visited.add((row, column))
        grid[row][column] = False

        directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
        random.shuffle(directions)

        for dr, dc in directions:
            nr, nc = row + dr, column + dc
            if MapCreator._is_valid(nr, nc, rows, cols) and (nr, nc) not in visited:
                mid_r, mid_c = row + dr // 2, column + dc // 2
                grid[mid_r][mid_c] = False
                self._carve_path(row=nr, column=nc, rows=rows, cols=cols, grid=grid, visited=visited)

    @staticmethod
    def print_char_map(char_map: list[list[str]]) -> None:
        """
        Print the character map.

        :param list[list[str]] char_map: the character map
        """

        for row in char_map:
            print(''.join(row))

    @staticmethod
    def dump_to_file(char_map: list[list[str]], filepath: str) -> None:
        """
        Print the character map.

        :param list[list[str]] char_map: the character map
        :param str filepath: the path to the file
        """

        reduced = [''.join(row) for row in char_map]
        reduced = '\n'.join(reduced)

        os.makedirs(pathlib.PureWindowsPath(filepath).parent)

        with open(filepath, mode='w+', encoding='utf-8') as f:
            f.write(reduced)

    @staticmethod
    def place_treasures(grid: list[list[bool]], chance: float = 0.3) -> list[list[str]]:
        """
        Place treasures in the 2D grid map.

        :param list[list[bool]] grid: the 2D map grid
        :param float chance: the chance of treasure
        :return: the placed treasures map
        """

        rows = len(grid)
        cols = len(grid[0])
        char_map = [[MapCreator._WALL if cell else MapCreator._FREE_SPACE for cell in row] for row in grid]

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for row in range(1, rows - 1):
            for column in range(1, cols - 1):
                if not grid[row][column]:
                    open_neighbors = 0
                    for dr, dc in directions:
                        nr, nc = row + dr, column + dc
                        if not grid[nr][nc]:
                            open_neighbors += 1
                    if open_neighbors == 1 and random.random() < chance:
                        char_map[row][column] = MapCreator._TREASURE

        return char_map

    @staticmethod
    def _is_valid(row: int, column: int, rows: int, cols: int) -> bool:
        """
        Check if passed cell is valid.

        :param int row: the current row
        :param int column: the current column
        :param int rows: the rows number
        :param int cols: the columns number
        :return: True if the cell is valid, False otherwise
        """

        return 0 <= row < rows and 0 <= column < cols

    @staticmethod
    def _seal_all_borders(grid: list[list[bool]]) -> None:
        """
        Seal all borders.

        :param grid: list[list[bool]] grid: the 2D map grid
        """

        rows = len(grid)
        cols = len(grid[0])

        for r in range(rows):
            grid[r][0] = True
            grid[r][cols - 1] = True

        for c in range(cols):
            grid[0][c] = True
            grid[rows - 1][c] = True

    @staticmethod
    def _add_entrance(grid: list[list[bool]]) -> None:
        """
        Add entrance to the 2D grid map.

        :param list[list[bool]] grid: the 2D map grid
        """

        grid[0][0] = False

        if not grid[1][0]:
            grid[1][0] = False

        elif not grid[0][1]:
            grid[0][1] = False

        else:
            grid[1][0] = False

    @staticmethod
    def _add_exit(grid: list[list[bool]], start: tuple[int, int]) -> None:
        """
        Add exit to the 2D grid map.

        :param list[list[bool]] grid: the 2D map grid
        :param tuple[int, int] start: the starting position
        """

        rows = len(grid)
        cols = len(grid[0])
        visited = set()
        queue = collections.deque([start])
        visited.add(start)

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        candidates = []

        while queue:

            row, column = queue.popleft()

            if row == rows - 2:
                candidates.append((row + 1, column))
            elif column == cols - 2:
                candidates.append((row, column + 1))

            for dr, dc in directions:
                nr, nc = row + dr, column + dc
                if MapCreator._is_valid(nr, nc, rows, cols) and not grid[nr][nc] and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    queue.append((nr, nc))

        if candidates:
            row, column = random.choice(candidates)
            grid[row][column] = False
