"""Graphic display of Boggle board"""
from typing import Optional

import config
import graphic_view
import text_view

def display(board: list[list[str]]):
    """Initialize the representation."""
    if config.GRAPHIC_VIEW:
        graphic_view.display(board)
    if config.TEXT_VIEW:
        text_view.display(board)

def celebrate(found: str):
    """Wow, we found something!"""
    if config.TEXT_VIEW:
        text_view.celebrate(found)
    if config.GRAPHIC_VIEW:
        graphic_view.celebrate(found)

def mark_occupied(row: int, col: int):
    """Mark board[row][col] as occupied in display"""
    if config.GRAPHIC_VIEW:
        graphic_view.mark_occupied(row, col)
    if config.TEXT_VIEW:
        text_view.mark_occupied(row, col)

def mark_unoccupied(row: int, col: int):
    """Mark board[row][col] as unoccupied (available)"""
    if config.GRAPHIC_VIEW:
        graphic_view.mark_unoccupied(row, col)
    if config.TEXT_VIEW:
        text_view.mark_unoccupied(row, col)


def prompt_to_close():
    """Prompt the user before closing the display"""
    if config.GRAPHIC_VIEW:
        graphic_view.prompt_to_close()


