"""
TOPIC 1: FUNCTIONS  (15 minutes)
================================
A function is a named, reusable block of code that TAKES input (parameters)
and usually GIVES BACK a result using `return`.

Why use functions?
  - Avoid repeating code (DRY: Don't Repeat Yourself)
  - Break big problems into small, testable pieces
  - Give a meaningful name to a piece of logic

Run this file:  python 01_functions.py
"""

# ---------------------------------------------------------------
# 1. Defining and calling a function            (~2 min)
# ---------------------------------------------------------------
# Syntax:
#   def function_name(parameters):
#       body
#       return value

def square(number):
    """Return the square of a number."""   # <- docstring: describes the function
    return number * number


result = square(5)          # calling the function; 5 is the ARGUMENT
print("1. square(5) =", result)
print("   square(12) =", square(12))


# ---------------------------------------------------------------
# 2. Multiple parameters                        (~2 min)
# ---------------------------------------------------------------
def add(a, b):
    return a + b


def calculate_total(price, quantity):
    return price * quantity


print("\n2. add(10, 20) =", add(10, 20))
print("   Total bill =", calculate_total(250, 3))


# ---------------------------------------------------------------
# 3. Default parameter values                   (~2 min)
# ---------------------------------------------------------------
# If the caller does not pass a value, the default is used.

def greet(name, message="Welcome to Anudip!"):
    return f"Hello {name}, {message}"


print("\n3.", greet("Ravi"))
print("  ", greet("Priya", "Good morning!"))


# ---------------------------------------------------------------
# 4. Keyword arguments                          (~1 min)
# ---------------------------------------------------------------
# You can pass arguments by NAME, so order does not matter.

def student_info(name, age, city):
    return f"{name} is {age} years old and lives in {city}"


print("\n4.", student_info(age=20, city="Kolkata", name="Amit"))


# ---------------------------------------------------------------
# 5. Returning multiple values                  (~2 min)
# ---------------------------------------------------------------
# Python returns them as a tuple, which we can "unpack".

def min_max_avg(numbers):
    smallest = min(numbers)
    largest = max(numbers)
    average = sum(numbers) / len(numbers)
    return smallest, largest, average


marks = [78, 92, 65, 88, 71]
low, high, avg = min_max_avg(marks)
print(f"\n5. Lowest: {low}, Highest: {high}, Average: {avg:.2f}")


# ---------------------------------------------------------------
# 6. Functions with logic (if / loops inside)   (~2 min)
# ---------------------------------------------------------------
def get_grade(score):
    if score >= 90:
        return "A"
    elif score >= 75:
        return "B"
    elif score >= 60:
        return "C"
    else:
        return "F"


def is_even(n):
    return n % 2 == 0          # returns True or False


print("\n6. Grades:")
for m in marks:
    print(f"   {m} -> {get_grade(m)}")
print("   Is 10 even?", is_even(10))


# ---------------------------------------------------------------
# 7. Variable scope: local vs global            (~2 min)
# ---------------------------------------------------------------
# Variables created INSIDE a function exist only inside it (local).

company = "Anudip"            # global variable

def show_scope():
    trainee = "Neha"          # local variable
    print(f"\n7. Inside function: {trainee} works at {company}")

show_scope()
# print(trainee)   # <- Uncomment: NameError! 'trainee' is local to show_scope


# ---------------------------------------------------------------
# 8. Functions calling other functions          (~1 min)
# ---------------------------------------------------------------
def area_of_circle(radius):
    return 3.14159 * square(radius)    # re-using square() from above


print("\n8. Area of circle with radius 7 =", round(area_of_circle(7), 2))


# ---------------------------------------------------------------
# PRACTICE EXERCISES (try in class, ~1 min to explain)
# ---------------------------------------------------------------
# 1. Write celsius_to_fahrenheit(c) that returns (c * 9/5) + 32
# 2. Write is_vowel(ch) that returns True if ch is a vowel
# 3. Write factorial(n) using a loop and return the result
# 4. Write simple_interest(p, r, t=1) with a default time of 1 year
