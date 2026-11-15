from datetime import datetime

date_format = "%d-%m-%Y"
CATEGORIES = {"I":"Income","E":"Expense"}


def get_date(prompt, allow_default=False):
    while True:
        date_str = input(prompt)

        if allow_default and not date_str:
            return datetime.today().strftime(date_format)

        try:
            valid_date = datetime.strptime(date_str, date_format)
            return valid_date.strftime(date_format)

        except ValueError:
            print("Invalid date format. Please enter the date in DD-MM-YYYY format.")



def get_amount():
    while True:
        try:
            amount = float(input("Enter the amount: "))

            if amount <= 0:
                raise ValueError("Amount must be greater than zero.")

            return amount

        except ValueError as e:
            print(e)
            print("Please enter a valid amount.")



def get_category():
    while True:
        category = input(
            "Enter category ('I' for Income or 'E' for Expense): "
        ).strip().upper()

        if category in CATEGORIES:
            return CATEGORIES[category]

        print("Invalid category. Please enter I or E.")



def get_description():
    description = input("Enter a description (optional): ").strip()

    if not description:
        return "No description"

    return description
