import pandas


def num_check(question, error, num_type):
    valid = False
    while not valid:

        try:
            response = num_type(input(question))

            if response <= 0:
                print(error)
            else:
                return response

        except ValueError:
            print(error)


def not_blank(question, error):
    valid = False
    while not valid:
        response = input(question)

        if response == "":
            print("{}. \n Please try again. \n".format(error))
            continue

        return response


# currency formatting
def currency(x):
    return f"${x:.2f}"
    # return "${:.2f}".format(x)


# Gets expenses, returns list wish has the data frame and sub-total
def get_expenses(var_fixed):
    # Set up dictionaries and lists

    item_list = []
    quantity_list = []
    price_list = []

    variable_dict = {
        "Item": item_list,
        "Quantity": quantity_list,
        "Price": price_list

    }

    # loop to get component, quantity and price
    item_name = ""

    while item_name.lower() != "xxx":

        print()
        # get name, quantity and item
        item_name = not_blank("Item name: ",
                              "The component name can't be blank.")

        if item_name.lower() == "xxx":
            break

        if var_fixed == "variable":
            quantity = num_check("Quantity:", "The amount must be a whole number which is more than zero", int)

        else:
            quantity = 1

        price = num_check("How much for a single item? $", "The price must be a number <more than 0>", float)

        # add item, quantity and price to lists
        item_list.append(item_name)
        quantity_list.append(quantity)
        price_list.append(price)

        expense_frame = pandas.DataFrame(variable_dict)
        expense_frame = expense_frame.set_index('Item')

        expense_frame['Cost'] = expense_frame['Quantity'] * expense_frame['Price']
        # Find sub-total
        expense_sub = expense_frame['Cost'].sum()

        add_dollars = ['Price', 'Cost']
        for item in add_dollars:
            expense_frame[item] = expense_frame[item].apply(currency)

        return [expense_frame, expense_sub]


# **** Main routine begins ****

# Get product name
# product_name = not_blank("Product name: ", "The product name can't be blank.")

fixed_expenses = get_expenses("fixed")
fixed_frame = fixed_expenses[0]
fixed_sub = fixed_expenses[1]

# **** Printing Area ****

print()
print(fixed_frame)
print()

print("Fixed Cost: ${:.2f}".format(fixed_sub))