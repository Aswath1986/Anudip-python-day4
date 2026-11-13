"""
Practice 1: Write and read
"w" = write (creates the file), "r" = read.
"""
import os

with open("hello.txt", "w") as file:
    file.write("Hello students!\n")
    file.write("Welcome to file handling.\n")

with open("hello.txt", "r") as file:
    content = file.read()

print("The file contains:")
print(content)

os.remove("hello.txt")      # delete this line to keep the file

# Try it yourself:
#   Write your name and city to the file, then read it back
