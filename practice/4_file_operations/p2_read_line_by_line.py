"""
Practice 2: Read line by line
A for loop reads one line at a time.
"""
import os

with open("fruits.txt", "w") as file:
    file.write("apple\n")
    file.write("banana\n")
    file.write("mango\n")

with open("fruits.txt", "r") as file:
    number = 1
    for line in file:
        print(number, line.strip())     # strip() removes the \n at the end
        number = number + 1

os.remove("fruits.txt")     # delete this line to keep the file

# Try it yourself:
#   Print each fruit in CAPITAL letters (hint: .upper())
