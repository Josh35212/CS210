"""Choose colors & contrasts that comply with WCAG 2 guidelines. 

The Web Content Accessibility Guidelines are standards for making
web content (including text and diagrams) accessible, including to
people with mild visual impairments.  This includes color-blindness and
low vision.   Among the requirements is a minimum contrast between
text and background, based on luminance (brightness) only and not on
hue. There are additional issues in accessibility of treemaps, such
as providing alternative rendering for people who are blind or have
more severe visual impairments.  This module deals only with ensuring that
textual labels on the treemap contrast sufficiently with colors of tiles.

We will produce labels only in black (to contrast with light colors) and
white (to contrast with dark colors).  Tile background colors are generated
randomly, then a contrasting label color (black or white) is chosen.
For some tiles colors  the desired contrast ratio of 7:1, the WCAG AAA criterion,
cannot be met with either a black or white label.  In that case we generate
another random color and try again.

Code for determining contrast is absolutely brimming with magic numbers and seemingly arbitrary
formulas, which are normally a "bad smell" in code.  Rather than defining
symbolic constants, which would not be helpful in this case, we have tried to
follow as closely as possible the names and expression of the WCAG documentation
at https://www.w3.org/WAI/GL/wiki/Relative_luminance .
"""
import random
import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

def brightness(r: int, g: int, b: int) -> float:
    """Relative luminance, for determining whether white or
    black will have sufficient contrast.
    Formulas are from https://www.w3.org/WAI/GL/wiki/Relative_luminance
    """
    return 0.2126 * s_rgb_val(r) + 0.7152 * s_rgb_val(g) + 0.11 * s_rgb_val(b)

def s_rgb_val(rgb_val: int) -> float:
    """Conversion of pixel value 0..255 to float values used in WCAG guidelines"""
    s_rgb = rgb_val / 255
    if s_rgb < 0.03928:
        return s_rgb / 12.92
    return ((s_rgb+0.055)/1.055) ** 2.4

BLACK_BRIGHT = brightness(0, 0, 0)
WHITE_BRIGHT = brightness(255, 255, 255)

def contrast(foreground: float, background: float) -> float:
    """Contrast of two relative luminance values as defined by WCAG.
    foreground::background and background::foreground have same contrast
    """
    return abs((foreground + 0.05)/(background + 0.05))

def next_color() -> tuple[str, str]:
    """Generates random RGB color code and contrast color,
    satisfying Web Content Accessibility Guidelines (WCAG).
    WCAG requires contrast ratio 4.5:1 for text; 7.0 is considered
    "enhanced" (AAA) contrast, so we'll shoot for that.
    """
    while True:
        r = random.randint(0,255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        rgb_code = f"#{r:02x}{g:02x}{b:02x}"
        luma = brightness(r, g, b)
        log.debug(f"Color rgb({r},{g},{b}) has brightness {luma}")
        black_contrast = (luma + 0.05)/(BLACK_BRIGHT + 0.05)
        if black_contrast >= 7.0:
            log.debug(f"Sufficient contrast ({black_contrast}) with black")
            return rgb_code, "black"
        white_contrast = (WHITE_BRIGHT + 0.05) / (luma + 0.05)
        if white_contrast >= 7.0:
            log.debug(f"Sufficent contrast ({white_contrast}) with white")
            return rgb_code, "white"
        log.debug(f"Rejecting {r},{g},{b} ({luma}) for {black_contrast} with black and {white_contrast} with white")

