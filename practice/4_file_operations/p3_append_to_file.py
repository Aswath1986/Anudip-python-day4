"""
Practice 3: Append to a file
"a" adds to the END of the file. "w" would erase the old content.
"""
import os

with open("diary.txt", "w") as file:
    file.write("Monday: learned functions\n")

with open("diary.txt", "a") as file:
    file.write("Tuesday: learned exceptions\n")
    file.write("Wednesday: learned files\n")

with open("diary.txt", "r") as file:
    print(file.read())

os.remove("diary.txt")      # delete this line to keep the file

# Try it yourself:
#   Change "a" to "w" and run again. Which lines are left?
