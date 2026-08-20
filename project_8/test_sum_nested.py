"""Test cases for summing nested structures,
including nested lists like [[1, 2], [[3, 4], 5]]
and nested dicts like
  { "mammals": { "monotremes": 12, "marsupials": 8, "placentals": 4 }}
"""

import unittest
from splitter import deep_sum

class TestSumNested(unittest.TestCase):
    """Case breakdown:
    1. An individual integer (base case)
    2. An individual (string, int) pair (base case)
    3. An individual (string, items) pair (recursive case, sum items)
    4. A list  (recursive case, combine sums)
    5. A dict (recursive case, combine dicts)
    """
    def test_individual_int(self):
        self.assertEqual(deep_sum(42), 42)

    def test_base_pair(self):
        self.assertEqual(deep_sum(("chickens", 12)), 12)

    def test_nested_pair(self):
        self.assertEqual(deep_sum(("colors", [3, 4, 5])), 12)

    def test_list(self):
        self.assertEqual(deep_sum([1, 2, 3, 4]), 10)
        self.assertEqual(deep_sum([("red", 3), ("green", 4), ("blue", 2)]), 9)
        self.assertEqual(deep_sum([{"red": 3, "green": 4, "blue": 5},
                                   {"chickens": 6, "colors": [1, 2, 3]}]), 24)

    def test_dict(self):
        self.assertEqual(deep_sum({"red": 3, "green": 4, "blue":7}), 14)
        self.assertEqual(deep_sum({"red": 3, "green":[ 1, 2, 3]}), 9)

    def test_recursive_mixed(self):
        self.assertEqual(deep_sum([{"red": 3, "green": 4, "blue": 5},
                                   {"chickens": 6, "colors": [1, 2, 3]}]), 24)

    def test_majors(self):
        majors = {
            "Exploring": 11,
            "SCDS": {
                "Computer Science": 79,
                "Data Science": 33,
                "MACS": 11
            },
            "Sciences": {
                "Psych": 8,
                "Physics": 5,
                "Multi": 4,
                "Math": 4,
                "Biology": 3,
                "Neuro": 2,
                "Marine": 1
            },
            "Bus": {"Business": 5, "Pre-Business": 10, "Acct": 1},
            "Soc": {"Poli-Sci": 3, "Econ": 2, "SDS": 1, "Ling": 2},
            "Art": [1, 1, 1],
            "Other": 3
        }
        self.assertEqual(deep_sum(majors), 191)


if __name__ == '__main__':
    unittest.main()