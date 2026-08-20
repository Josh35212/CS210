"""Flood-fill to count chambers in a cave.
CS 210 project.
Josh Gilliam, November 3rd 2025
Credits: None
"""

import doctest
import cave
import config
import cave_view
from tracer import trace

def scan_cave(cavern: list[list[str]]) -> int:
    """Scan the cave for air pockets.  Return the number of
    air pockets encountered.

    >>> cavern_1 = cave.read_cave("data/tiny-cave.txt")
    >>> scan_cave(cavern_1)
    1
    >>> cavern_2 = cave.read_cave("data/cave.txt")
    >>> scan_cave(cavern_2)
    3
    """
    count = 0
    for row_i in range(len(cavern)):
        for col_i in range(len(cavern[0])):
            if cavern[row_i][col_i] == config.AIR:
                pour(cavern, row_i, col_i)
                cave_view.change_water()
                count += 1
    return count

@trace() # comment out for readability
def pour(cavern: list[list[str]], row_i: int, col_i: int):
    """Fill the whole chamber around cavern[row_i][col_i] with water
    """
    if row_i not in range(len(cavern)):
        return 
    if col_i not in range(len(cavern[0])):
        return
    if not cavern[row_i][col_i] == config.AIR:
        return
    else:
        cavern[row_i][col_i] = config.WATER
        cave_view.fill_cell(row_i, col_i)
        pour(cavern, row_i - 1, col_i)
        pour(cavern, row_i, col_i - 1)
        pour(cavern, row_i + 1, col_i)
        pour(cavern, row_i, col_i + 1)

def main():
    doctest.testmod()
    cavern = cave.read_cave(config.CAVE_PATH)
    cave_view.display(cavern,config.WIN_WIDTH, config.WIN_HEIGHT)
    chambers = scan_cave(cavern)
    print(f"Found {chambers} chambers")
    cave_view.redisplay(cavern)
    cave_view.prompt_to_close()
    
if __name__ == "__main__":
    main()
