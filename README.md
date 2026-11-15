# Personal Finance Tracker

A beginner-friendly, Python-based Personal Finance Tracker that helps users record, analyse, and visualise their income and expenses using CSV files.

## Features

- **Transaction Management:** Add income and expense transactions with dates, amounts, and descriptions.
- **Date Range Filtering:** View transactions within a selected date range.
- **Financial Summary:** Calculate total income, total expenses, net savings, and savings rate.
- **Data Visualisation:** Generate three types of financial graphs:
  - Daily Income vs Expenses
  - Weekly Income vs Expenses
  - Cumulative Income vs Expenses
- **CSV Storage:** Store transaction records locally using CSV files.
- **Input Validation:** Handle invalid dates, amounts, and transaction categories.
- **Flexible Startup:** Start with sample transactions, create a new tracker, or continue with existing transactions.

## Technologies Used

- Python
- Pandas
- Matplotlib
- CSV

## Project Structure

```text
Financial-Tracker/
│
├── main.py
├── data_entry.py
├── data.csv
├── sample_data.csv
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/AkshathChaudhary/Financial-Tracker.git
```

### 2. Navigate to the project directory

```bash
cd Financial-Tracker
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the application

```bash
python main.py
```

## How to Use

1. Launch the application.
2. Choose whether to load sample transactions, create a new tracker, or continue with existing transactions.
3. Add income or expense records through the main menu.
4. Select a date range to view your transactions and financial summary.
5. Generate graphs to analyse your financial activity.

## Data Storage

All transaction records are stored locally in CSV format.

- `sample_data.csv` contains demonstration transactions.
- `data.csv` stores the transactions used by the application.

Your financial records are not uploaded to an external server.

## Learning Objectives

This project was developed to practise:

- Python programming and modular code organisation.
- File handling and CSV operations.
- Data manipulation using Pandas.
- Data visualisation using Matplotlib.
- Input validation and exception handling.

## Future Improvements

Potential improvements include:

- More detailed financial analytics.
- Expense categorisation.
- Improved reporting and visualisation.
- A graphical user interface.

## Author

**Akshath Chaudhary**

GitHub: [AkshathChaudhary](https://github.com/AkshathChaudhary)