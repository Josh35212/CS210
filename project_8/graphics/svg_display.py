"""SVG display of Treemap"""
import io
import sys


from .gr_display import Rectangular
from .tk_display import LINE_HEIGHT_APPROX  #FIXME: factor out of sibling module
from . import display_options

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# We will assemble the output SVG file from
# these parts, in this order
#   - SVG header
#   - CSS prologue
#   - CSS entries buffer, which we build up incrementally as we build the structure
#   - CSS epilogue
#   - SVG entries buffer, which we build up incrementally with 1-1 correspondence to CSS entries
#   - SVG epilogue

MARGIN = 3

SVG_HEAD = "uninitialized"  # Set in 'init' with height and width
CSS_PROLOGUE = """"
   <defs>
   <style>
   .tile rect { fill: white;  stroke: grey; }
   .tile_label {
            text-anchor: middle;  
            font-family: Helvetica, Arial, sans-serif;
            font-size: 12pt;
            white-space: pre-wrap; 
    }
    .group_outline { stroke: grey; fill: white; stroke-width: 2; }
    .group_outline:hover { stroke: red; fill: red; stroke-width: 20; }
"""
CSS_BUFFER: list[str] = []
CSS_EPILOGUE   = """
   </style>
   </defs>
"""
SVG_BUFFER: list[str] = []
SVG_EPILOGUE = "\n</svg>"


WIDTH = 0
HEIGHT = 0
IS_STYLED = False  # Is there a user-supplied CSS file, or do we need to randomly generate colors?


def init(width: int, height: int, svg_path: str = None):
    """We keep SVG commands in a buffer, to be written
    at the end of execution.
    """
    global SVG_HEAD
    global SVG_BUFFER
    global CSS_BUFFER
    global WIDTH
    global HEIGHT
    global IS_STYLED
    WIDTH, HEIGHT = width, height
    if not svg_path:
        svg_path = "treemap.svg"
    try:
        SVG_OUT = open(svg_path, "w")
        log.info(f"SVG figure will be written to {svg_path}")
    except FileNotFoundError:
        log.error(f"Could not open SVG file {svg_path}")
        sys.exit(1)

    SVG_HEAD = f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">'
    if display_options.css:
            IS_STYLED = True
            CSS_BUFFER += display_options.css


def xml_escape(s: str) -> str:
    """"Escape XML special characters as XML entities"""
    return ((s.replace("&", "&amp;").
            replace("<", "&lt;")).
            replace(">", "&gt;").
            replace('"', '&quot;'))

LBRACE = "{"
RBRACE = "}"

def draw_tile(r: Rectangular):
    """Generate display directions for a tile in SVG rendering.
    Includes labeling the rectangle, in text or as a tool-tip.
    """
    ((llx, lly), (urx, ury)) = r.box
    width = max(1, (urx - llx - 2 * MARGIN))
    height = max(1, (ury - lly - 2 * MARGIN))
    key = xml_escape(r.key)
    SVG_BUFFER.append(
        f"""\n<g class="{key}"><rect x="{llx + MARGIN}" y="{lly + MARGIN}" 
         width="{width}"  height="{height}"
         rx="10"  
         class="tile {key}" />
      """)
    if r.label:
        # Label is associated with group that wraps rect, so that
        # it can be rendered as either <title> or <text> depending
        # on available space
        draw_label(r)
    # If we haven't been given a custom CSS file, we'll fill in colors
    # that match the Tk rendering (which currently are randomly generated)
    if not IS_STYLED:
        CSS_BUFFER.append(f""".{key}  {LBRACE} fill: {r.fill_color}; {RBRACE}""")
        CSS_BUFFER.append(f"""text.{key} {LBRACE} fill: {r.label_color}; {RBRACE}""")
    SVG_BUFFER.append("</g>")




def begin_group(r: Rectangular):
    ((llx, lly), (urx, ury)) = r.box
    width = max(1, (urx - llx - 2 * MARGIN))
    height = max(1, (ury - lly - 2 * MARGIN))
    SVG_BUFFER.append(
        f"""<g class="group {r.key}">
            <rect x="{llx + MARGIN}" y="{lly + MARGIN}" 
            width="{width}"  height="{height}"
            rx="5"  
            class="group_outline" />
        <title>{r.label}</title> 
        """
    )

def end_group():
    SVG_BUFFER.append("\n</g>")



CHAR_WIDTH_APPROX = 13  # Rough approximation of average character width in pixels
LINE_HEIGHT_APPROX = 17

def text_width_roughly(label: str) -> int:
    """Approximate width of a string in pixels, based on
    rendering in a 12pt font.  Very rough since real width
    depends on font, screen resolution, width of individual
    characters, etc.  Just a "better than nothing" guess.
    """
    lines = label.split()  # Guess at LONGEST line
    longest = 0
    for line in lines:
        longest = max(longest, len(line) * CHAR_WIDTH_APPROX)
    return longest

def label_fits(label: str, llx: int, lly: int, urx: int, ury: int) -> bool:
    """Does this label fit in the screen area (probably)?
    We can't measure it directly (e.g., we don't know the typeface and size),
    so we make a very rough guess based on typical character width and line height.
    """
    width = text_width_roughly(label)
    if width > (urx - llx):
        return False
    if len(label.split()) * LINE_HEIGHT_APPROX > ury - lly:
        return False
    return True


def draw_label(r):
    """Generate display directions for a label in SVG rendering.
    May be rendered as <text> or <title> depending on available space, so
    make sure there is an element (e.g., a <g>...</g>) to attach the
    title to.
    """
    ((llx, lly), (urx, ury)) = r.box
    center_x = (urx + llx) // 2
    center_y = (lly + ury) // 2

    # If a label contains special HTML/XML characters, they must be escaped,
    # and newlines should break the text into parts
    label = xml_escape(r.label)
    key = xml_escape(r.key)

    # Let's make a title element (tool tip) regardless
    # (even when it duplicates the label)

    # "Title" element works as a tool-tip
    title = label.replace('\n', ' – ')
    SVG_BUFFER.append(f"""<title>{title}</title>""")

    # Also a label in the rectangle if it fits
    if display_options.messy or label_fits(label, llx, lly, urx, ury):
        label = label.replace('\n', f'</tspan><tspan x="{center_x}" dy="1.2em">')
        SVG_BUFFER.append(
            f"""<text x="{center_x}"  y="{center_y}" class="tile_label {key}">
              <tspan>{label}</tspan>
            </text>
            """)
        # Note text style was inserted in draw_tile already


def close():
    pass

def content() -> list[str]:
    # Assemble the output SVG file from parts
    log.info(f"Combining parts of SVG representation")
    return ( SVG_HEAD
             + CSS_PROLOGUE  + "\n".join(CSS_BUFFER) + CSS_EPILOGUE
             + "\n".join(SVG_BUFFER)
             + SVG_EPILOGUE )
