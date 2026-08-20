"""Enrollment analysis:  Summary report of majors enrolled in a class.
CS 210 project, Fall 2025.
Author:  Josh Gilliam
Credits: Copilot helped guide me through creating the items_v_k function + doctest.
"""

import doctest
import csv

def read_csv_column(path: str, field: str) -> list[str]:
    """Read one column from a CSV file with headers into a list of strings.

    >>> read_csv_column("data/test_roster.csv", "Major")
    ['DSCI', 'CIS', 'BADM', 'BIC', 'CIS', 'GSS']
    """
    major_codes = []
    with open(path, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if field in row:
                major_codes.append(row[field])
    return major_codes

def counts(column: list[str]) -> dict[str, int]:
    """Returns a dict with counts of elements in column.

    >>> counts(["dog", "cat", "cat", "rabbit", "dog"])
    {'dog': 2, 'cat': 2, 'rabbit': 1}
    """
    element_counts = {}
    for el in column:
        if el in element_counts:
            element_counts[el] += 1
        else:
            element_counts[el] = 1
    return element_counts

def read_csv_dict(path: str, key_field: str, value_field: str) -> dict[str, str]:
    """Read a CSV with column headers into a dict with selected
    key and value fields.

    >>> read_csv_dict("data/test_programs.csv", key_field="Code", value_field="Program Name")
    {'ABAO': 'Applied Behavior Analysis', 'ACTG': 'Accounting', 'ADBR': 'Advertising and Brand Responsibility'}
    """
    program_names = {}
    with open(path, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            program_names[row[key_field]] = row[value_field]
    return program_names

def items_v_k(d: dict) -> list[tuple]:
    """Convert a dictionary into a list of (value, key) tuples.
    
    >>> items_v_k({'CS': 20, 'MATH': 15})
    [(20, 'CS'), (15, 'MATH')]
    """
    result = []
    for key, value in d.items():
        # Flips the order so that value comes first
        result.append((value, key))
    return result


def main():
    doctest.testmod()
    majors = read_csv_column("data/roster_25F_selected.csv", "Major")
    counts_by_major = counts(majors)
    program_names = read_csv_dict("data/programs_25F.csv", "Code", "Program Name")
    by_count = items_v_k(counts_by_major)  # "Refactored" into a function
    by_count.sort(reverse=True)  # From largest to smallest
    for count, code in by_count:
        program = program_names[code]
        print(count, program)

if __name__ == "__main__":
    main()