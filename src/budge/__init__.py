from dataclasses import dataclass, field
from datetime import date
from heapq import merge
from typing import Self

from dateutil.rrule import rrule
from stockholm import Money


@dataclass
class Transaction:
    """A single transaction record."""

    date: date
    amount: Money
    description: str
    parent: "RecurringTransaction | None" = None

    def __lt__(self, other: Self):
        return self.date < other.date


@dataclass
class RecurringTransaction:
    """A transaction that repeats on a schedule described by a `dateutil.rrule.rrule`."""

    rrule: rrule
    amount: Money
    description: str

    def __iter__(self):
        for next in self.rrule:
            yield Transaction(
                date=next.date(),
                amount=self.amount,
                description=self.description,
                parent=self,
            )


@dataclass
class Account:
    """A register of transactions and repeating transactions that can be used to
    calculate or forecast a balance for any point in time."""

    name: str
    transactions: list[Transaction] = field(default_factory=list)
    recurring_transactions: list[RecurringTransaction] = field(default_factory=list)

    def __iter__(self):
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
