#!/usr/bin/env bash
#
#  Process a UO class roster file (with or without personally identifying information, which we discard)
# into a simple CSV file with counts by major.
#
# OS- or configuration-dependent names
#
PY=python3
COUNT=restructure/count_column.py
roster="${1}"
unblank="${roster// /_}"
counts="${unblank%.csv}_counts.csv"

echo "Convert ${roster} to ${counts}"
${PY} ${COUNT} "${roster}" --starting "Student name" --by "Major" >"${counts}"
