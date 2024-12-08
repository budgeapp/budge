from datetime import date

from dateutil.relativedelta import relativedelta
from dateutil.rrule import MONTHLY, rrule
from stockholm import Money

from budge import Account, RecurringTransaction, Transaction


class TestAccount:
    today = date(2022, 12, 6)

    t1 = Transaction(Money(1), "test 1", date(2022, 12, 6))

    rule1 = rrule(freq=MONTHLY, bymonthday=1, dtstart=today)
    rt1 = RecurringTransaction(Money(1), "test 1", schedule=rule1)

    rule2 = rrule(freq=MONTHLY, bymonthday=15, dtstart=today)
    rt2 = RecurringTransaction(Money(2), "test 2", schedule=rule2)

    acct = Account("test", [t1], [rt1, rt2])

    def test_balance(self):
        """
        Verify that the balance on the given date is equal to the value of all
        transactions up to and including that date.
        """
        assert self.acct.balance(self.today) == Money(1)

    def test_balance_as_of_future(self):
        """
        Verify that the balance as of one year in the future is equal to the
        expected amount after accounting for all recurring transactions.
        """
        as_of = self.today + relativedelta(years=1)
        assert self.acct.balance(as_of) == Money(37)

    def test_transactions_range(self):
        """
        Verify that the transactions_range method returns the correct number of
        transactions between the given start and end dates.
        """
        start_date = self.today + relativedelta(months=6)
        end_date = self.today + relativedelta(months=9)

        transactions = list(self.acct.transactions_range(start_date, end_date))
        assert len(transactions) == 6
