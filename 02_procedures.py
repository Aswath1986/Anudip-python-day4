# Function: Calculate total price
def calculate_total(price, quantity):
    total = price * quantity
    return total


# Function: Calculate discount
def calculate_discount(total):
    if total >= 5000:
        return total * 0.10
    elif total >= 2000:
        return total * 0.05
    else:
        return 0


# Procedure: Display bill
def display_bill(customer, total, discount, final_amount):
    print("\n========== CUSTOMER BILL ==========")
    print("Customer Name :", customer)
    print("Total Amount  :", total)
    print("Discount      :", discount)
    print("Final Amount  :", final_amount)
    print("===================================")


# Main procedure
def main():
    customer = input("Enter customer name: ")
    price = float(input("Enter product price: "))
    quantity = int(input("Enter quantity: "))

    total = calculate_total(price, quantity)
    discount = calculate_discount(total)
    final_amount = total - discount

    display_bill(customer, total, discount, final_amount)


main()