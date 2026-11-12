"""
TOPIC 2: PROCEDURES  (15 minutes)
=================================
A PROCEDURE is a function that PERFORMS AN ACTION (printing, updating a list,
writing a file...) but does NOT return a useful value.

    Function  -> computes and RETURNS a value      e.g. square(5) -> 25
    Procedure -> DOES something, returns nothing   e.g. print_report()

In Python both are written with `def`. A procedure without `return`
automatically returns `None`.

Run this file:  python 02_procedures.py
"""

# ---------------------------------------------------------------
# 1. A simple procedure                          (~2 min)
# ---------------------------------------------------------------
def print_line():
    print("-" * 40)


def welcome_banner():
    print_line()
    print("     WELCOME TO PYTHON DAY 4")
    print_line()


welcome_banner()


# ---------------------------------------------------------------
# 2. Procedure with parameters                   (~2 min)
# ---------------------------------------------------------------
def print_multiplication_table(n, upto=10):
    print(f"\nMultiplication table of {n}:")
    for i in range(1, upto + 1):
        print(f"  {n} x {i:2} = {n * i}")


print_multiplication_table(7)
print_multiplication_table(3, upto=5)


# ---------------------------------------------------------------
# 3. Procedure vs Function — side by side        (~3 min)
# ---------------------------------------------------------------
def add_function(a, b):          # FUNCTION: gives the answer back
    return a + b


def add_procedure(a, b):         # PROCEDURE: just prints, gives nothing back
    print("  Sum is:", a + b)


print("\nFunction vs Procedure:")
x = add_function(4, 5)
print("  Value from function:", x)        # 9  -> we can reuse it

y = add_procedure(4, 5)
print("  Value from procedure:", y)       # None -> nothing came back!

# Key point for students:
#   You can do  total = add_function(4, 5) * 2   ✅
#   You CANNOT do total = add_procedure(4, 5) * 2 ❌ (None * 2 -> TypeError)


# ---------------------------------------------------------------
# 4. Procedures that MODIFY data                 (~3 min)
# ---------------------------------------------------------------
# Lists are mutable, so a procedure can change them directly.

def add_student(student_list, name):
    student_list.append(name)
    print(f"  Added {name}")


def remove_student(student_list, name):
    if name in student_list:
        student_list.remove(name)
        print(f"  Removed {name}")
    else:
        print(f"  {name} not found!")


def display_students(student_list):
    print("  Current class:", ", ".join(student_list) if student_list else "(empty)")


print("\nManaging a class list:")
batch = []
add_student(batch, "Ravi")
add_student(batch, "Priya")
add_student(batch, "Amit")
display_students(batch)
remove_student(batch, "Priya")
remove_student(batch, "Rahul")
display_students(batch)


# ---------------------------------------------------------------
# 5. Early exit using `return` in a procedure    (~2 min)
# ---------------------------------------------------------------
# A bare `return` stops the procedure immediately.

def withdraw(balance, amount):
    if amount > balance:
        print(f"  Cannot withdraw {amount}: insufficient balance ({balance})")
        return                      # stop here
    print(f"  Withdrawn {amount}. Remaining balance: {balance - amount}")


print("\nATM:")
withdraw(1000, 300)
withdraw(1000, 5000)


# ---------------------------------------------------------------
# 6. Mini program built from procedures          (~2 min)
# ---------------------------------------------------------------
def print_report_card(name, marks):
    print_line()
    print(f"  REPORT CARD : {name}")
    print_line()
    for subject, score in marks.items():
        print(f"  {subject:<10} {score:>3}")
    total = sum(marks.values())
    print_line()
    print(f"  {'TOTAL':<10} {total:>3}")
    print(f"  {'AVERAGE':<10} {total / len(marks):>6.2f}")
    print_line()


print()
print_report_card("Neha", {"Maths": 88, "Science": 92, "English": 79})


# ---------------------------------------------------------------
# PRACTICE EXERCISES (~1 min to explain)
# ---------------------------------------------------------------
# 1. Write a procedure print_square(n) that prints an n x n square of '*'
# 2. Write a procedure print_even_numbers(limit) that prints evens up to limit
# 3. Write a procedure update_price(prices, item, new_price) that changes
#    a dictionary entry and prints a confirmation message
