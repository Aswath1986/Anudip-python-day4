
def print_line():
    print("-" * 40)


def welcome_banner():
    print_line()
    print("     WELCOME TO PYTHON DAY 4")
    print_line()


welcome_banner()


def print_multiplication_table(number, limit=10):
    print(f"\nMultiplication table of {number}:")
    for multiplier in range(1, limit + 1):
        print(f"  {number} x {multiplier:2} = {number * multiplier}")


print_multiplication_table(7)
print_multiplication_table(3, limit=5)


def add_function(first_number, second_number):
    return first_number + second_number


def add_procedure(first_number, second_number):
    print("  Sum is:", first_number + second_number)


print("\nFunction vs Procedure:")
function_result = add_function(4, 5)
print("  Value from function:", function_result)

procedure_result = add_procedure(4, 5)
print("  Value from procedure:", procedure_result)


def add_student(student_list, student_name):
    student_list.append(student_name)
    print(f"  Added {student_name}")


def remove_student(student_list, student_name):
    if student_name in student_list:
        student_list.remove(student_name)
        print(f"  Removed {student_name}")
    else:
        print(f"  {student_name} not found!")


def display_students(student_list):
    print("  Current class:", ", ".join(student_list) if student_list else "(empty)")


print("\nManaging a class list:")
student_list = []

add_student(student_list, "Ravi")
add_student(student_list, "Priya")
add_student(student_list, "Amit")
display_students(student_list)

remove_student(student_list, "Priya")
remove_student(student_list, "Rahul")
display_students(student_list)


def withdraw(balance, withdrawal_amount):
    if withdrawal_amount > balance:
        print(f"  Cannot withdraw {withdrawal_amount}: insufficient balance ({balance})")
        return

    remaining_balance = balance - withdrawal_amount
    print(f"  Withdrawn {withdrawal_amount}. Remaining balance: {remaining_balance}")


print("\nATM:")
withdraw(1000, 300)
withdraw(1000, 5000)


def print_report_card(student_name, subject_marks):
    print_line()
    print(f"  REPORT CARD : {student_name}")
    print_line()

    for subject, score in subject_marks.items():
        print(f"  {subject:<10} {score:>3}")

    total_marks = sum(subject_marks.values())

    print_line()
    print(f"  {'TOTAL':<10} {total_marks:>3}")
    print(f"  {'AVERAGE':<10} {total_marks / len(subject_marks):>6.2f}")
    print_line()


print()
print_report_card("Sherin", {"Maths": 88, "Science": 92, "English": 79})
