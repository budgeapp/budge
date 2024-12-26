from dataclasses import dataclass, field
from datetime import date as _date
from typing import Self

from dateutil.rrule import rrule, rruleset
from stockholm import Money

from . import account


@dataclass
class Transaction:
    """A single transaction record."""

    amount: Money
    description: str
    date: _date = field(default_factory=_date.today)
    account: "account.Account | None" = field(default=None, kw_only=True)
    parent: Self | None = field(default=None, kw_only=True)

    def __hash__(self):
        return hash((self.amount, self.description, self.date))

    def __lt__(self, other: Self):
        """Compare transactions based on their date for ordering."""
        return self.date < other.date


@dataclass(kw_only=True)
class RepeatingTransaction(Transaction):
    """
    A transaction that repeats on a schedule described by a
    `dateutil.rrule.rrule` or `dateutil.rrule.rruleset`.
    """

    schedule: rrule | rruleset

    def __hash__(self):
        return hash((self.amount, self.description, self.schedule))

    def __iter__(self):
        """
        Yield transactions generated by the repeat rule, each with the specified
        amount and description, and link them to this repeat transaction as
        their parent.
        """
        yield from (
            Transaction(
                amount=self.amount,
                description=self.description,
                date=next.date(),
                account=self.account,
                parent=self,
            )
            for next in self.schedule
        )
