# import libraries
import pandas
import math


# Functions start here

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


# Checks that the user has entered yes / no to a question
def yes_no(question):
    to_check = ["yes", "no"]

    valid = False
    while not valid:

        response = input(question).lower()

        for var_item in to_check:
            if response == var_item:
                return response
            elif response == var_item[0]:
                return var_item

        print("Please enter either yes or no...\n")


# Ensures that the string isn't blank
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

    expense_dict = {
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

        if item_name.lower() == "xxx" and var_fixed == "variable" and len(item_list) < 1:
            item_name = ""
            print("you must have at least one variable cost")
            continue
        elif item_name.lower() == "xxx":
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

        expense_frame = pandas.DataFrame(expense_dict)
        expense_frame = expense_frame.set_index('Item')

        expense_frame['Cost'] = expense_frame['Quantity'] * expense_frame['Price']
        # Find sub-total
        expense_sub = expense_frame['Cost'].sum()

        add_dollars = ['Price', 'Cost']
        for item in add_dollars:
            expense_frame[item] = expense_frame[item].apply(currency)

    return [expense_frame, expense_sub]


# Print expenses frames
def expense_print(heading, frame, subtotal):
    print()
    print("**** {} Costs ****".format(heading))
    print(frame)
    print()
    print("{} Costs: ${:.2f}".format(heading, subtotal))
    return ""


# asks the user for a profit goal in $ / %, returns
# profit goal as $
def profit_goal(total_costs):
    # Initialise variables and error message
    error = "Please enter a VALID profit goal " \
            "(sorry, you can't do 0 because then it's not a goal \n"

    profit_type = "unknown"

    while True:

        # asks for profit goal...
        response = input("What is your profit goal? For example, $500 or $0.01 (or 50%)!")

        if response[0] == "$":
            var_profit_type = "$"
            # Get amount
            amount = response[1:]

        # check if last character is %
        elif response[-1] == "%":
            var_profit_type = "%"
            # get amount
            amount = response[:-1]

        else:
            # set response to amount for now
            var_profit_type = "unknown"
            amount = response

        try:
            # CHeck amount is a number more than 0
            amount = float(amount)
            if amount <= 0:
                print(error)
                continue

        except ValueError:
            print(error)
            continue

        if var_profit_type == "unknown" and amount >= 100:
            dollar_type = yes_no("Do you mean ${:.2f}. "
                                 "ie {:.2f} dollars?, y/n "
                                 "".format(amount, amount))
            dollar_type = yes_no(f"Do you mean {amount:.2f}")

            # SET PROFIT TYPE BASED ON USER ANSWER ABOVE
            if dollar_type == "yes":
                var_profit_type = "$"
            else:
                var_profit_type = "%"

        if var_profit_type == "unknown" and amount < 100:
            percent_type = yes_no("Do you mean {}%? , y/n".format(amount))
            if percent_type == "yes":
                profit_type = "%"
            else:
                profit_type = "$"

        # return profit goal to main routine
        if profit_type == "$":
            return amount
        else:
            goal = (amount / 100) * total_costs
            return goal


# rounding function
def round_up(amount, round_to):
    return int(math.ceil(amount / round_to)) * round_to


# **** Main routine begins ****
# Get product name
product_name = not_blank("Product name: ", "The product name can't be blank.")

how_many = num_check("How many items will you be producing?",
                     "The number of items must be a whole number more than zero", int)

print()
print("Please enter your variable costs:")
# Get variable costs
variable_expenses = get_expenses("variable")
variable_frame = variable_expenses[0]
variable_sub = variable_expenses[1]
variable_txt = pandas.DataFrame.to_string(variable_frame)

print()
have_fixed = yes_no("Do you have fixed costs (yes/no)? ")

if have_fixed == "yes":
    fixed_expenses = get_expenses("fixed")
    fixed_frame = fixed_expenses[0]
    fixed_sub = fixed_expenses[1]
    fixed_txt = pandas.DataFrame.to_string(fixed_frame)
else:
    fixed_txt = ""
    fixed_sub = 0

# work out total costs and profit target
all_costs = variable_sub + fixed_sub
profit_target = profit_goal(all_costs)

# Calculates total sales needed to reach goal
sales_needed = all_costs + profit_target

# Ask user for rounding
round_to = num_check("Round to nearest...?",
                     "Can't be 0", int)

# Calculate recommended price
selling_price = sales_needed / how_many
print(f"Selling Price (unrounded): ${selling_price:.2f}")

recommended_price = round_up(selling_price, round_to)

# Write to File
selling_info = "-* Selling Information *-"
product_name_heading = f"***** {product_name}  *****"
variable_heading = "*** Variable Costs ***"
variable_total_costs = "{Variable Costs Sub Total: $2.25}"
profit_target_txt = f" Profit Target: ${profit_target}"
fixed_heading = "*** Fixed Costs ***"
fixed_total_costs = f"** Fixed Costs Sub Total: ${get_expenses} **"
required_sales = "Required Sales: $200.00"
recommended_price = "The recommended price is $5.00"

# list holding stuff to print / write to file
to_write = [product_name_heading, variable_heading, variable_txt,
            variable_total_costs, fixed_heading, fixed_txt, fixed_total_costs,
            selling_info, profit_target_txt, required_sales, recommended_price]

# Write to file
# create file to hold data (add .txt extension)
file_name = "{}.txt".format(product_name)
text_file = open(file_name, "w+")

# heading
for item in to_write:
    text_file.write(item)
    text_file.write("\n\n")

# close file
text_file.close()


# print stuff
for item in to_write:
    print(item)
    print()
