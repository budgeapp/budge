from dataclasses import dataclass, field
from datetime import date
from heapq import merge
from itertools import groupby

from stockholm import Money

from .transaction import RepeatingTransaction, Transaction


@dataclass
class Account:
    """
    A register of transactions and repeating transactions that can be used to
    calculate or forecast a balance for any point in time.
    """

    name: str
    transactions: set[Transaction] = field(default_factory=set)
    repeating_transactions: set[RepeatingTransaction] = field(default_factory=set)

    def __iter__(self):
        """
        Iterate over all transactions in the account, including those generated
        by repeating transactions, ordered by date. This is useful for
        calculating or forecasting a balance for any point in time.
        """
        yield from merge(sorted(self.transactions), *self.repeating_transactions)

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

    def balance(self, as_of: date | None = None):
        """Calculate the account balance as of the given date."""
        as_of = as_of or date.today()

        return Money.sum(
            transaction.amount
            for transaction in self.transactions_range(end_date=as_of)
        )

    def balance_iter(
        self, start_date: date | None = None, end_date: date | None = None
    ):
        """
        Iterate over the account's balance over the given range, yielding a
        tuple of each date in the range and the account balance on that date.

        If `start_date` is not provided, the first yield will be the initial
        balance of the account.

        If `end_date` is not provided, the iteration will continue until all
        transactions in the account have been iterated over.

        :param start_date: The start date of the range
        :param end_date: The end date of the range
        :yield: A tuple of (date, balance) for each day in the range
        """
        bal = self.balance(start_date) if start_date else Money(0)

        for date_, transactions in groupby(
            self.transactions_range(start_date, end_date), lambda t: t.date
        ):
            bal += Money.sum(transaction.amount for transaction in transactions)
            yield date_, bal
