"""
Practice 3: Greeting with a default value
If the caller does not give `greeting`, Python uses "Hello".
"""

def greet(name, greeting="Hello"):
    return greeting + ", " + name + "!"


print(greet("Ravi"))
print(greet("Priya", "Good morning"))
print(greet(greeting="Welcome", name="Amit"))   # keyword arguments

# Try it yourself:
#   Add a third parameter `city` with the default value "Kolkata"
