"""Options for treemap display.
We keep these in the form of a "property list", that is, a dict with properties as keys
and property values as settings.   Options can be set by main driver program and accessed
by other modules whose behavior they control.  Some options may apply to only some display media,
e.g., CSS stylesheets apply to SVG but not to Tk graphics.

Keeping these options as a dict rather than a set of individual variables makes it convenient to
check whether an option has been set at all.

Usage:
import treemap_options as options
...
if options.prop_name:
    # Code to execute if property has a truthy value
"""


color_scheme: dict[str, tuple[str, str]] = {}    # Maps class name to (fill, text) color pair
css: str | None = None
messy: bool = False

