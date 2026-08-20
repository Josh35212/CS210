#!/usr/bin/env bash
#
#  Process CSV of majors and counts with column headers
#  into a JSON tree based on  major codes and programs at U. Oregon.
#
# OS- or configuration-dependent names
#
PY="python3"
BUILD="restructure/schematize.py"
SCHEMA="restructure/schemas/UO-majors.json"
CSV_IN="${1}"
JSON_OUT="${CSV_IN%.csv}.json"

echo "Convert ${CSV_IN} to ${JSON_OUT}"
${PY} ${BUILD}  --key "Major" --value "Count" "${SCHEMA}" "${CSV_IN}" "${JSON_OUT}"
