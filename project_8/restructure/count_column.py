"""Produce aggregated counts by content of one column in a CSV spreadsheet.
Designed particularly for UO class rosters, where we can count majors, levels, etc.
These spreadsheets may contain other material before and after the part we want.  We
assume that we can trigger start of counting by label in column 1.
"""

import csv
import argparse
import io

import logging
import sys


logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

def cli() -> object:
    """Command line interface"""
    parser = argparse.ArgumentParser("Occurrences of values in a given CSV field")
    parser.add_argument("input", type=argparse.FileType(mode="r", encoding="utf-8-sig"),
                        nargs="?", default=sys.stdin,
                        help="Flat data file as CSV"
                        )
    parser.add_argument("--starting", type=str,
                        help="Start counting after header line that starts with this string")
    parser.add_argument("--by", type=str,
                        help="Column containing values to count")
    parser.add_argument("output", type=argparse.FileType(mode="w"),
                         nargs="?", default=sys.stdout,
                         help="Summarized CSV file")
    args = parser.parse_args()
    return args

def reader_from(in_csv: io.IOBase, from_label: str) -> csv.DictReader:
    """A csv DictReader that starts with the line after the selected header line"""
    reader = csv.reader(in_csv)
    for row in reader:
        if len(row) > 0 and row[0] == from_label:
            log.debug(f"Found header row {row}")
            headers = row
            dict_reader = csv.DictReader(in_csv, fieldnames = headers)
            return dict_reader
        log.debug(f"Skipping {row}")
    raise ValueError(f"Did not find header {from_label} in column 0")

def count_column(in_csv: io.IOBase, count_column: str, from_row: str="") -> dict[str, int]:
    """Count occurrences of each label in selected column,
    starting from a row that starts with from_row if given.
    """
    if from_row:
        reader = reader_from(in_csv, from_row)
    else:
        reader = csv.DictReader(in_csv)
    log.debug("Obtained reader")

    counts = { }
    for row in reader:
        if count_column not in row:
            raise ValueError(f"Didn't find {count_column} in {row}")
        value = row[count_column]
        counts[value] = 1 + counts.get(value, 0)
    return counts

def total_share(counts: dict[str, int]) -> dict[str, float]:
    """Convert counts to share of total"""
    total = sum(counts.values())
    shares = {}
    for key, value in counts.items():
        shares[key] = value / total
    return shares

def store(f: io.IOBase, label: str, counts: list[list]):
    writer = csv.writer(f)
    writer.writerow([label, "Count", "Share"])
    for row in counts:
        writer.writerow(row)

def join(rows: list, values: dict):
    """To each row [key, ...]  append values[key]"""
    for row in rows:
        row.append(values[row[0]])

def main():
    args = cli()
    log.debug(f"count_column reading from {args.input.name}")
    column = args.by
    counts = count_column(args.input, column, from_row=args.starting)
    shares = total_share(counts)
    ordered = sorted(([label, count] for label, count in counts.items()),
                key=lambda pair: 0 - pair[1])
    join(ordered, shares)
    store(args.output, args.by, ordered)


if __name__ == "__main__":
    main()