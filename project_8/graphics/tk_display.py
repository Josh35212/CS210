"""
Tk (built-in Python graphics package) display of Treemap canvas.
"""

from . import graphics  # Zelle's Tk graphics package
from .gr_display import Rectangular

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

MARGIN = 4   # Between tile and its surrounding object
TYPEFACE = "helvetica"
FONTSIZE = 12

# Text size estimates borrowed from svg_display.  Could be different
# in future depending on text sizes.  I don't know how to measure
# rendered text size directly in Tk, but maybe it's possible?
#
CHAR_WIDTH_APPROX = 12  # Rough approximation of average character width in pixels
LINE_HEIGHT_APPROX = 17


CANVAS: graphics.GraphWin | None = None   # Set in init function

def init(width: int, height: int):
    global CANVAS
    CANVAS = graphics.GraphWin("Treemap", width, height)
    CANVAS.setCoords(0, 0, width, height)


# Replacing individual calls to draw_rect and draw_label by
# a single function draw_tile, taking explicit arguments instead
# of a property list


def draw_tile(r: Rectangular):
    ((llx, lly), (urx, ury)) = r.box
    """Draw a tile and its label, transforming to screen coordinates."""
    assert CANVAS, "Did you forget to initialize the window?"
    # The tile background
    lly_flipped = CANVAS.height - lly
    ury_flipped = CANVAS.height - ury
    image = graphics.Rectangle(graphics.Point(llx+MARGIN, lly_flipped-MARGIN),
                              graphics.Point(urx-MARGIN,ury_flipped+MARGIN))
    if r.fill_color:
        image.setFill(r.fill_color)
    image.draw(CANVAS)

    # The textual label on the background
    if  label_fits(r.label, llx, lly, urx, ury):
        label = graphics.Text(graphics.Point((llx + urx)/2, (lly_flipped + ury_flipped)/2), r.label)
        label.setSize(FONTSIZE)
        label.setFace(TYPEFACE)
        label.setTextColor(r.label_color)
        label.draw(CANVAS)



def text_width_roughly(label: str) -> int:
    """Approximate width of a string in pixels.
    Very rough since real width
    depends on font, screen resolution, width of individual
    characters, etc.  Just a "better than nothing" guess.
    """
    lines = label.split()  # Guess at LONGEST line
    longest = 0
    for line in lines:
        longest = max(longest, len(line) * CHAR_WIDTH_APPROX)
    return longest

def label_fits(label: str, llx: int, lly: int, urx: int, ury: int) -> bool:
    # Too wide?
    if text_width_roughly(label) > urx - llx:
        return False
    # Too tall?
    if len(label.split()) * LINE_HEIGHT_APPROX > ury - lly:
        return False
    return True




def wait_close():
    """Hold display on screen until user clicks"""
    print("Click window to close it")
    CANVAS.getMouse()
    CANVAS.close()


