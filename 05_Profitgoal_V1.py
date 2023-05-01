# import libraries


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


def profit_goal(total_costs):
    # Initialise variables and error message
    error = "Please enter a VALID profit goal " \
            "(no, you can't do 0 because then it's not a goal [yes carl, we're talking about you." \
            "])\n"

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


# Main routine goes here
all_costs = 200

# Loop for quick testing:
for item in range(0, 6):
    profit_target = profit_goal(all_costs)
    print("Profit Target: ${:.2f}".format(profit_target))
    print("Total Sales: ${:.2f}".format(all_costs + profit_target))
    print()