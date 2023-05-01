import math


# integer that is more than zero. Takes in custom error message
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


# rounding function
def round_up(amount, var_round_to)


# main routine starts here
how_many = num_check("How many items ", "Cant be 0", int)
total = num_check("Total Costs? ", "More than 0", float)
profit_goal = num_check("Profit Goal? ", "More than 0 ", float)
round_to = num_check("Round to nearest...? ", "Cant be 0", int)

sales_needed = total + profit_goal

print("Total: ${:.2f}".format(total))
print("Profit Goal ${:.2f}".format(profit_goal))

selling_price = sales_needed / how_many
print("Selling Price (unrounded) : ${:.2f}".format(selling_price))