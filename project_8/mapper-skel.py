""" Construct a treemap.
Author: _Your name here_
Credits: _Did you collaborate with other students or find useful materials online?
         _Did you use AI tools to create some starter code?

Instructions:  Copy this file to mapper.py and then edit it. REMOVE this part of the
docstring and complete the identifying information above.  Credits should start out
empty, but add classmates or outside sources (including web sources or AI helpers)
as appropriate.  Be certain you understand it well enough to recreate it without help.

Example use:  python3 mapper.py data/small_flat.json 500 500
"""

# Standard Python library modules
import logging
import doctest

# Project modules, provided
import geometry
import display

# Enable logging with log.debug(msg), log.info(msg), etc.
logging.basicConfig()
log = logging.getLogger(__name__)  # Log messages will look like "DEBUG:mapper:msg"
log.setLevel(logging.DEBUG)   # Change to logging.INFO to suppress debugging messages


# Layout works with integers, floating point numbers, or a mix of the two.
Real = int | float    # Named type for use in type annotations


def treemap(values: list[Real], width: int, height: int):
    """Create treemap of values in width x height pixel display
    in Tk interface and in SVG file written to treemap.svg.
    """
    display.init(width, height)
    area = geometry.Rect(geometry.Point(0, 0),
                         geometry.Point(width, height))
    layout(values, area)
    display.wait_close()



def layout(items: list[Real], rect: geometry.Rect):
    """Lay elements of items out in rectangle.
    Version 0 (skeleton code) just takes a slice off the canvas for
    each rectangle.  You will replace it with much better recursive
    layouts.
    """
    while len(items) > 0:
        log.debug(f"Laying out {items} in {rect}")
        proportion = items[0] / sum(items)
        left_rect, rect = rect.split(proportion)
        display.draw_tile(left_rect, items[0])
        items = items[1:]


if __name__ == "__main__":
    doctest.testmod()



