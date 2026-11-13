"""
Practice 3: List and dictionary errors
IndexError -> the position does not exist in the list
KeyError   -> the key does not exist in the dictionary
"""

fruits = ["apple", "banana", "mango"]
prices = {"apple": 120, "banana": 40}

try:
    print("Fruit at position 5:", fruits[5])
except IndexError:
    print("There is no fruit at position 5")

try:
    print("Price of mango:", prices["mango"])
except KeyError:
    print("Mango has no price yet")

# Try it yourself:
#   Change 5 to 1, and "mango" to "apple". What prints now?
