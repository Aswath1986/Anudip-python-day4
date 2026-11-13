"""
Practice 2: Multiplication table
A procedure with a loop inside.
"""

def print_table(number):
    print("Table of", number)
    for i in range(1, 11):
        print(number, "x", i, "=", number * i)


print_table(5)

# Try it yourself:
#   Add a second parameter `upto` so print_table(5, 20) goes up to 20
