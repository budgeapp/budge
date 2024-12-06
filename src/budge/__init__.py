from dataclasses import dataclass
from datetime import date
from typing import Self

from stockholm import Money


@dataclass
class Transaction:
    date: date
    amount: Money
    description: str

    def __lt__(self, other: Self):
        return self.date < other.date
