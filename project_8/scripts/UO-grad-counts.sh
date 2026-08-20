#! /bin/bash
#
#  Example script, takes restructure/data/UO-grads/UO-grads.csv to data/Majors/grads-202x.json
#  using hierarchical schema in restructure/schemas/UO-majors-schema.json and visualizes
#  with color scheme in restructure/data/UO-grads/UO-grads.css.
#
#  This script can be used as a model for building other data pipelines for visualization.
#
#  Run this script from the project directory (Treemap or Treemap-master)
#  to resolve the file paths correctly.
#

# ----------------------------------------------------------
# Data sources and parameters for grouping and visualizing
# ----------------------------------------------------------

#  Counts of UO graduates by major code, 2020-2024
COUNTS_CSV="restructure/data/UO-grads/UO-grads-by-major.csv"
# Schema for hierarchical organization as JSON
MAJORS_SCHEMA="restructure/schemas/UO-majors-schema.json"
# Color scheme as a CSV file.  I have used named colors, but
# you can also use RGB colors like #FF0000 for bright red.
MAJORS_COLORS="restructure/schemas/UO-majors-colors.csv"
#  Where we'll place the files we use for treemap visualization
DEST_DIR="data/Majors"
DEST_JSON="grad-counts-2020-24.json"
# Version ordered from largest to smallest totals in each group
DEST_JSON_ORDERED="grad-counts-ordered.json"
# CSS style sheet generated from MAJORS_COLORS
MAJORS_CSS="UO-majors-colors.css"
# Keep a copy of the SVG file here
MAJORS_SVG="uo_grads.svg"

# --------------------------------------------------------
#  The Python programs we will use
# --------------------------------------------------------
PY="python3"
BUILD="restructure/schematize.py"
COLORIZE="color_scheme.py"
REORDER="extensions/json_nest_sort.py"
VISUALIZE="treemap.py"

# ------------------------------------------------------------
#  Step 1:  Restructure CSV of individual major codes and counts
#  into a hierarchy (a "items" in our Python program) represented
#  as a JSON file.
#  Also create a version sorted from largest to smallest groups.
# -------------------------------------------------------------

echo "Converting ${COUNTS_CSV} to ${DEST_DIR}/${DEST_JSON}"
${PY} ${BUILD}  --key "Major code" --value "20-24" ${MAJORS_SCHEMA} ${COUNTS_CSV} ${DEST_DIR}/${DEST_JSON}

# -------------------------------------------------------------
# Step 2: Reorder the tree so that "heavier" branches precede "lighter"
# branches.  In a treemap visualization, this means that the biggest rectangle
# is in the upper left and smaller rectangles (usually including those too
# small to be labeled) are in the lower right, on each level of hierarchy
# --------------------------------------------------------------
echo "Building a version ordered by size at each level of hierarchy"
${PY} ${REORDER} ${DEST_DIR}/${DEST_JSON}  ${DEST_DIR}/${DEST_JSON_ORDERED}

# --------------------------------------------------------------
# Step 3: Convert color table in CSV format to CSS stylesheet.
# We could just let the conversion happen on the fly while visualizing,
# but converting to a stylesheet allows the user to edit further, e.g.,
# changing typeface for some elements.
# --------------------------------------------------------------
echo "Building CSS style sheet from color table in ${MAJORS_COLORS}"
${PY} ${COLORIZE} ${MAJORS_COLORS} ${DEST_DIR}/${MAJORS_CSS}

# --------------------------------------------------------------
# Step 4: Visualize the ordered version.  We'll use both the color
# table (for the tk visualizations) and the generated CSS file
# (for the SVG version).  If we had not generated the CSS file or
# did not edit it further (as we haven't here), we could omit
# the --css argument and the CSV color table would apply to both.
# --------------------------------------------------------------

echo "Visualizing"
${PY} ${VISUALIZE} -c ${MAJORS_COLORS} --css ${DEST_DIR}/${MAJORS_CSS} --svg ${DEST_DIR}/${MAJORS_SVG}\
      ${DEST_DIR}/${DEST_JSON_ORDERED} 1000 800


