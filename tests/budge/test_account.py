from datetime import date

from dateutil.relativedelta import relativedelta
from dateutil.rrule import MONTHLY, rrule
from stockholm import Money

from budge import Account, RepeatingTransaction, Transaction


class TestAccount:
    today = date(2022, 12, 6)

    t1 = Transaction("test 1", Money(1), date(2022, 12, 1))

    rule1 = rrule(freq=MONTHLY, bymonthday=1, dtstart=today)
    rt1 = RepeatingTransaction("test 1", Money(1), schedule=rule1)
    rt1_manual = Transaction(rt1.description, rt1.amount, rule1[0].date())

    rule2 = rrule(freq=MONTHLY, bymonthday=15, dtstart=today)
    rt2 = RepeatingTransaction("test 2", Money(2), schedule=rule2)

    acct = Account("test")
    acct.transactions.add(t1, rt1_manual)
    acct.repeating_transactions.add(rt1)
    acct.repeating_transactions.add(rt2)

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

    def test_daily_balance_past(self):
        """
        Verify that the daily_balance method returns the correct balances for each
        day in the past month, starting from a given start date and ending on today's
        date. The initial balance should be zero, and the balance on today's date
        should match the expected value.
        """
        start_date = date(2022, 11, 6)
        balances = list(
            self.acct.daily_balance(start_date=start_date, end_date=self.today)
        )

        assert len(balances) == 31
        assert balances[0] == (start_date, Money(0))
        assert balances[-1] == (self.today, Money(1))

    def test_daily_balance_future(self):
        """
        Verify that the daily_balance method returns the correct balances for each
        day in the future month, starting from today's date and ending on a given
        end date. The initial balance should be the expected value, and the balance
        on the end date should match the expected value.
        """
        end_date = self.today + relativedelta(months=1)
        balances = list(
            self.acct.daily_balance(start_date=self.today, end_date=end_date)
        )

        assert len(balances) == 32
        assert balances[0] == (self.today, Money(1))
        assert balances[9] == (date(2022, 12, 15), Money(3))
        assert balances[-1] == (end_date, Money(4))
