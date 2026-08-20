"""Command-line driver for nest_sort.py, sorts a JSON-encoded items."""

import argparse
import json
import sys

import nest_sort

def main():
    parser = argparse.ArgumentParser(description='Sort JSON items by items')
    parser.add_argument('json_in', help='JSON file to sort',
                        type=argparse.FileType('r', encoding='utf-8'), nargs='?', default=sys.stdin)
    parser.add_argument('json_out', help='Output file',
                        type=argparse.FileType('w', encoding='utf-8'), nargs='?', default=sys.stdout)

    args = parser.parse_args()
    nest = json.load(args.json_in)
    reordered = nest_sort.ordered(nest)
    json.dump(reordered, args.json_out, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()

