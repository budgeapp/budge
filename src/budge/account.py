from dataclasses import dataclass, field
from datetime import date
from heapq import merge

from stockholm import Money

from .transaction import RecurringTransaction, Transaction


@dataclass
class Account:
    """
    A register of transactions and repeating transactions that can be used to
    calculate or forecast a balance for any point in time.
    """

    name: str
    transactions: list[Transaction] = field(default_factory=list)
    recurring_transactions: list[RecurringTransaction] = field(default_factory=list)

    def __iter__(self):
        """
        Iterate over all transactions in the account, including those generated
        by recurring transactions, ordered by date. This is useful for
        calculating or forecasting a balance for any point in time.
        """

        for transaction in merge(
            *self.recurring_transactions, sorted(self.transactions)
        ):
            yield transaction

    def transactions_range(
        self, start_date: date | None = None, end_date: date | None = None
    ):
        """Iterate over transactions in the account over the given range."""
        for transaction in self:
            if start_date and transaction.date < start_date:
                continue
            if end_date and transaction.date > end_date:
                break
            yield transaction

    def balance(self, as_of: date = date.today()) -> Money:
        """Calculate the account balance as of the given date."""
        return Money(
            sum(
                transaction.amount
                for transaction in self.transactions_range(end_date=as_of)
            )
        )
