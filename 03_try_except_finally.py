
print("1. Common errors: ZeroDivisionError, ValueError, TypeError,")
print("   IndexError, KeyError, FileNotFoundError")


print("\n2. Basic try/except:")
try:
    division_result = 10 / 0
    print("   This line never runs")
except ZeroDivisionError:
    print("   Oops! You cannot divide by zero.")

print("   ...and the program continues normally!")


def safe_divide(first_number, second_number):
    try:
        return int(first_number) / int(second_number)
    except ZeroDivisionError:
        print(f"   Error: cannot divide {first_number} by zero")
    except ValueError:
        print(f"   Error: '{first_number}' or '{second_number}' is not a valid number")
    except TypeError:
        print("   Error: wrong data type given")

    return None


print("\n3. Multiple except blocks:")
print("   safe_divide(20, 4) =", safe_divide(20, 4))
safe_divide(20, 0)
safe_divide("abc", 5)
safe_divide(None, 5)


print("\n4. Reading the error message:")
number_list = [10, 20, 30]

try:
    print(number_list[5])
except IndexError as error:
    print("   Caught IndexError ->", error)


student_details = {"name": "Ravi", "age": 20}

try:
    print(student_details["city"])
except KeyError as error:
    print("   Caught KeyError -> missing key", error)


try:
    converted_value = int("12.5")
except Exception as error:
    print(f"   Caught {type(error).__name__} -> {error}")


print("\n5. try / except / else:")


def convert_age(age_text):
    try:
        student_age = int(age_text)
    except ValueError:
        print(f"   '{age_text}' is not a valid age")
    else:
        print(f"   Valid age entered: {student_age}")


convert_age("25")
convert_age("twenty")


print("\n6. try / except / else / finally:")


def process_payment(payment_amount):
    print(f"   Processing payment of {payment_amount}...")

    try:
        payment_amount = float(payment_amount)

        if payment_amount <= 0:
            raise ValueError("amount must be positive")

    except ValueError as error:
        print("   Payment failed:", error)

    else:
        print("   Payment successful!")

    finally:
        print("   Closing payment session (finally always runs)\n")


process_payment(500)
process_payment(-50)
process_payment("abc")


def set_marks(student_marks):
    if not 0 <= student_marks <= 100:
        raise ValueError(
            f"Marks must be between 0 and 100, got {student_marks}"
        )

    return student_marks


print("7. Raising exceptions:")

for mark in (85, 150):
    try:
        print("   Marks set to", set_marks(mark))
    except ValueError as error:
        print("   Error:", error)
