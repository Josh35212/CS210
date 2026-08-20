"""Define a type for packaging up information that display.py passes to svg_display and tk_display."""

class Rectangular:
    def __init__(self,
                 # Category or class name, used as a class in SVG rendering
                 key: str,
                 # Bounding box
                 box: tuple[tuple[int, int], tuple[int, int]], # (llx, lly), (urx, ury)
                 # Textual label
                 label: str,
                 fill_color: str, label_color: str):

        self.key = key
        self.box = box
        self.label = label
        self.fill_color = fill_color
        self.label_color = label_color




