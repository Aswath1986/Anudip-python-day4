"""
Practice 4: Largest of three numbers
A function can use if / elif / else before it returns.
"""

def largest(a, b, c):
    if a >= b and a >= c:
        return a
    elif b >= c:
        return b
    else:
        return c


print("Largest of 4, 9, 2   :", largest(4, 9, 2))
print("Largest of 15, 3, 8  :", largest(15, 3, 8))
print("Largest of 1, 1, 7   :", largest(1, 1, 7))

# Try it yourself:
#   Write smallest(a, b, c)
