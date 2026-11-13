"""
Practice 5: Total and average of marks
A function can return TWO values at once.
"""

def total_and_average(marks):
    total = sum(marks)
    average = total / len(marks)
    return total, average


marks = [80, 75, 92, 68, 85]
total, average = total_and_average(marks)

print("Marks   :", marks)
print("Total   :", total)
print("Average :", average)

# Try it yourself:
#   Also return the highest mark (hint: max(marks))
