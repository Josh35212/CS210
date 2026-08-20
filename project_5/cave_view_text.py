"""A graphical display of a cave represented as a rectangular grid of characters"""




CAVE_COPY: list[list[str]] = []

DIGITS = "1234567890"  # Used for labeling chambers
COLOR_IDX = 0

def stash(cavern: list[list[str]]):
    """Save initial cavern into CAVE_COPY"""
    global CAVE_COPY
    CAVE_COPY = []
    for row in cavern:
        CAVE_COPY.append(row.copy())

def display(cavern: list[list[str]], width: int, height: int):
    # Stash copy that we will manipulate
    stash(cavern)
    # Show it
    show(CAVE_COPY)

def show(cavern: list[list[str]]):
    """For now, like printed version but with spaces.
    """
    print()
    for row in CAVE_COPY:
        print(" ".join(row))

def redisplay(cavern: list[list[str]]):
    show(CAVE_COPY)

def change_water():
    """Switch to a new color of water;
    not for text.
    """
    global COLOR_IDX
    COLOR_IDX = (COLOR_IDX + 1) % len(DIGITS)

def fill_cell(row: int, col: int):
    """Fill display of cave[row][col] with current colored water"""
    global CAVE_COPY
    assert row >= 0 and col >= 0, "Can't fill cell in empty cave"
    assert 0 <= row < len(CAVE_COPY)
    assert 0 <= col < len(CAVE_COPY[0])
    CAVE_COPY[row][col] = DIGITS[COLOR_IDX]












