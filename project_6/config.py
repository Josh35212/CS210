""""Configuration of Boggle player"""

# List of words to search for
DICT_PATH = "data/dict.txt"

# How big a board?  Rows = columns
N_ROWS = 4  # 3 for Boggle Junior, 4 for Classic Boggle
N_COLS = N_ROWS
BOARD_SIZE = N_COLS * N_ROWS

# Minimum acceptable length of a Boggle word
MIN_WORD = 3   # 3 is the rule for "classic" boggle

GRAPHIC_VIEW = True
TEXT_VIEW = True
# Text view verbosity
TEXT_VIEW_EACH_MOVE = False  # Show prefix at each letter
TEXT_VIEW_EACH_BACK = False  # Show prefix when backing up
TEXT_VIEW_EACH_WORD = True  # Show full board with selected word

GRAPHIC_VIEW_SIZE = 500

