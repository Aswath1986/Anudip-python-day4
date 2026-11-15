
import os

FILE_NAME = "students.txt"


with open(FILE_NAME, "w") as file_pointer:
    file_pointer.write("Ravi,85\n")
    file_pointer.write("Priya,92\n")
    file_pointer.write("Amit,78\n")

print(f"1. Wrote 3 students to {FILE_NAME}")


with open(FILE_NAME, "r") as file:
    file_content = file.read()

print("\n2. Full content using read():")
print(file_content)


print("3. Reading line by line:")
with open(FILE_NAME, "r") as file:
    for line in file:
        print("   ->", line.strip())


with open(FILE_NAME, "r") as file:
    first_line = file.readline()
    remaining_lines = file.readlines()

print("   readline():", first_line.strip())
print("   readlines():", remaining_lines)


with open(FILE_NAME, "a") as file:
    file.write("Neha,95\n")
    file.writelines(["Rahul,67\n", "Sneha,88\n"])


print("\n4. After appending:")
with open(FILE_NAME, "r") as file:
    print(file.read())


def load_students(file_name):
    student_details = {}

    with open(file_name, "r") as file:
        for line in file:
            student_name, student_marks = line.strip().split(",")
            student_details[student_name] = int(student_marks)

    return student_details


def save_report(student_details, file_name):
    with open(file_name, "w") as file:
        file.write("STUDENT REPORT\n")
        file.write("=" * 20 + "\n")

        for student_name, student_marks in student_details.items():
            result_status = "PASS" if student_marks >= 70 else "FAIL"
            file.write(f"{student_name:<8} {student_marks:>3}  {result_status}\n")

        average_marks = sum(student_details.values()) / len(student_details)

        file.write("=" * 20 + "\n")
        file.write(f"Class average: {average_marks:.2f}\n")


student_data = load_students(FILE_NAME)
print("5. Loaded:", student_data)

save_report(student_data, "report.txt")

print("   Report saved to report.txt:\n")

with open("report.txt", "r") as file:
    print(file.read())


print("6. Handling a missing file:")

try:
    with open("does_not_exist.txt", "r") as file:
        print(file.read())

except FileNotFoundError:
    print("   File not found! Please check the file name.")

finally:
    print("   Finished trying to read the file.")


file_pointer = None

try:
    file_pointer = open(FILE_NAME, "r")
    print("   First line:", file_pointer.readline().strip())

finally:
    if file_pointer:
        file_pointer.close()
        print("   File closed manually?", file_pointer.closed)


print("\n7. File utilities:")
print("   Does students.txt exist?", os.path.exists(FILE_NAME))
print("   Size of students.txt:", os.path.getsize(FILE_NAME), "bytes")


for file_name in (FILE_NAME, "report.txt"):
    if os.path.exists(file_name):
        os.remove(file_name)

print("   Cleaned up demo files. Exists now?", os.path.exists(FILE_NAME))
