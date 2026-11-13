"""
Practice 5: Marks file
Save names and marks, read them back, and handle a missing file.
"""
import os

with open("marks.txt", "w") as file:
    file.write("Ravi,85\n")
    file.write("Priya,92\n")
    file.write("Amit,78\n")

total = 0
with open("marks.txt", "r") as file:
    for line in file:
        name, marks = line.strip().split(",")
        print(name, "scored", marks)
        total = total + int(marks)
print("Total marks:", total)

# A file that does not exist
try:
    with open("attendance.txt", "r") as file:
        print(file.read())
except FileNotFoundError:
    print("attendance.txt was not found")
finally:
    print("Done reading files")

os.remove("marks.txt")      # delete this line to keep the file

# Try it yourself:
#   Print the average marks of the class
