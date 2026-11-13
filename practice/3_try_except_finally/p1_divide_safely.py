"""
Practice 1: Divide safely
Without try/except, dividing by zero crashes the program.
"""

def divide(a, b):
    try:
        print(a, "/", b, "=", a / b)
    except ZeroDivisionError:
        print(a, "/", b, "-> Cannot divide by zero!")


divide(10, 2)
divide(10, 0)
print("The program is still running.")

# Try it yourself:
#   Remove the try/except and run again. What happens?
