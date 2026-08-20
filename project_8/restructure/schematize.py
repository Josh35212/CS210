"""Structure a CSV data set as guided by a schema in JSON format.
Example:    python3 schematize.py data/sch-schema.json data/sch.csv
See README-structure.md for detail.
M Young, 2024-06-19
"""
import json
import csv
import argparse
import io

#Experiment: Regex matching as fallback
import re

import logging
import sys
from numbers import Number

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

def cli() -> object:
    """Command line interface"""
    parser = argparse.ArgumentParser("Structure CSV data guided by json schema")
    parser.add_argument("--key",
                        help="Optional: Key values appear in column with this header",
                        nargs="?", default=None)
    parser.add_argument("--value",
                        help="(Only if 'key' specified) Values appear in column with this header",
                        nargs="?", default=None)
    parser.add_argument("schema", type=argparse.FileType(mode="r", encoding="utf-8"),
                        help="Schema expressed as json; see README-structure.md for details")
    parser.add_argument("data", type=argparse.FileType(mode="r", encoding="utf-8"),
                        nargs="?", default=sys.stdin,
                        help="Flat data file as CSV with each line being string, int for category, quantity"
                        )
    parser.add_argument("output", type=argparse.FileType(mode="w"),
                        nargs="?", default=sys.stdout,
                        help="Json file representing restructured data")
    args = parser.parse_args()
    return args

def parse_schema(schema_file: io.IOBase) -> dict[str, list[str]]:
    """Construct map from category to ancestry chain from elements of schema
    expressed as json.
    """
    map = { }
    try:
        json_text = schema_file.read()
    except Exception as e:
        log.error(f"Failed to read schema from file {schema_file}")
        exit(1)
    try:
        schema = json.loads(json_text)
        log.debug(f"Schema: \n{schema}")
    except Exception as e:
        log.error(f"Failed to parse schema from file {schema_file}")
        exit(1)
    assert isinstance(schema, list), f"Schema should be a list of dictionaries"

    def build_chains(prefix: list[str], element):
        """Build chains from this element downward through structure"""
        log.debug(f"Tracing ancestor chain {prefix} through {element}")
        if isinstance(element, str):
            if element in map:
                log.warning(f"{element} appears as {prefix} and also as {map[element]}, ignoring latter")
            map[element] = prefix.copy()
            log.debug(f"Added {element}: {prefix} to map")
        elif isinstance(element, list):
            for item in element:
                build_chains(prefix, item)
        elif isinstance(element, dict):
            for group, part in element.items():
                prefix.append(group)
                build_chains(prefix, part)
                prefix.pop()
        else:
            assert False, f"Trouble in schema, encountered {element}"

    for root in schema:
        build_chains([], root)
    return map

def insert(key: str, value: int, path: list[str], structure: dict):
    """Insert as value as structure[p1][p2][...][key] where pi are elements of path"""
    log.debug(f"Inserting {key}:{value} on path {path} in {structure}")
    if len(path) == 0:
        structure[key] = value
        return
    initial = path[0]
    suffix = path[1:]
    if initial not in structure:
        structure[initial] = {}
    insert(key, value, suffix, structure[initial])

def to_number(s: str) -> Number:
    """Converts to integer if possible, float if necessary;
    throws error if neither is possible.
    """
    if s.isdecimal():
        return int(s)
    return float(s)   # Throws error if it doesn't work


def load_unlabeled(flat: io.IOBase) -> list[tuple[str, int]]:
    """Read the input CSV file WITHOUT headers, assuming
    first two fields are key and value.
    """
    reader = csv.reader(flat)
    pairs = []
    try:
        for record in reader:
            log.debug(f"Interpreting CSV line as {record}")
            key, value = record[:2]
            pairs.insert((key, to_number(value)))
    except Exception as e:
        raise ValueError(f"Could not interpret data row {record}")
    return pairs


def load_labeled(flat: io.IOBase, keys: str, values: str) -> list[tuple[str, int]]:
    """Read the key, value pairs from CSV file WITH headers"""
    reader = csv.DictReader(flat)
    pairs = []
    try:
        for record in reader:
            log.debug(f"Interpreting CSV line as {record}")
            key = record[keys]
            value_str = record[values]
            try:
                value = to_number(value_str)
            except:
                raise ValueError(f"Couldn't convert {value_str} in {values} field of {record}")
            pairs.append((key, value))
    except KeyError as e:
        raise ValueError(f"Missing column {keys} or {values}")
    return pairs


def reshape(pairs: list[tuple[str, int]], paths: dict[str, list[str]]) -> dict:
    """Reshape in_csv CSV file into tree structure represented as items of dictionaries."""
    structure = {}
    for key, value in pairs:
        if key in paths:
            path = paths[key]
        else:
            path = regex_fallback(key, paths)
        insert(key, int(value), path, structure)
    return structure

def regex_fallback(key: str, paths: dict[str, list[str]]) -> list[str]:
    """If we did not find an exact match, perhaps some of the
    schema is keyed by regular expressions.
    FIXME: This linear search of all keys is expensive.
    """
    for pattern, path in paths.items():
        if re.match(pattern, key):
            return path
    return []



def main():
    args = cli()
    map = parse_schema(args.schema)
    log.debug(f"Ancestry map: {map}")
    if args.key or args.value:
        assert args.key and args.value, "Specify both key and value columns or neither"
        pairs = load_labeled(args.data, args.key, args.value)
    else:
        pairs = load_unlabeled(args.data)
    structure = reshape(pairs, map)
    # log.debug(f"Reshaped data: {json.dumps(structure, indent=3)}")
    json.dump(structure, args.output, indent=3)

if __name__ == "__main__":
    main()
