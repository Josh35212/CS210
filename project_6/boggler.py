"""Boggler:  Boggle game solver. CS 210, Fall 2022.
Josh Gilliam
Credits: AI helped with debugging the solve function
"""
import doctest
import config
import sys
import board_view

# Possible search outcomes
NOPE = "Nope"       # Not a match, nor a prefix of a match
MATCH = "Match"     # Exact match to a valid word
PREFIX = "Prefix"   # Not an exact match, but a prefix (keep searching!)

# Special character in position that is
# already in use
IN_USE = "@"

# Max word length is 16, so we can just list all
# the point values.
#
#         0  1  2  3  4  5  6  7  8
POINTS = [0, 0, 0, 1, 1, 2, 3, 5, 11,
          11, 11, 11, 11, 11, 11, 11, 11 ]
#          9  10  11  12  13  14  15  16

def test_it():
    """A little extra work to keep text display from
    interfering with doctests.
    """
    saved_flag = config.TEXT_VIEW
    config.TEXT_VIEW = False
    doctest.testmod(verbose=True)
    config.TEXT_VIEW = saved_flag

def read_dict(path: str) -> list[str]:
    """Returns ordered list of valid, normalized words from dictionary.

    >>> read_dict("data/shortdict.txt")
    ['ALPHA', 'BED', 'BETA', 'DELTA', 'GAMMA', 'OMEGA']
    """
    words = []
    dict_file = open(path, "r", encoding="utf-8-sig")
    for line in dict_file:
        word = line.strip()
        if allowed(word):
            words.append(normalize(word))
    words.sort()
    return words

def allowed(s: str) -> bool:
    """Is s a legal Boggle word?

    >>> allowed("am")  ## Too short
    False

    >>> allowed("de novo")  ## Non-alphabetic
    False

    >>> allowed("about-face")  ## Non-alphabetic
    False
    """
    if len(s) >= config.MIN_WORD:
        return s.isalpha()
    return False

def normalize(s: str) -> str:
    """Canonical for strings in dictionary or on board
    >>> normalize("filter")
    'FILTER'
    """
    return s.upper()

def search(candidate: str, word_list: list[str]) -> str:
    """Determine whether candidate is a MATCH, a PREFIX of a match, or a big NOPE
    Note word list MUST be in sorted order.

    >>> search("ALPHA", ['ALPHA', 'BETA', 'GAMMA']) == MATCH
    True

    >>> search("BE", ['ALPHA', 'BETA', 'GAMMA']) == PREFIX
    True

    >>> search("FOX", ['ALPHA', 'BETA', 'GAMMA']) == NOPE
    True

    >>> search("ZZZZ", ['ALPHA', 'BETA', 'GAMMA']) == NOPE
    True
    """
    low = 0
    high = len(word_list) - 1
    candidate = candidate.upper()   

    while low <= high:
        mid = ((low + high) // 2)
        word = word_list[mid]
        if word == candidate: 
            return MATCH
        elif word < candidate:
            low = mid + 1
        elif word > candidate:
            high = mid - 1
    
    # Determine result if no MATCH found
    if low < len(word_list) and word_list[low].startswith(candidate):
        return PREFIX
    else:
        return NOPE

def get_board_letters() -> str:
    """Get a valid string to form a Boggle board
    from the user.  May produce diagnostic
    output and quit.
    """
    while True:
        board_string = input("Boggle board letters (or 'return' to exit)> ")
        if allowed(board_string) and len(board_string) == config.BOARD_SIZE:
            return normalize(board_string)
        elif len(board_string) == 0:
            print(f"OK, sorry it didn't work out")
            sys.exit(0)
        else:
            print(f'"{board_string}" is not a valid Boggle board')
            print(f'Please enter exactly {config.BOARD_SIZE} letters (or empty to quit)')

def unpack_board(letters: str, rows=config.N_ROWS) -> list[list[str]]:
    """Unpack a single string of characters into
    a square matrix of individual characters, N_ROWS x N_ROWS.

    >>> unpack_board("abcdefghi", rows=3)
    [['a', 'b', 'c'], ['d', 'e', 'f'], ['g', 'h', 'i']]

    >>> unpack_board("abcdefghijklmnop", rows=4)
    [['a', 'b', 'c', 'd'], ['e', 'f', 'g', 'h'], ['i', 'j', 'k', 'l'], ['m', 'n', 'o', 'p']]
    """
    board = []
    for i in range(rows):
        row = []
        for j in range(rows):
            row.append(letters[i * rows + j])
        board.append(row)
    return board

def boggle_solve(board: list[list[str]], words: list[str]) -> list[str]:
    """Find all the words that can be made by traversing
    the boggle board in all 8 directions.  Returns sorted list without
    duplicates.

    >>> board = unpack_board("PLXXMEXXXAXXSXXX", rows=4)
    >>> words = read_dict("data/dict.txt")
    >>> boggle_solve(board, words)
    ['AMP', 'AMPLE', 'AXE', 'AXLE', 'ELM', 'EXAM', 'LEA', 'MAX', 'PEA', 'PLEA', 'SAME', 'SAMPLE', 'SAX']
    """
    solutions = []

    def solve(row: int, col: int, prefix: str):
        """One solution step"""
        if row < 0 or row >= config.N_ROWS or col < 0 or col >= config.N_COLS:
            return
        
        if board[row][col] == IN_USE:
            return  
        
        letter = board[row][col]
        new_prefix = prefix + letter
        status = search(new_prefix, words)

        if status == NOPE:
            return
        
        board[row][col] = IN_USE  # Prevent reusing 
        board_view.mark_occupied(row, col)

        if status == MATCH:
            solutions.append(new_prefix)
            board_view.celebrate(new_prefix)
        
        if status == MATCH or status == PREFIX:
            # Try all 8 directions
            for d_row in [-1, 0, 1]:
                for d_col in [-1, 0, 1]:
                    # Skip the case of current position
                    if d_row == 0 and d_col == 0:
                        continue
                    solve(row + d_row, col + d_col, new_prefix)
        
        # Restore
        board[row][col] = letter
        board_view.mark_unoccupied(row, col)

    # Look for solutions starting from each board position
    for row_i in range(config.N_ROWS):
        for col_i in range(config.N_COLS):
            solve(row_i, col_i, "")

    # Return solutions without duplicates, in sorted order
    solutions = list(set(solutions))
    return sorted(solutions)

def word_score(word: str) -> int:
    """Standard point value in Boggle"""
    assert len(word) <= 16
    return POINTS[len(word)]

def score(solutions: list[str]) -> int:
    """Sum of scores for each solution

    >>> score(["ALPHA", "BETA", "ABSENTMINDED"])
    14
    """
    total = 0
    for word in solutions:
        length = len(word)
        if length > 16:
            length = 16
        total += POINTS[length]
    return total


def main():
    words = read_dict(config.DICT_PATH)
    board_string = get_board_letters()
    board_string = normalize(board_string)
    board = unpack_board(board_string)
    board_view.display(board)
    solutions = boggle_solve(board, words)
    print(solutions)
    print(f"{score(solutions)} points")
    board_view.prompt_to_close()

if __name__ == "__main__":
    main()