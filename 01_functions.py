# Function 1: Display student details
def display_student(name, age, department, marks):
    print("\n========== STUDENT DETAILS ==========")
    print("Name       :", name)
    print("Age        :", age)
    print("Department :", department)
    print("Marks      :", marks)


# Function 2: Calculate total marks
def calculate_total(marks):
    total = sum(marks)
    return total


# Function 3: Calculate average
def calculate_average(total, subjects):
    average = total / subjects
    return average


# Function 4: Find grade
def calculate_grade(average):
    if average >= 90:
        return "A+"
    elif average >= 80:
        return "A"
    elif average >= 70:
        return "B"
    elif average >= 60:
        return "C"
    elif average >= 50:
        return "D"
    else:
        return "Fail"


# Function 5: Display result
def display_result(total, average, grade):
    print("\n========== EXAM RESULT ==========")
    print("Total Marks :", total)
    print("Average     :", average)
    print("Grade       :", grade)


# Main function
def main():

    name = input("Enter student name: ")
    age = int(input("Enter student age: "))
    department = input("Enter department: ")

    marks = []

    for i in range(5):
        mark = float(input(f"Enter subject {i + 1} mark: "))
        marks.append(mark)

    display_student(name, age, department, marks)

    total = calculate_total(marks)
    average = calculate_average(total, len(marks))
    grade = calculate_grade(average)

    display_result(total, average, grade)


# Program execution
if __name__ == "__main__":
    main()