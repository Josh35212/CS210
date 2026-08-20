"""Summarize a path in a map, using the standard Ramer-Douglas-Peucher (aka Duda-Hart)
split-and-merge algorithm.
Author: Josh Gilliam
Credits: TBD
"""

import csv
import doctest
import geometry
import map_view
import config
import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

def read_points(path: str) -> list[tuple[float, float]]:
    result = []
    with open(path, 'r', newline='') as file:
        reader = csv.reader(file)
        next(reader) # skip first row with column names
        for row in reader:
            easting = float(row[0])
            northing = float(row[1])
            result.append((easting, northing))
    return result

def summarize(points: list[tuple[float, float]],
              tolerance: int = config.TOLERANCE_METERS,
              ) -> list[tuple[float, float]]:
    """
     >>> path = [(0,0), (1,1), (2,2), (2,3), (2,4), (3,4), (4,4)]
     >>> expect = [(0,0), (2,2), (2,4), (4,4)]
     >>> simple = summarize(path, tolerance=0.5)
     >>> simple == expect
     True
    """
    summary: list[tuple[float, float]] = [points[0]]
    epsilon = float(tolerance * tolerance)

    def simplify(start: int, end: int):
        """Add necessary points in (start, end] to summary."""
        # find which point between start and end is furthest from straight line
        # initialize that furthest point as index of furthest 
        # if the deviation of that furthest point <= epsilon(the tollerance):
            # summary.append(points[end])
            # return
        # else:
            # simplify(start, furthest)
            # simplify(furthest, end)
        if end - start > 2:  
            map_view.scratch(points[start], points[end])

        max_deviation = 0.0
        furthest = None
        for i in range(start + 1, end):
            deviation = geometry.deviation_sq(points[start], points[end], points[i])
            if deviation > max_deviation:
                max_deviation = deviation
                furthest = i
        if max_deviation <= epsilon:
            summary.append(points[end])
            map_view.plot_to(points[end])
            return
        else:
            simplify(start, furthest)
            simplify(furthest, end) 
    
    simplify(0, len(points)-1)
    map_view.clean_scratches()
    return summary


def main():
    points = read_points(config.UTM_CSV)
    print(f"{len(points)} raw points")
    summary = summarize(points, config.TOLERANCE_METERS)
    print(f"{len(summary)} points in summary")
    map_view.init()
    for point in summary:
        map_view.plot_to(point)
    map_view.wait_to_close()

if __name__ == "__main__":
    doctest.testmod()
    print("Tested")
    main()