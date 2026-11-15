
def square(number):
    return number * number


square_result = square(5)
print("1. square(5) =", square_result)
print("   square(12) =", square(12))


def add_numbers(first_number, second_number):
    return first_number + second_number


def calculate_total(price, quantity):
    return price * quantity


print("\n2. add(10, 20) =", add_numbers(10, 20))
print("   Total bill =", calculate_total(250, 3))


def greet_student(student_name, message="Welcome to Anudip!"):
    return f"Hello {student_name}, {message}"


print("\n3.", greet_student("Sherin"))
print("  ", greet_student("Priya", "Good morning!"))


def get_student_info(student_name, student_age, city):
    return f"{student_name} is {student_age} years old and lives in {city}"


print("\n4.", get_student_info(student_age=20, city="Kolkata", student_name="Amit"))


def calculate_min_max_average(numbers):
    smallest_number = min(numbers)
    largest_number = max(numbers)
    average_value = sum(numbers) / len(numbers)
    return smallest_number, largest_number, average_value


student_marks = [78, 92, 65, 88, 71]
lowest_mark, highest_mark, average_mark = calculate_min_max_average(student_marks)

print(f"\n5. Lowest: {lowest_mark}, Highest: {highest_mark}, Average: {average_mark:.2f}")


def get_grade(score):
    if score >= 90:
        return "A"
    elif score >= 75:
        return "B"
    elif score >= 60:
        return "C"
    else:
        return "F"


def is_even(number):
    return number % 2 == 0


print("\n6. Grades:")
for mark in student_marks:
    print(f"   {mark} -> {get_grade(mark)}")

print("   Is 10 even?", is_even(10))


company_name = "Anudip"


def show_scope():
    trainee_name = "Sherin"
    print(f"\n7. Inside function: {trainee_name} works at {company_name}")


show_scope()


def calculate_circle_area(radius):
    return 3.14159 * square(radius)


print("\n8. Area of circle with radius 7 =", round(calculate_circle_area(7), 2))
