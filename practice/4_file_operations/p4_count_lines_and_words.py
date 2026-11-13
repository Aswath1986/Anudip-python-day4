"""
Practice 4: Count lines and words
Read a file and count what is inside it.
"""
import os

with open("story.txt", "w") as file:
    file.write("Python is easy to learn\n")
    file.write("Practice makes it easier\n")
    file.write("Keep coding every day\n")

lines = 0
words = 0
with open("story.txt", "r") as file:
    for line in file:
        lines = lines + 1
        words = words + len(line.split())

print("Lines:", lines)
print("Words:", words)

os.remove("story.txt")      # delete this line to keep the file

# Try it yourself:
#   Also count the characters (hint: len(line))
