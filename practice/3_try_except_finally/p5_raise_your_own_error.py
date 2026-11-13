"""
Practice 5: Raise your own error
Use `raise` when a value is wrong for YOUR program.
"""

def withdraw(balance, amount):
    if amount > balance:
        raise ValueError("Not enough balance")
    return balance - amount


try:
    print("Balance left:", withdraw(1000, 300))
    print("Balance left:", withdraw(1000, 5000))
except ValueError as error:
    print("Error:", error)
finally:
    print("Thank you for using the ATM")

# Try it yourself:
#   Also raise ValueError when amount is 0 or negative
