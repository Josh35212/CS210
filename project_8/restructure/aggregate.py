"""Aggregate rows of a CSV file by summing certain fields.
Intended as a preparatory step before extracting a tree
from the CSV file.

Uses schema files compatible with those used by csv_to_json.py,
provided only retained columns are given.   If elided columns are
mentioned in the schema, there will be errors in subsequent
processing using that schema.
"""
import csv
import json

import argparse
import io

import logging
import numbers
import sys


logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

def cli() -> object:
    """Command line interface"""
    parser = argparse.ArgumentParser("Summarize CSV file on selected columns")
    parser.add_argument("schema", type=argparse.FileType(mode="r", encoding="utf-8-sig"),
                        help="JSON file specifying label and data columns")
    parser.add_argument("input", type=argparse.FileType(mode="r", encoding="utf-8-sig"),
                        nargs="?", default=sys.stdin,
                        help="Flat data file as CSV"
                        )
    parser.add_argument("--by", type=str,
                        help="Field to summarize by (break at changes in this or prior columns as defined in schema)")
    parser.add_argument("output", type=argparse.FileType(mode="w"),
                        nargs="?", default=sys.stdout,
                        help="Summarized CSV file")
    args = parser.parse_args()
    return args

def control_field_labels(label_fields: list[str], summarize_by_field: str) -> list[str]:
    """Returns the prefix of label_fields that will be considered when
    summing by summarize_by_field.
    """
    for i, label in enumerate(label_fields):
        if label == summarize_by_field:
            return label_fields[:i+1]
    raise ValueError(f"Field {summarize_by_field} not in schema label fields {label_fields}")


def is_control_break(record: dict[str, object], control_fields: list[str], current_values: list[str]) -> bool:
    """Does a non-empty field of the record differ
    from current values for one of the control fields?
    """
    for i, key in enumerate(control_fields):
        if record[key] and record[key] != current_values[i]:
            return True
    return False


def load_schema(schema_file: io.IOBase) -> dict[str, list[str]]:
    """Configuration options we expect:
       "labels" -> non-empty list of column headers
       "values" -> non-empty list of column headers
    """
    schema = json.load(schema_file)
    log.debug(f"Schema: \n{schema}")
    assert isinstance(schema, dict), f"Schema should be a dict with entries 'labels' and 'data'"
    return schema

def guess_numeric_value(field: str) -> object:
    """Convert field into int or float; empty interpreted as zero"""
    try:
        return int(field)
    except Exception: pass
    try:
        return float(field)
    except Exception: pass
    if not field:
        # Interpret blank and null fields as zero
        return 0
    raise ValueError(f"Unable to convert {field} to an int or float")



def summarize(in_csv: io.IOBase,
              control_fields: list[str], data_fields: list[str],
              out_csv: io.IOBase):
    """Summarize CSV file on control fields,
    i.e., accumulate sums when non-empty control field labels match current state, 
    emit and reinitialize when there is a change.
    """
    reader = csv.DictReader(in_csv)
    writer = csv.writer(out_csv)
    # Write column headers on output
    writer.writerow(control_fields + data_fields)

    row_labels = ["NA" for label in control_fields]
    sums = [0 for label in data_fields]

    input_records = iter(reader)  # Lets me special case first row

    ## First row
    record = next(input_records)
    row_labels = [record[label] for label in control_fields]
    sums = [guess_numeric_value(record[col]) for col in data_fields]

    ## Subsequent rows
    for record in input_records:
        if is_control_break(record, control_fields, row_labels):
            writer.writerow(row_labels + sums)
            sums = [0 for label in data_fields]
        for i,label in enumerate(control_fields):
            if record[label]:  # Retain "sticky" values when field is empty
                row_labels[i] = record[label]
            log.debug(f"Labels effectively {row_labels}")
        for i, value_column in enumerate(data_fields):
            sums[i] += guess_numeric_value(record[value_column])

    ## Treat EOF as a control break
    writer.writerow(row_labels + sums)


def main():
    args = cli()
    schema = load_schema(args.schema)
    log.debug(f"Schema: {map}")
    sum_by_field = args.by
    control_fields = control_field_labels(schema["labels"], sum_by_field)
    data_fields = schema["values"]
    summarize(args.input, control_fields, data_fields, args.output)


if __name__ == "__main__":
    main()
