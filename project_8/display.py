"""Graphical display for treemapper.  Displays Tk graphics incrementally
and returns an SVG version, which can be saved to a file.

A color scheme from a key: color table and/or a CSS style sheet
may be applied based on graphics.display_options.

Note we are using modules (display, tk_display, svg_display) as stateful objects,
which makes them "singletons".   To allow multiple instances of display (e.g.,
 building two different treemaps at the same time to compare them) would require
rewrite of all three modules to isolate state in objects managed by other code.
"""

import graphics.tk_display as tk
import graphics.svg_display as svg
import graphics.gr_display as gr
import geometry
from graphics import display_options as options
import color_contrast


import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


# ------
# Tk display requires us to keep a stack of keys so that we can
# inherit graphical attributes from a parent.
#
INCLUSION_STACK: list[str] = []  # Initially empty


# --------------------------------------------------------
#  API is
#       init(width: int, height: int):
#           Creates the display (Tk visible and SVG buffer) with width and height in pixels
#
#           def draw_tile(r: geometry.Rect,
#                   key: object = None,
#                   value: object = None):
#           Draws a tile.  The tile is labeled with key (usually a string) and/or value (usually numeric).
#           If provided, the key will be normalized to conform to SVG/CSS naming rules and may be mapped to a color
#           in graphics.display_options.color_scheme (usually from a CSV file via color_scheme.py)
#           or associated with CSS styling through graphics.display_options.css.
#           Example normalization of keys to CSS class identifiers:
#               "dogs" -> "dogs",
#               "99 problems & 32 solutions" -> "C_99problems32solutions"
#               0x10 -> "C_16"
#
#           A color may be inherited from an enclosing group.  If there is no associated color
#           for the key or any enclosing group, a random color (and contrasting label color)
#           will be generated.
#
#       begin_group(r: geometry.Rect,
#                 key: str | None = None,
#                 value: str | None = None):
#           Begins a rectangular group of tiles, which should tile r.
#           Arguments are the same as draw_tile, but the label is not displayed in Tk and in
#           SVG is only visible as a tool tip on hover.  To hover on a group, place cursor
#           *between* tiles. begin_group must be paired with matching end_group.
#
#       end_group():
#           Marks the end of the current group of tiles. Groups may be nested arbitrarily, but
#           must be properly nested (like nested parentheses).   Tiles can inherit colors within
#           groups, in both the Tk graphics and the SVG graphics.
#
#       svg_content() -> list[str]:
#           Returns the SVG representation as a list of strings.
#           Typically these should be written to a file, which can then
#           be opened in a web browser or illustration application like
#           Inkscape (free and open source) or Adobe Illustrator (very not free or open source).
#
#       wait_close():
#           Closes the display after waiting for user to click it.
#

# -------------------------------------------------------------------
#  API visible functions
# -------------------------------------------------------------------

def init(width: int, height: int):
    tk.init(width, height)
    svg.init(width, height)


def draw_tile(r: geometry.Rect,
              key: object = None,
              value: object = None):
    """Draw the tile (on both media).
     Displays on Tk (Python built-in graphics) and
     also writes corresponding graphics into buffer to
     produce corresponding SVG diagram which can be displayed
     in a web page, imported into a diagramming tool like
     Inkscape, OmniGraffle, Illustrator, etc.
     `key`, if present, is normalized to become the class name
     for SVG CSS class and/or the Tk color assignment table.
    """
    log.debug(f"Drawing tile key {key} value {value} at {r}")
    # fill_color and label_color will be used in tk graphics,
    # and also in SVG graphics ONLY if the user hasn't provided a CSS stylesheet
    if value and key:
        label = f"{key}\n{value}"
    elif value:
        label = f"{value}"
    elif key:
        label = str(key)
    else:
        label = ""
    # For everything else, we need the key normalized
    key = normalize_key(key)
    fill_color, label_color = lookup_colors(key)
    tile = gr.Rectangular(key,
                          ((r.ll.x, r.ll.y), (r.ur.x, r.ur.y)),
                          label=label, fill_color=fill_color, label_color=label_color)

    tk.draw_tile(tile)
    svg.draw_tile(tile)


def begin_group(r: geometry.Rect,
                key: str | None = None,
                value: str | None = None):
    """
    Begin a group of tiles. The `key` argument, if present,
    is normalized to become the class name for SVG CSS and/or
    the Tk color assignment table.  The (key, value) pair may not
    be directly visible, but if either `key` or `value` is present
    it will be displayed as a tooltip in SVG.
    """
    global INCLUSION_STACK
    INCLUSION_STACK.append(key)
    fill_color, label_color = lookup_colors(key)
    if value:
        label = f"{key}: {value}"
    else:
        label = f"{key}"
    key = normalize_key(key)
    region = gr.Rectangular(key, ((r.ll.x, r.ll.y),(r.ur.x, r.ur.y)),
                            label=label, fill_color=fill_color, label_color=label_color)
    # SVG version - create SVG group
    # Note fill and label colors will be ignored if we have a CSS stylesheet
    svg.begin_group(region)

def end_group():
    """Must be matched with begin_group"""
    # Tk:  Nothing to do
    # SVG: Ends the SVG group
    INCLUSION_STACK.pop()
    svg.end_group()

def svg_content() -> list[str]:
    """Contents of the SVG representation"""
    return svg.content()

def wait_close():
    """Hold display on screen until user indicates finish"""
    svg.close()
    tk.wait_close()


# --------------------------------------------------------------
#  Internal functions, not part of API
# --------------------------------------------------------------

def lookup_colors(key: str) -> tuple[str, str]:
    """Finds nearest color for key or enclosing key on inclusion stack."""
    if key in options.color_scheme:
        return options.color_scheme[key]
    for enclosing in reversed(INCLUSION_STACK):
        if enclosing in options.color_scheme:
            return options.color_scheme[enclosing]
    # Not mapped in any enclosing object.  Generate a random color pair.
    # We memoize the assignment for two reasons:  So we can propagate it if
    # we are coloring a group, and so we will use the same color if we encounter
    # the same key again.   Exception:  None or "" don't get an assigned color,
    # and don't propagate to parts.
    log.info(f"Could not find color for key {key}; a random color will be assigned.")
    fill, text = color_contrast.next_color()
    if key:
        options.color_scheme[key] = (fill, text)
    return fill, text


def normalize_key(key: object) -> str:
    """Extract a suitable and predictable key from a category name.
    We extract as first line, replacing spaces by underscores, and
    removing any other non-alphanumeric characters.
    The result is usable as a dict key (for Tk color schemes)
     and CSS classes (to use in the SVG output).
    """
    key = str(key)
    basis = key.split()[0]
    if not basis[0].isalpha():
        basis = "C_" + basis
    chars = [ch for ch in basis if ch.isalnum()]
    return "".join(chars)


