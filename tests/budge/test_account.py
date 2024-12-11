from datetime import date

from dateutil.relativedelta import relativedelta
from dateutil.rrule import MONTHLY, rrule
from stockholm import Money

from budge import Account, RepeatingTransaction, Transaction


class TestAccount:
    today = date(2022, 12, 6)

    t1 = Transaction(Money(1), "test 1", date(2022, 12, 6))

    rule1 = rrule(freq=MONTHLY, bymonthday=1, dtstart=today)
    rt1 = RepeatingTransaction(Money(1), "test 1", schedule=rule1)

    rule2 = rrule(freq=MONTHLY, bymonthday=15, dtstart=today)
    rt2 = RepeatingTransaction(Money(2), "test 2", schedule=rule2)

    acct = Account("test", set([t1]), set([rt1, rt2]))

    def test_balance(self):
        """
        Verify that the balance on the given date is equal to the value of all
        transactions up to and including that date.
        """
        assert self.acct.balance(self.today) == Money(1)

    def test_balance_as_of_future(self):
        """
        Verify that the balance as of one year in the future is equal to the
        expected amount after accounting for all repeating transactions.
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

    def test_balance_iter(self):
        """
        Verify that the balance_iter method returns the correct number of
        balances between the given start and end dates.
        """
        start_date = self.today + relativedelta(months=6)
        end_date = self.today + relativedelta(months=9)

        balances = list(self.acct.balance_iter(start_date, end_date))

        assert balances == [
            (date(2023, 6, 15), Money(21)),
            (date(2023, 7, 1), Money(22)),
            (date(2023, 7, 15), Money(24)),
            (date(2023, 8, 1), Money(25)),
            (date(2023, 8, 15), Money(27)),
            (date(2023, 9, 1), Money(28)),
        ]
