""" Construct a treemap.
Author: Josh Gilliam
Credits: Received help from ChatGPT.
"""

# Standard Python library modules
import logging
import doctest

# Project modules, provided
import geometry
import display

# Enable logging with log.debug(msg), log.info(msg), etc.
logging.basicConfig()
log = logging.getLogger(__name__)  # Log messages will look like "DEBUG:mapper:msg"
log.setLevel(logging.DEBUG)   # Change to logging.INFO to suppress debugging messages

# Layout works with integers, floating point numbers, or a mix of the two.
Real = int | float    # Named type for use in type annotations
Nest = Real | list['Nest'] | dict[ str, 'Nest'] | tuple[str, 'Nest']

def deep_sum(nest: Nest) -> Real:
    """Returns the total of all numbers in the Nest.

    >>> deep_sum(12)
    12
    >>> deep_sum([12, 13, 10])
    35
    >>> deep_sum([[7, 3], [1, [2, 7]], 10])
    30
    >>> deep_sum([[1.0, 2.0], [3, 4]])
    10.0
    >>> deep_sum({ "Cake": { "Chocolate": 10, "Carrot": 4 }, "Ice Cream": 15 })
    29
    """
    if isinstance(nest, dict):
        nest = list(nest.items())

    if isinstance(nest, (int, float)):
        return nest
    
    if isinstance(nest, tuple):
        assert len(nest) == 2
        key, value = nest
        return deep_sum(value)

    if isinstance(nest, list):
        total = 0
        for item in nest:
            total += deep_sum(item)
        return total
    
    else: 
        assert False, f"Unanticipated type in deep_sum: {nest}"

def badness(target: Real, candidate: Real) -> Real: 
    """How far is the candidate from the target?"""
    return abs(candidate - target)

def bisect(li: Nest) -> tuple[Nest, Nest]:
    """Returns (prefix, suffix) such that prefix+suffix == items
    and abs(sum(prefix) - sum(suffix)) is minimal.
    Breaks tie in favor of earlier split, e.g., bisect([1,5,1]) == ([1], [5, 1]).
    Requires len(items) >= 2, and all elements of items positive.

    >>> bisect([1, 1, 2])  # Perfect balance
    ([1, 1], [2])
    >>> bisect([2, 1, 1])  # Perfect balance
    ([2], [1, 1])
    >>> bisect([1, 2, 1])  # Equally bad either way; split before pivot
    ([1], [2, 1])
    >>> bisect([6, 5, 4, 3, 2, 1])  # Must include element at split
    ([6, 5], [4, 3, 2, 1])
    >>> bisect([1, 2, 3, 4, 5])
    ([1, 2, 3], [4, 5])
    >>> bisect([1, 1, [1, 1]])
    ([1, 1], [[1, 1]])
    >>> bisect([[3, 3], 5, [2, 2], [1, 1, 1]])
    ([[3, 3], 5], [[2, 2], [1, 1, 1]])
    """
    if isinstance(li, dict):
        li = list(li.items())

    assert isinstance(li, list), f"bisect is only for lists, can't split {li}"
    assert len(li) >= 2, f"Cannot bisect {li}; length must be at least 2"
    log.debug(f"Bisecting {li}")
    target = deep_sum(li) / 2
    best_index = 0
    best_badness = badness(target, 0)
    new_sum = 0

    for i in range(len(li) + 1):
        if i > 0:
            new_sum += deep_sum(li[i - 1])
        current_badness = badness(target, new_sum)
        if current_badness < best_badness:
            best_index = i
            best_badness = current_badness
    return li[:best_index], li[best_index:]

def layout(items: Nest, rect: geometry.Rect):
    """Lay elements of items out in rectangle.
    Recursively lays out a nested list of integers
    """
    if isinstance(items, (int, float)):
        display.draw_tile(rect, str(items))
        return
    
    elif isinstance(items, dict):
        items = list(items.items())
        layout(items, rect)
        return
    
    elif isinstance(items, tuple):
        key, value = items
        if isinstance(value, (int, float)):
            display.draw_tile(rect, key, value)
            return
        display.begin_group(rect, key, deep_sum(value))
        layout(value, rect)
        display.end_group()
        return

    elif isinstance(items, list):
        if len(items) == 0:
            return
        
        if len(items) == 1:
            layout(items[0], rect)
            return

        left, right = bisect(items)
        total_left = deep_sum(left)
        total_right = deep_sum(right)

        proportion = total_left / (total_left + total_right)
        left_rect, right_rect = rect.split(proportion)

        layout(left, left_rect)
        layout(right, right_rect)    
        return
    
    else:    
        assert False, f"What have we here? {items}"

def treemap(values: list[Real], width: int, height: int):
    """Create treemap of values in width x height pixel display
    in Tk interface and in SVG file written to treemap.svg.
    """
    display.init(width, height)
    area = geometry.Rect(geometry.Point(0, 0),
                         geometry.Point(width, height))
    layout(values, area)
    display.wait_close()


if __name__ == "__main__":
    doctest.testmod()