"""Sort JSON-structured nested quantitative data from largest to smallest.
A items may be
    - a list of nests  (reorder from largest to smallest sum)
    - a dict of name: items associations  (reorder from largest to smallest items)
    - a tuple (name, items) (base case, already in order; note this appears when decomposing dicts)
    - a real number (base case, already in order)

There is a fair amount of repeated code here from mapper.py. Factoring it out would be a good student project.
"""
import doctest

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

    if isinstance(nest, Real):
        return nest
    elif isinstance(nest, list):
        return sum(deep_sum(item) for item in nest)
    elif isinstance(nest, tuple):
        label, value = nest
        return deep_sum(value)
    else:
        assert False, f"Unanticipated type in deep_sum: {nest}"


def ordered(nest: Nest) -> Nest:
    """Reorder from largest to smallest.
    >>> ordered(12)
    12
    >>> ordered([12, 13, 10])
    [13, 12, 10]
    >>> ordered([[7, 3], [1, [2, 7]], 10])
    [[7, 3], [[7, 2], 1], 10]
    >>> ordered([[1.0, 2.0], [3, 4]])
    [[4, 3], [2.0, 1.0]]
    >>> ordered({ "Cake": { "Chocolate": 4, "Carrot": 10 }, "Ice Cream": 15 })
    {'Ice Cream': 15, 'Cake': { 'Carrot': 10, 'Chocolate': 4 }}
    """
    # Base cases: Already in order
    if isinstance(nest, Real) or isinstance(nest, tuple):
        return nest

    if isinstance(nest, list):
        elements = [ordered(el) for el in nest]
        return sorted(elements, key= lambda el: deep_sum(el), reverse=True)

    if isinstance(nest, dict):
        # Reorder each element
        pairs = ((k, ordered(v)) for (k, v) in nest.items())
        # Build dict from sorted list of reordered k, v pairs
        in_order = sorted(pairs, key=lambda pair: deep_sum(pair[1]), reverse=True)
        return { k: v for (k, v) in in_order }

    # Should be exhaustive if items is well-formed
    assert False, f"Unanticipated type in deep_sum: {nest}"


if __name__ == '__main__':
    doctest.testmod()