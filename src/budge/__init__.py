from dataclasses import dataclass
from datetime import date
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
