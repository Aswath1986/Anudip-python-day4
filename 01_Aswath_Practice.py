# """
# TOPIC 1: FUNCTIONS  (15 minutes)
# ================================
# A function is a named, reusable block of code that TAKES input (parameters)
# and usually GIVES BACK a result using `return`.

# Why use functions?
#   - Avoid repeating code (DRY: Don't Repeat Yourself)
#   - Break big problems into small, testable pieces
#   - Give a meaningful name to a piece of logic

# Run this file:  python 01_functions.py
# """

# # ---------------------------------------------------------------
# # 1. Defining and calling a function            (~2 min)
# # ---------------------------------------------------------------
# # Syntax:
# #   def function_name(parameters):
# #       body
# #       return value

# def square(number):
#     """Return the square of a number."""   # <- docstring: describes the function
#     return number * number

# result = square(7)          # calling the function; 5 is the ARGUMENT

# print("1. square(7) = ", result)
# print("   square(12) = ", square(12))

# #Get the total number of students and Subjects 
# # Implement functions to get the input marks for each student and each subject
# def userInput(studentsTotal, subjectsTotal):
#     listReturn = []
#     for student in range(studentsTotal):
#         for subject in range(subjectsTotal):
#             marksStudents = int(input(f"Enter the student {student+1} and subject {subject+1} marks : "))
#             listReturn.append(marksStudents)
#     return listReturn

# #[[20,20],[90,90],[90,100]] #Students marks
# #[[20,90,90],[20, 90, 100]] #subjects marks

# listDetails = []
# numberOfStudents = int(input("Enter the total number of students : "))
# numberOfSubjects = int(input("Enter the total number of subjects : "))
# listDetails = userInput(numberOfStudents, numberOfSubjects)

# print(listDetails)
# # print ("Total collected list : ", len(listDetails))


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

#Get the total number of students and Subjects 
# Implement functions to get the input marks for each student and each subject
def userInput(studentsTotal, subjectsTotal):
    studentList = []
    for student in range(studentsTotal):
        markList = []
        for subject in range(subjectsTotal):
            marksStudents = int(input(f"Enter the student {student+1} and subject {subject+1} marks : "))
            markList.append(marksStudents)
        studentList.append(markList)
    return studentList

listDetails = []
numberOfStudents = int(input("Enter the total number of students : "))
numberOfSubjects = int(input("Enter the total number of subjects : "))
listDetails = userInput(numberOfStudents, numberOfSubjects)

print("List collected is : ", listDetails)
print ("Total collected list : ", len(listDetails))