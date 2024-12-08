from datetime import date

from stockholm import Money

from budge import Account, Transfer


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
