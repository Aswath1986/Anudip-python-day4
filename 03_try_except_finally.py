"""
TOPIC 3: EXCEPTION HANDLING — try / except / else / finally  (15 minutes)
=========================================================================
An EXCEPTION is an error that happens while the program is running.
If we don't handle it, the program CRASHES.

    try:      code that might fail
    except:   what to do IF it fails
    else:     runs ONLY IF nothing failed
    finally:  ALWAYS runs (success or failure) — used for clean-up

Run this file:  python 03_try_except_finally.py
"""

# ---------------------------------------------------------------
# 1. What happens WITHOUT exception handling?   (~1 min)
# ---------------------------------------------------------------
# Uncomment the next line and run — the program stops with a traceback:
# print(10 / 0)          # ZeroDivisionError: division by zero
print("1. Common errors: ZeroDivisionError, ValueError, TypeError,")
print("   IndexError, KeyError, FileNotFoundError")


# ---------------------------------------------------------------
# 2. Basic try / except                          (~2 min)
# ---------------------------------------------------------------
print("\n2. Basic try/except:")
try:
    result = 10 / 0
    print("   This line never runs")
except ZeroDivisionError:
    print("   Oops! You cannot divide by zero.")

print("   ...and the program continues normally!")


# ---------------------------------------------------------------
# 3. Catching different exceptions separately   (~3 min)
# ---------------------------------------------------------------
def safe_divide(a, b):
    try:
        return int(a) / int(b)
    except ZeroDivisionError:
        print(f"   Error: cannot divide {a} by zero")
    except ValueError:
        print(f"   Error: '{a}' or '{b}' is not a valid number")
    except TypeError:
        print("   Error: wrong data type given")
    return None


print("\n3. Multiple except blocks:")
print("   safe_divide(20, 4) =", safe_divide(20, 4))
safe_divide(20, 0)
safe_divide("abc", 5)
safe_divide(None, 5)


# ---------------------------------------------------------------
# 4. Getting the error message with `as`         (~2 min)
# ---------------------------------------------------------------
print("\n4. Reading the error message:")
numbers = [10, 20, 30]
try:
    print(numbers[5])
except IndexError as e:
    print("   Caught IndexError ->", e)

student = {"name": "Ravi", "age": 20}
try:
    print(student["city"])
except KeyError as e:
    print("   Caught KeyError -> missing key", e)

# Catch-all (use carefully — put it LAST):
try:
    value = int("12.5")
except Exception as e:
    print(f"   Caught {type(e).__name__} -> {e}")


# ---------------------------------------------------------------
# 5. else block                                  (~2 min)
# ---------------------------------------------------------------
print("\n5. try / except / else:")

def convert_age(text):
    try:
        age = int(text)
    except ValueError:
        print(f"   '{text}' is not a valid age")
    else:
        # runs only when NO exception happened
        print(f"   Valid age entered: {age}")

convert_age("25")
convert_age("twenty")


# ---------------------------------------------------------------
# 6. finally block — ALWAYS runs                 (~3 min)
# ---------------------------------------------------------------
print("\n6. try / except / else / finally:")

def process_payment(amount):
    print(f"   Processing payment of {amount}...")
    try:
        amount = float(amount)
        if amount <= 0:
            raise ValueError("amount must be positive")   # raise our own error
    except ValueError as e:
        print("   ❌ Payment failed:", e)
    else:
        print("   ✅ Payment successful!")
    finally:
        print("   🔒 Closing payment session (finally always runs)\n")

process_payment(500)
process_payment(-50)
process_payment("abc")

# Real-world uses of finally: closing files, closing database
# connections, releasing resources, logging "done".


# ---------------------------------------------------------------
# 7. Raising your own exceptions                 (~1 min)
# ---------------------------------------------------------------
def set_marks(marks):
    if not 0 <= marks <= 100:
        raise ValueError(f"Marks must be between 0 and 100, got {marks}")
    return marks

print("7. Raising exceptions:")
for m in (85, 150):
    try:
        print("   Marks set to", set_marks(m))
    except ValueError as e:
        print("   Error:", e)


# ---------------------------------------------------------------
# 8. Real-life pattern: keep asking until valid input
# ---------------------------------------------------------------
# (Demo live in class — uncomment to try interactively)
#
# while True:
#     try:
#         n = int(input("Enter a number: "))
#         break
#     except ValueError:
#         print("That's not a number, try again!")
# print("You entered", n)


# ---------------------------------------------------------------
# PRACTICE EXERCISES (~1 min to explain)
# ---------------------------------------------------------------
# 1. Ask the user for two numbers and divide them; handle both
#    ValueError and ZeroDivisionError.
# 2. Write get_item(lst, index) that returns the item or prints a
#    friendly message on IndexError.
# 3. Add a finally block that prints "Calculation finished" every time.
