"""
Practice 3: Star pattern
A procedure that prints a triangle of stars.
"""

def print_triangle(rows):
    for i in range(1, rows + 1):
        print("*" * i)


print_triangle(5)

# Try it yourself:
#   Write print_square(size) that prints a square of stars
