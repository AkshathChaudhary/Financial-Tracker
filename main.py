import pandas as pd
from datetime import datetime
import csv
from data_entry import get_category, get_amount, get_date, get_description
import matplotlib.pyplot as plt
import os
import shutil




class CSV:
    CSV_FILE = 'data.csv'
    SAMPLE_FILE = 'sample_data.csv'

    Cols = ['date', 'amount', 'category', 'description']
    FORMAT = "%d-%m-%Y"

        
    @classmethod
    def initialise_csv(cls):

        while True:
            print("\n========== WELCOME TO PERSONAL FINANCE TRACKER ==========")
            print("1. Start with sample transactions")
            print("2. Create a new empty tracker")
            print("3. Continue with existing transactions")

            choice = input("\nChoose an option (1-3): ").strip()

            # OPTION 1: Use sample data
            if choice == "1":

                if not os.path.exists(cls.SAMPLE_FILE):
                    print("Sample data file not found!")
                    continue

                if os.path.exists(cls.CSV_FILE):
                    confirm = input(
                        "This will replace your existing transactions. Continue? (Y/N): "
                    ).strip().upper()

                    if confirm != "Y":
                        print("Operation cancelled.")
                        continue

                shutil.copyfile(cls.SAMPLE_FILE, cls.CSV_FILE)
                print("Sample transactions loaded successfully!")
                break

            # OPTION 2: Create a fresh empty tracker
            elif choice == "2":

                if os.path.exists(cls.CSV_FILE):
                    confirm = input(
                        "This will delete your existing transactions. Continue? (Y/N): "
                    ).strip().upper()

                    if confirm != "Y":
                        print("Operation cancelled.")
                        continue

                df = pd.DataFrame(columns=cls.Cols)
                df.to_csv(cls.CSV_FILE, index=False)

                print("New empty tracker created successfully!")
                break

            # OPTION 3: Continue with existing data
            elif choice == "3":

                if os.path.exists(cls.CSV_FILE):
                    print("Continuing with your existing transactions!")
                    break
                else:
                    print("No existing transaction file found. Please choose 1 or 2.")

            else:
                print("Invalid choice! Please select 1, 2 or 3.")




    @classmethod
    def add_entry(cls,date,amount,category,description):
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description
        }
        with open(cls.CSV_FILE, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.Cols)
            writer.writerow(new_entry)
        print("Entry added successfully.")

    
    @classmethod
    def get_transactions(cls, start_date, end_date):

        df = pd.read_csv(cls.CSV_FILE)

        # Check whether the CSV has the required columns
        if not all(column in df.columns for column in cls.Cols):
            print("CSV file has an invalid structure.")
            return pd.DataFrame(columns=cls.Cols)

        # Handle an empty CSV
        if df.empty:
            print("No transactions available.")
            return df

        # Convert dates into datetime format
        df["date"] = pd.to_datetime(
            df["date"],
            format=cls.FORMAT,
            errors="coerce"
        )

        # Remove rows containing invalid dates
        df.dropna(subset=["date"], inplace=True)

        # Convert amount into numeric values
        df["amount"] = pd.to_numeric(
            df["amount"],
            errors="coerce"
        )

        # Remove rows containing invalid amounts
        df.dropna(subset=["amount"], inplace=True)

        # Convert input dates
        start_date = datetime.strptime(start_date, cls.FORMAT)
        end_date = datetime.strptime(end_date, cls.FORMAT)

        # Filter transactions within the selected date range
        mask = (
            (df["date"] >= start_date) &
            (df["date"] <= end_date)
        )

        filtered_df = df.loc[mask].copy()

        if filtered_df.empty:
            print("No transactions in the given date range.")

        else:
            print(
                f"\nTransactions from {start_date.strftime(cls.FORMAT)} "
                f"to {end_date.strftime(cls.FORMAT)}"
            )

            print(
                filtered_df.to_string(
                    index=False,
                    formatters={
                    "date": lambda x: x.strftime(cls.FORMAT)
                    }
                )
            )
        print("\n========== SUMMARY ==========")

        total_income = filtered_df[
            filtered_df["category"] == "Income"
        ]["amount"].sum()

        total_expense = filtered_df[
            filtered_df["category"] == "Expense"
        ]["amount"].sum()

        net_savings = total_income - total_expense
        if total_income > 0:
            savings_rate = (net_savings / total_income) * 100
        else:
            savings_rate = 0
        transaction_count = len(filtered_df)

        print(f"Total transactions: {transaction_count}")
        print(f"Total income: ₹{total_income:.2f}")
        print(f"Total expenses: ₹{total_expense:.2f}")
        print(f"Net savings: ₹{net_savings:.2f}")
        print(f"Savings Rate   : {savings_rate:.2f}%")
        print("=======================================")

        return filtered_df



def add():
    date=get_date("Enter the date of transaction (dd-mm-yyyy) or ENTER for todays date: ", allow_default=True)
    amount=get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date,amount,category,description)


def plot_transactions(df):
    if df.empty:
        print("No transactions available to plot.")
        return

    df = df.copy()

    # Ensure correct data types
    df["date"] = pd.to_datetime(df["date"])
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)

    df.set_index("date", inplace=True)
    df.sort_index(inplace=True)

    # Create a continuous daily timeline
    date_range = pd.date_range(
        start=df.index.min(),
        end=df.index.max(),
        freq="D"
    )

    # Calculate daily income and expenses separately
    daily_income = (
        df[df["category"] == "Income"]["amount"]
        .resample("D").sum()
        .reindex(date_range, fill_value=0)
    )

    daily_expense = (
        df[df["category"] == "Expense"]["amount"]
        .resample("D").sum()
        .reindex(date_range, fill_value=0)
    )

    # Ask user which graph they want
    print("\n========== GRAPH OPTIONS ==========")
    print("1. Daily Income vs Expenses")
    print("2. Weekly Income vs Expenses")
    print("3. Cumulative Income vs Expenses")
    print("4. Back")

    choice = input("Choose a graph (1-4): ")

    if choice == "4":
        return

    plt.figure(figsize=(11, 6))

    # GRAPH 1: DAILY
    if choice == "1":

        plt.plot(
            daily_income.index,
            daily_income,
            label="Income",
            color="green",
            marker="o",
            linewidth=2
        )

        plt.plot(
            daily_expense.index,
            daily_expense,
            label="Expense",
            color="red",
            marker="o",
            linewidth=2
        )

        plt.title("Daily Income vs Expenses")
        plt.xlabel("Date")
        plt.ylabel("Amount (₹)")

    # GRAPH 2: WEEKLY
    elif choice == "2":

        weekly_income = daily_income.resample("W").sum()
        weekly_expense = daily_expense.resample("W").sum()

        plt.plot(
            weekly_income.index,
            weekly_income,
            label="Income",
            color="green",
            marker="o",
            linewidth=2
        )

        plt.plot(
            weekly_expense.index,
            weekly_expense,
            label="Expense",
            color="red",
            marker="o",
            linewidth=2
        )

        plt.title("Weekly Income vs Expenses")
        plt.xlabel("Week")
        plt.ylabel("Amount (₹)")

    # GRAPH 3: CUMULATIVE
    elif choice == "3":

        cumulative_income = daily_income.cumsum()
        cumulative_expense = daily_expense.cumsum()

        plt.plot(
            cumulative_income.index,
            cumulative_income,
            label="Total Income",
            color="green",
            linewidth=2.5
        )

        plt.plot(
            cumulative_expense.index,
            cumulative_expense,
            label="Total Expenses",
            color="red",
            linewidth=2.5
        )

        plt.title("Cumulative Income vs Expenses")
        plt.xlabel("Date")
        plt.ylabel("Cumulative Amount (₹)")

    else:
        print("Invalid choice! Please select 1, 2, 3 or 4.")
        plt.close()
        return

    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def main():
    CSV.initialise_csv()
    while True:
        print("\n1. Add a transaction")
        print("2. View transactions and summary within a date range")
        print("3. Exit")
        choice = input("Enter your choice (1-3) :- ")

        if choice=="1":
            add()
        elif choice=="2":
            start_date = get_date("Enter the start date (dd-mm-yyyy):- ")
            end_date = get_date("Enter the end date (dd-mm-yyyy):- ")
            start = datetime.strptime(start_date, CSV.FORMAT)
            end = datetime.strptime(end_date, CSV.FORMAT)
            if start > end:
                print("Error: Start date cannot be after the end date.")
                continue
            df = CSV.get_transactions(start_date,end_date)
            if input("Do you wanna see a plot? (Y/N):- ").lower() == "y":
                plot_transactions(df)
        elif choice=="3":
            print("Exiting...")
            break
        else:
            print("Invalid choice! Enter 1, 2 or 3.")

if __name__== "__main__":
    main()