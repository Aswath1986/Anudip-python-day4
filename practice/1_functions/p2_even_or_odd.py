"""
Practice 2: Even or odd
A function can return True or False.
"""

def is_even(number):
    return number % 2 == 0


for n in [4, 7, 10, 13]:
    if is_even(n):
        print(n, "is even")
    else:
        print(n, "is odd")

# Try it yourself:
#   Write is_positive(number) that returns True when number > 0
