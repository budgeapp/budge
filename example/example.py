import pandas as pd
from budge import Account, RepeatingTransaction, Transaction
from budge.rrule import rrulestr
from stockholm import Money


def load_bills(account: Account, filename: str):
    """Load bills from a CSV file with description, amount, and schedule columns."""

    bills_data = pd.read_csv(filename)

    account.repeating_transactions.clear()

    for _, bill in bills_data.iterrows():
        account.repeating_transactions.add(
            RepeatingTransaction(
                bill["description"],
                Money(bill["amount"]),
                schedule=rrulestr(bill["schedule"]),
            )
        )


def load_transactions(account: Account, filename: str):
    """Load transactions from a CSV file with description, amount, and date columns."""

    transactions_data = pd.read_csv(filename)
    transactions_data["date"] = pd.to_datetime(transactions_data["date"]).dt.date

    account.transactions.clear()

    for _, transaction in transactions_data.iterrows():
        account.transactions.add(
            Transaction(
                transaction["description"],
                Money(transaction["amount"]),
                transaction["date"],
            )
        )
