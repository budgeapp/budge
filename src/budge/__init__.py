from dataclasses import dataclass, field
from datetime import date
from heapq import merge
from typing import Self

from dateutil.rrule import rrule
from stockholm import Money


@dataclass
class Transaction:
    date: date
    amount: Money
    description: str

    def __lt__(self, other: Self):
        return self.date < other.date


@dataclass
class RecurringTransaction:
    rrule: rrule
    amount: Money
    description: str

    def __iter__(self):
        for next in self.rrule:
            yield Transaction(next.date(), self.amount, self.description)


@dataclass
class Account:
    name: str
    transactions: list[Transaction] = field(default_factory=list)
    recurring_transactions: list[RecurringTransaction] = field(default_factory=list)

    def __iter__(self):
        for transaction in merge(
            *self.recurring_transactions, sorted(self.transactions)
        ):
            yield transaction

    def until(self, end_date: date = date.today()):
        for transaction in self:
            if transaction.date > end_date:
                break
            yield transaction

    def balance(self, as_of: date = date.today()) -> Money:
        return Money(sum(transaction.amount for transaction in self.until(as_of)))
