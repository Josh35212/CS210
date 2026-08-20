"""Extract the tree structure implied by a table (CSV format)
where some columns represent categories, subcategories, etc.,
and some columns (usually after the labels) are values (often numeric)
associated with leaf-level entries.
Output as nested dicts in JSON format.

Example input:
Program,Level,Course,SCH
CS,1xx,CS 102,376
CS,1xx,CS 110,976
CS,3xx,CS 330,320
CS,4xx,CS 407,40

Example output:
{ "CS": {
    "1xx": { "CS 102": 376,  "CS 110": 976 },
    "3xx": { "CS 330": 320 },
    "4xx": { "CS 407": 40 }}}

Transformation is guided by a configuration file in JSON format, e.g.
{
  "COMMENT" : "Configuration file for csv_to_json.py, gives schema of CSV file by listing column headers",
  "labels" : ["Program" ,"Level" , "Course"],
  "values" : ["SCH"]
}

Note "values" columns will be interpreted as numbers (int or float) if they appear to be numeric,
but "labels" columns will always be treated as strings.

FIXME: To support summarization, we need to ignore schema columns that are not present
  (perhaps with a warning).
"""

import json
import csv
import argparse
import io

import logging
import sys

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

def cli() -> object:
    """Command line interface"""
    parser = argparse.ArgumentParser("Extract implied tree from CSV columns")
    parser.add_argument("schema", type=argparse.FileType(mode="r"),
                        help="JSON file specifying label and data columns")
    parser.add_argument("data", type=argparse.FileType(mode="r", encoding="utf-8-sig"),
                        nargs="?", default=sys.stdin,
                        help="Flat data file as CSV"
                        )
    parser.add_argument("output", type=argparse.FileType(mode="w"),
                        nargs="?", default=sys.stdout,
                        help="Json file representing restructured data")
    args = parser.parse_args()
    return args


def load_schema(schema_file: io.IOBase) -> dict[str, list[str]]:
    """Configuration options we expect:
       "labels" -> non-empty list of column headers
       "values" -> non-empty list of column headers
    """
    schema = json.load(schema_file)
    log.debug(f"Schema: \n{schema}")
    assert isinstance(schema, dict), f"Schema should be a dict with entries 'labels' and 'data'"
    return schema

nest = list[int] | dict[str, 'items']

def insert(values: list[int], path: list[str], structure: dict):
    """Insert as value as structure[p1][p2][...][key] where pi are elements of path"""
    log.debug(f"Inserting {values} on path {path} in {structure}")
    if len(path) == 1:
        key = path[0]
        structure[key] = values
        return
    initial = path[0]
    suffix = path[1:]
    if initial not in structure:
        structure[initial] = {}
    insert(values, suffix, structure[initial])


def coerce_by_guessing(values: list) -> object:
    """Best guess at interpretation of value fields.
    If a field contains only digits, we guess it is an integer.
    If a looks like a floating point number, we coerce it to float.
    Otherwise we leave it as a string.
    If the list has only a single item, we unpack it.
    """
    def guess_value(field: str) -> object:
        try:
            return int(field)
        except Exception: pass
        try:
            return float(field)
        except Exception: pass
        return field
    coerced = [ guess_value(field) for field in values]
    if len(coerced) == 1:
        return coerced[0]
    else:
        return coerced



def unflatten(flat: io.IOBase, schema: dict[str, list[str]]) -> dict:
    """Reshape in_csv CSV file into tree structure represented as items of dictionaries.
    Rows that go in the tree are those with content in the data columns.
    Each label column is "sticky", i.e., when a column is empty, we assume it is a duplicate
    of the last non-empty value in that column, whether or not the previous row had
    data values.
    """
    reader = csv.DictReader(flat)
    values = schema["values"]
    # Missing column labels could be because we are using a schema for
    # a table that has been summarized by aggregate.py.  Warn but continue.
    column_labels = reader.fieldnames
    labels = []
    for label in schema["labels"]:
        if label in column_labels:
            labels.append(label)
        else:
            log.warning(f"Missing column label '{label}' will be ignored")

    #
    structure = {}
    row_labels = ["NA" for label in labels]

    for record in reader:
        for i,label in enumerate(labels):
            if record[label]:  # Retain "sticky" values when field is empty
                row_labels[i] = record[label]
            log.debug(f"Labels effectively {row_labels}")
        value_fields = [record[field] for field in values]
        if value_fields[0]:
            leaf_value = coerce_by_guessing(value_fields)
            # This row has values to insert
            log.debug(f"Inserting {row_labels} -> {leaf_value}")
            insert(leaf_value, row_labels, structure)
    return structure



def main():
    args = cli()
    map = load_schema(args.schema)
    log.debug(f"Schema: {map}")
    structure = unflatten(args.data, map)
    # log.debug(f"Reshaped data: {json.dumps(structure, indent=3)}")
    print(json.dumps(structure, indent=3), file=args.output)


if __name__ == "__main__":
    main()
