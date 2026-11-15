
"""
TOPIC 1: FUNCTIONS

A function is a reusable block of code that takes input
and returns a result.
"""


def get_student_marks(total_students, total_subjects):
    student_marks = []

    for student in range(total_students):
        marks_list = []

        for subject in range(total_subjects):
            marks = int(input(
                f"Enter the student {student + 1} and subject {subject + 1} marks: "
            ))
            marks_list.append(marks)

        student_marks.append(marks_list)

    return student_marks


total_students = int(input("Enter the total number of students: "))
total_subjects = int(input("Enter the total number of subjects: "))

student_details = get_student_marks(total_students, total_subjects)

print("List collected is:", student_details)
print("Total number of students:", len(student_details))
