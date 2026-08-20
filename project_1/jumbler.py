"""jumbler: List dictionary words that match an anagram.
2025-10-5 by Josh Gilliam

Credits: 
Chat-GBT: helped write/explain lines 30-32 
"""

#DICT = "shortdict.txt"
DICT = "dict.txt"

def main(): 
    anagram = input("Anagram to find: ")
    find(anagram)

def normalize(word: str) -> list[str]:
    """Returns a list of characters that is canonical for anagrams.
    
    >>> normalize("gamma") == normalize("magam")
    True
    
    >>> normalize("MAGAM") == normalize("gamma")
    True
    
    >>> normalize("KAWEA") == normalize("awake")
    True
    
    >>> normalize("KAWEA") == normalize("gamma")
    False
    """
    word = word.lower()
    letters = sorted(word)
    return letters

def find(anagram: str):
    """Print words in DICT that match anagram.
  
    >>> find("AgEmo")
    omega
  
    >>> find("nosuchword")

    >>> find("alpha")
    alpha

    >>> find("KAWEA")
    awake
  
    """
    dict_file = open(DICT, "r", encoding="utf-8-sig")
    for line in dict_file:
        word = line.strip()
        if normalize(word) == normalize(anagram):
            print(word)

if __name__ == "__main__":
    main()
    #import doctest
    #doctest.testmod()
    #print("Doctests complete!")