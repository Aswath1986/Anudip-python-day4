"""
Practice 5: Function vs procedure
See the difference between RETURNING a value and PRINTING a value.
"""

def add_function(a, b):      # function: gives the answer back
    return a + b


def add_procedure(a, b):     # procedure: only shows the answer
    print("Sum is", a + b)


x = add_function(2, 3)
print("Function gave back :", x)
print("We can reuse it    :", x * 10)

y = add_procedure(2, 3)
print("Procedure gave back:", y)     # None - nothing came back

# Try it yourself:
#   Write multiply as a function AND as a procedure
