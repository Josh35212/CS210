"""Unit tests for splitter.py"""

import unittest
import time  # To distinguish linear-time from quadratic time solutions
from mapper import bisect

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

def show_pivot(i: int, li: list[int]) -> str:
    """String showing i"""
    return f"{sum(li)}= {sum(li[:i])}+{sum(li[i:])}  {li} => {li[:i]}|{li[i:]}"

class Tests(unittest.TestCase):
    def test_pair(self):
        """Special case for list of length 2"""
        li = [42, 42]
        parts = bisect(li)
        self.assertEqual(parts, ([42], [42]))

    def test_pair_skewed_right(self):
        li = [1, 2]
        parts = bisect(li)
        self.assertEqual(parts, ([1], [2]))
        li = [1,10]
        parts = bisect(li)
        self.assertEqual(parts, ([1], [10]))

    def test_pair_skewed_left(self):
        li = [2,1]
        parts = bisect(li)
        self.assertEqual(parts, ([2], [1]))
        li = [10.0, 1.0]
        parts = bisect(li)
        self.assertEqual(parts, ([10.0], [1.0]))

    def test_simple_units(self):
        li = [1, 1, 1, 1, 1, 1]
        left, right = bisect(li)
        self.assertEqual(left, [1, 1, 1])
        self.assertEqual(right, [1, 1, 1])

    def test_extreme_left(self):
        li = [12, 1, 1, 1]
        left, right = bisect(li)
        self.assertEqual(left, [12])
        self.assertEqual(right, [1, 1, 1])

    def test_extreme_right(self):
        li = [1, 1, 1, 12]
        parts = bisect(li)
        self.assertEqual(parts, ([1, 1, 1], [12]))

    def test_balanced_left(self):
        li = [3, 1, 1, 1]
        parts = bisect(li)
        self.assertEqual(parts, ([3], [1, 1, 1]))

    def test_balanced_right(self):
        li = [1, 1, 1, 3]
        parts = bisect(li)
        self.assertEqual(parts, ([1, 1, 1], [3]))

    def test_growing(self):
        li = [1, 2, 3, 4, 5, 6]  # total 21, target is 10, so [1..4] and [5..6]
        parts = bisect(li)
        self.assertEqual(parts, ([1, 2, 3, 4], [5, 6]))

    def test_shrinking(self):
        li = [6, 5, 4, 3, 2, 1]  # total 21, target is 10, so [6,5] and [4,3,2,1]
        parts = bisect(li)
        self.assertEqual(parts,  ([6, 5], [4, 3, 2, 1]))

    def test_fast_enough(self):
        """Note: 50_000 entries is chosen empirically to be enough to
        take about 20 to 30 seconds on a 2020 M1 macbook pro
        using the quadratic algorithm, but around .01 seconds with the
        linear time algorithm.
        It will be annoying to students with slow computers, but
        I want to be sure this test can distinguish between linear time and quadratic
        time even on a fast "gaming" desktop computer for at least a few years.
        """
        a_lot = 50_000
        li = [1] * a_lot   # A lot of 1s
        li.append(a_lot)   # Make it split off just the last element
        begin_time = time.time()
        parts = bisect(li)
        end_time = time.time()
        elapsed = end_time - begin_time
        log.debug(f"Splitting {a_lot+1} items in {elapsed} seconds")
        # A linear time solution should finish in less than a second
        self.assertLess(elapsed, 1.0)


if __name__ == "__main__":
    unittest.main()


