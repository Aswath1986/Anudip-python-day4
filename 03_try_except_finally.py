def check_balance(balance, amount):

    if amount <= 0:
        raise ValueError("Withdrawal amount must be positive.")

    if amount > balance:
        raise ValueError("Insufficient account balance.")

    return balance - amount


def display_details(balance):
    print("\n========== ATM DETAILS ==========")
    print("Remaining Balance:", balance)
    print("Transaction completed.")
    print("=================================")


def main():

    balance = 10000

    try:
        print("Available Balance:", balance)

        amount = float(input("Enter withdrawal amount: "))

        new_balance = check_balance(balance, amount)

    except ValueError as e:
        print("Transaction Failed:", e)

    else:
        display_details(new_balance)

    finally:
        print("\nThank you for using our ATM!")


main()