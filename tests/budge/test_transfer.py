from datetime import date

from dateutil.relativedelta import relativedelta
from dateutil.rrule import MONTHLY, rrule
from stockholm import Money

from budge import Account, RepeatingTransfer, Transfer


class TestTransfer:
    today = date(2022, 12, 6)

    a1 = Account("a1")
    a2 = Account("a2")

    def test_transfer(self):
        """
        Verify that a transfer between two accounts correctly updates the
        balance of each account.
        """
        transfer = Transfer(
            date=self.today,
            amount=Money(100),
            description="test transfer",
            from_account=self.a1,
            to_account=self.a2,
        )

        assert transfer.from_transaction.amount == Money(-100)
        assert transfer.to_transaction.amount == Money(100)

        assert self.a1.balance(self.today) == Money(-100)
        assert self.a2.balance(self.today) == Money(100)


class TestRepeatingTransfer:
    today = date(2022, 12, 6)

    a1 = Account("a1")
    a2 = Account("a2")

    def test_repeating_transfer(self):
        """
        Verify that a repeating transfer between two accounts correctly updates
        the balance of each account.
        """
        transfer = RepeatingTransfer(
            amount=Money(100),
            description="test transfer",
            from_account=self.a1,
            to_account=self.a2,
            schedule=rrule(freq=MONTHLY, bymonthday=1, dtstart=self.today),
        )

        assert transfer.from_transaction.amount == Money(-100)
        assert transfer.to_transaction.amount == Money(100)

        test_date = self.today + relativedelta(months=6)

        assert self.a1.balance(test_date) == Money(-600)
        assert self.a2.balance(test_date) == Money(600)
