"""Textual display of Boggle board.

We use lower case for letters that have not been used,
upper case for letters that have been used.

We make use of fact (assumption) that occupied/unoccupied
appear in LIFO (stack-like) order for dynamic display of
moves taken.
"""

from typing import Optional

import config

BOARD: Optional[list[list[str]]] = []
IN_USE_LETTERS: list[str] = []
IN_USE_COORDS: list[tuple[int, int]] = []

def display(board: list[list[str]]):
    """Initialize the representation."""
    global BOARD
    BOARD = [[cell.lower() for cell in row] for row in board]
    show_board(BOARD)

def show_board(board: list[list[str]]):
    """We print with spaces to make it more accessible
    to a screen reader.
    """
    if not BOARD:
        # In the context of a doctest
        return
    print("\nBoard: ")
    for row in BOARD:
        print(" ".join(row))
    print()

def celebrate(found: str):
    print(f"\nFound: {found}")
    show_board(BOARD)

def mark_occupied(row: int, col: int):
    """Board[row][col] is being explored"""
    global BOARD
    if not BOARD:
        # This happens in doctests
        return
    IN_USE_LETTERS.append(BOARD[row][col])
    IN_USE_COORDS.append((row, col))
    letter = BOARD[row][col]
    BOARD[row][col] = letter.upper()
    if not config.TEXT_VIEW_EACH_MOVE:
        return
    if len(IN_USE_LETTERS) == 1:
        # New line for words starting with a new letter
        print()
        print(" ".join(IN_USE_LETTERS) + ". ", end="")


def mark_unoccupied(row: int, col: int):
    """Mark board[row][col] as unoccupied (available)"""
    if not BOARD:
        # In the doctests
        return
    letter = BOARD[row][col]
    BOARD[row][col] = letter.lower()
    IN_USE_LETTERS.pop()
    IN_USE_COORDS.pop()
    if config.TEXT_VIEW_EACH_BACK:
        print(" ".join(IN_USE_LETTERS) + "! ", end="")
        if len(IN_USE_LETTERS) == 1:
            print()



def prompt_to_close():
    """Prompt the user before closing the display;
    Not applicable to text display"""
    return


