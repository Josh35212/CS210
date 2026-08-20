"""A graphical display of a cave represented as a rectangular grid of characters"""
import logging

import cave
import cave_view_text, cave_view_graphic
import config

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

ACTIVE = False  # Because doctests don't initialize display

def display(cavern: list[list[str]], width: int, height: int):
    """Create a graphical representation of cave using the grid.
    This graphical representation can be further manipulated
    (e.g., filling cave cells with water of various colors)
    with fill_cell.
    """
    global ACTIVE
    ACTIVE = True
    if config.GRAPHIC_DISPLAY:
        cave_view_graphic.display(cavern, width, height)
    if config.TEXTUAL_DISPLAY:
        cave_view_text.display(cavern, width, height)
    return


def change_water():
    """Switch to a new color of water"""
    if not ACTIVE:
        log.debug("Skipping change_water, display is not active")
        return
    if config.GRAPHIC_DISPLAY:
        cave_view_graphic.change_water()
    if config.TEXTUAL_DISPLAY:
        cave_view_text.change_water()
    return


def fill_cell(row: int, col: int):
    """Fill display of cave[row][col] with current colored water"""
    if not ACTIVE:
        log.debug("Skipping fill_cell because display is not active")
        # Probably because we're running doctests
        return
    if config.GRAPHIC_DISPLAY:
        cave_view_graphic.fill_cell(row, col)
    if config.TEXTUAL_DISPLAY:
        cave_view_text.fill_cell(row, col)

def prompt_to_close():
    """Prompt the user before closing the display,
    only for graphic display.
    """
    if config.GRAPHIC_DISPLAY:
        cave_view_graphic.prompt_to_close()
    return

def redisplay(cavern: list[list[str]]):
    """Make sure current version is on display"""
    if not ACTIVE:
        log.debug("Redisplay skipped because inactive (probably doctests)")
        return
    if config.TEXTUAL_DISPLAY:
        cave_view_text.redisplay(cavern)
    if config.GRAPHIC_DISPLAY:
        cave_view_graphic.redisplay(cavern)












