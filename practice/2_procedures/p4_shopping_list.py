"""
Practice 4: Shopping list
Procedures can CHANGE a list that is given to them.
"""

def add_item(shopping_list, item):
    shopping_list.append(item)
    print("Added:", item)


def show_list(shopping_list):
    print("Shopping list:")
    for number, item in enumerate(shopping_list, start=1):
        print(" ", number, item)


my_list = []
add_item(my_list, "Rice")
add_item(my_list, "Milk")
add_item(my_list, "Eggs")
show_list(my_list)

# Try it yourself:
#   Write remove_item(shopping_list, item)
