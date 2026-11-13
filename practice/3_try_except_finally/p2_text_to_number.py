"""
Practice 2: Text to number
int("abc") gives a ValueError. We catch it.
"""

values = ["25", "hello", "100", "12.5"]

for text in values:
    try:
        number = int(text)
        print(text, "-> number", number)
    except ValueError:
        print(text, "-> not a whole number")

# Try it yourself:
#   Use float(text) instead of int(text). Which values work now?
