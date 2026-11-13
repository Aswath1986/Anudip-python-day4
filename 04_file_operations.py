"""
TOPIC 4: FILE OPERATIONS  (15 minutes)
======================================
Programs often need to SAVE data and READ it back later. We use files.

    open(filename, mode)

    Mode   Meaning
    ----   -------------------------------------------------------
    "r"    Read   (default) — error if the file does not exist
    "w"    Write  — creates the file, or ERASES existing content!
    "a"    Append — adds to the end, creates the file if missing
    "x"    Create — error if the file already exists

Best practice: use `with open(...) as f:` — the file closes automatically,
even if an error happens.

Run this file:  python 04_file_operations.py
"""
import os

FILENAME = "students.txt"

# ---------------------------------------------------------------
# 1. Writing to a file ("w")                    (~2 min)
# ---------------------------------------------------------------
with open(FILENAME, "w") as fPointer:
    fPointer.write("Ravi,85\n")          # \n = new line (write() does NOT add one)
    fPointer.write("Priya,92\n")
    fPointer.write("Amit,78\n")

print(f"1. Wrote 3 students to {FILENAME}")


# ---------------------------------------------------------------
# 2. Reading a whole file: read()               (~2 min)
# ---------------------------------------------------------------
with open(FILENAME, "r") as f:
    content = f.read()

print("\n2. Full content using read():")
print(content)


# ---------------------------------------------------------------
# 3. Reading line by line                       (~2 min)
# ---------------------------------------------------------------
print("3. Reading line by line (best for big files):")
with open(FILENAME, "r") as f:
    for line in f:
        print("   ->", line.strip())     # strip() removes the trailing \n

# Other options:
with open(FILENAME) as f:
    first_line = f.readline()            # one line
    remaining = f.readlines()            # list of the remaining lines
print("   readline()  :", first_line.strip())
print("   readlines() :", remaining)


# ---------------------------------------------------------------
# 4. Appending ("a") — add without erasing      (~2 min)
# ---------------------------------------------------------------
with open(FILENAME, "a") as f:
    f.write("Neha,95\n")
    f.writelines(["Rahul,67\n", "Sneha,88\n"])   # write a list of lines

print("\n4. After appending:")
with open(FILENAME) as f:
    print(f.read())


# ---------------------------------------------------------------
# 5. Processing file data                       (~3 min)
# ---------------------------------------------------------------
# Read the student file, compute results, and write a NEW report file.

def load_students(filename):
    """Return a dictionary {name: marks} from a CSV-like file."""
    students = {}
    with open(filename) as f:
        for line in f:
            name, marks = line.strip().split(",")
            students[name] = int(marks)
    return students


def save_report(students, filename):
    """Write a report file (a procedure — returns nothing)."""
    with open(filename, "w") as f:
        f.write("STUDENT REPORT\n")
        f.write("=" * 20 + "\n")
        for name, marks in students.items():
            status = "PASS" if marks >= 70 else "FAIL"
            f.write(f"{name:<8} {marks:>3}  {status}\n")
        avg = sum(students.values()) / len(students)
        f.write("=" * 20 + "\n")
        f.write(f"Class average: {avg:.2f}\n")


data = load_students(FILENAME)
print("5. Loaded:", data)
save_report(data, "report.txt")
print("   Report saved to report.txt:\n")
with open("report.txt") as f:
    print(f.read())


# ---------------------------------------------------------------
# 6. Handling file errors (links to Topic 3!)   (~2 min)
# ---------------------------------------------------------------
print("6. Handling a missing file:")
try:
    with open("does_not_exist.txt") as f:
        print(f.read())
except FileNotFoundError:
    print("   File not found! Please check the file name.")
finally:
    print("   Finished trying to read the file.")

# Old style WITHOUT `with` — shows why finally is useful:
f = None
try:
    f = open(FILENAME)
    print("   First line (manual open):", f.readline().strip())
finally:
    if f:
        f.close()                 # we must close it ourselves
        print("   File closed manually? ", f.closed)


# ---------------------------------------------------------------
# 7. Checking & deleting files with `os`        (~1 min)
# ---------------------------------------------------------------
print("\n7. File utilities:")
print("   Does students.txt exist?", os.path.exists(FILENAME))
print("   Size of students.txt   :", os.path.getsize(FILENAME), "bytes")

# Clean up the files we created (comment these out to inspect the files)
for name in (FILENAME, "report.txt"):
    if os.path.exists(name):
        os.remove(name)
print("   Cleaned up demo files. Exists now?", os.path.exists(FILENAME))


# ---------------------------------------------------------------
# PRACTICE EXERCISES (~1 min to explain)
# ---------------------------------------------------------------
# 1. Write your name and 3 hobbies to "me.txt", one per line, then read it back.
# 2. Count how many lines and words are in a text file.
# 3. Ask the user for a file name; print its content or a friendly
#    message if it does not exist (use try/except/finally).
# 4. Build a tiny "diary": each run APPENDS today's note to diary.txt.
