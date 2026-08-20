"""A simple scatter plot of points in the unit square (0,0) to (1,1)
Author: Michal Young, July 2022
Credits:  Independent work, but we are grateful for
   graphics.py by John Zell of Wartburg College.
"""

from graphics.graphics import GraphWin, Point, Rectangle
from typing import Optional

## Global parameters:  How big is a point, in pixels?
PT_WID = 6                  # Width of a point
KERF = max(1, PT_WID//2)    # Extends this far up and down

## Module state, initialized by init
WIN: Optional[GraphWin] = None
ORIGIN: tuple[float, float] = [0.0, 0.0]
BOUND: tuple[float, float] = [1.0, 1.0]

def init(width=500, height=500, origin=(0.0, 0.0), bound=(1.0, 1.0)):
    """Initializes a canvas for plotting points in the Cartesian plain.
    By default we plot in the unit square, from (0,0) to (1,1),
    in a canvas of size 500x500 pixels.  Pass height and width to
    choose a different canvas size.  Pass origin and bound to set a
    different range of world coordinates.
    """
    global WIN
    WIN = GraphWin("Plot", width, height )
    WIN.setBackground("white")
    global ORIGIN
    ORIGIN = origin
    global BOUND
    BOUND = bound


def close():
    """Return to uninitialized state, with no window"""
    global WIN
    if WIN:
        WIN.close()
        WIN = None


def wait_to_close():
    """Prompt user before closing display, so the
    user has time to inspect it.  No effect or delay
    if window is not present.
    """
    global WIN
    if WIN:
        input("Press enter to close plot window")
        close()



def plot(x: float, y: float, color_rgb: tuple[int, int, int]=(50, 50, 50)):
    """If we are plotting (WIN has been initialized), plot point (x,y) in the window.
    color_rgb should be a tuple of three integers in the range 0 to 255,
    indicating intensity of red, green, and blue.
    In uninitialized state (WIN is None), do nothing.
    """
    if WIN is None:
        return
    x_bound, y_bound = BOUND
    x_origin, y_origin = ORIGIN
    assert x_origin <= x <= x_bound, f"x coordinate outside plot area {ORIGIN} to {BOUND}"
    assert y_origin <= y <= y_bound, f"y coordinate outside plot area {ORIGIN} to {BOUND}"
    # Scale world coordinates to canvas coordinates
    x_center = (x - x_origin) * WIN.width
    y_center = (y - y_origin) * WIN.height
    # Mark with a 2x2 pixel rectangle
    mark = Rectangle(Point(x_center - KERF, y_center - KERF),
                     Point(x_center + KERF, y_center + KERF))
    r, g, b = color_rgb
    rgb_str = "#%02x%02x%02x" % (r,g,b)
    mark.setFill(rgb_str)
    mark.draw(WIN)

