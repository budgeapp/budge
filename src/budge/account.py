from dataclasses import dataclass, field
from datetime import date, timedelta
from heapq import merge
from itertools import groupby
from typing import Generator, NamedTuple

from stockholm import Money

from .collection import Collection
from .date import daterange
from .transaction import RepeatingTransaction, Transaction


class Balance(NamedTuple):
    date: date
    balance: Money


@dataclass
class Account:
    """
    A register of transactions and repeating transactions that can be used to
    calculate or forecast a balance for any point in time.
    """

    name: str
    transactions: Collection[Transaction] = field(init=False)
    repeating_transactions: Collection[RepeatingTransaction] = field(init=False)

    def __post_init__(self):
        self.transactions = Collection[Transaction]("account", self)
        self.repeating_transactions = Collection[RepeatingTransaction]("account", self)

    def __iter__(self):
        """
        Iterate over all transactions in the account, including those generated
        by repeating transactions, ordered by date. This is useful for
        calculating or forecasting a balance for any point in time.
        """
        yield from merge(
            sorted(self.transactions),
            *(
                (
                    transaction
                    for transaction in repeating_transaction
                    if transaction not in self.transactions
                )
                for repeating_transaction in self.repeating_transactions
            ),
        )

    def transactions_range(
        self, start_date: date | None = None, end_date: date | None = None
    ) -> Generator[Transaction]:
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

    def daily_balance(
        self, start_date: date | None = None, end_date: date | None = None
    ) -> Generator[Balance]:
        """
        Iterate over the daily balance of the account, yielding tuples of date
        and balance.

        The balance on the given start date is yielded first, and then the
        balance for each subsequent date is yielded. If the start date is not
        given, the date of the first transaction is used. If the end date is not
        given, today's date is used.
        """
        start_date = start_date or next(self.transactions_range()).date
        end_date = end_date or date.today()

        balance = self.balance(start_date)
        yield Balance(start_date, balance)

        for _date, delta in self._daily_balance_delta(
            start_date + timedelta(days=1), end_date
        ):
            balance += delta
            yield Balance(_date, balance)

    def _deltas_by_date(self, start_date: date, end_date: date) -> Generator[Balance]:
        """
        Iterate over the deltas in the account balance for each date in the
        given range, including the given start and end dates.

        Yields tuples, where the first element is the date and the second
        element is the total amount of all transactions on that date.
        """
        yield from (
            Balance(
                _date, Money.sum(transaction.amount for transaction in transactions)
            )
            for _date, transactions in groupby(
                self.transactions_range(start_date, end_date), key=lambda t: t.date
            )
        )

    def _daily_balance_delta(
        self, start_date: date, end_date: date
    ) -> Generator[Balance]:
        """
        Calculate the daily change in account balance over the specified date range.

        This function yields tuples, where the first element is the date and the
        second element is the net change in balance for that date. It combines the
        deltas from actual transactions and placeholder deltas for dates without
        transactions to ensure a continuous range.
        """
        yield from (
            Balance(_date, Money.sum(delta.balance for delta in deltas))
            for _date, deltas in groupby(
                merge(
                    self._deltas_by_date(start_date, end_date),
                    (
                        Balance(_date, Money(0))
                        for _date in daterange(start_date, end_date)
                    ),
                ),
                key=lambda t: t.date,
            )
        )
