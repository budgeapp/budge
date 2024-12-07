from datetime import date

from dateutil.relativedelta import relativedelta
from dateutil.rrule import MONTHLY, rrule
from stockholm import Money

from budge import Account, RecurringTransaction, Transaction


class TestAccount:
    today = date(2022, 12, 6)

    t1 = Transaction(date(2022, 12, 6), Money(1), "test 1")

    rule1 = rrule(freq=MONTHLY, bymonthday=1, dtstart=today)
    rt1 = RecurringTransaction(rule1, Money(1), "test 1")

    rule2 = rrule(freq=MONTHLY, bymonthday=15, dtstart=today)
    rt2 = RecurringTransaction(rule2, Money(2), "test 2")

    acct = Account("test", [t1], [rt1, rt2])

    def test_balance(self):
        assert self.acct.balance(self.today) == Money(1)

    def test_until(self):
        as_of = self.today + relativedelta(years=1)
        transactions = list(self.acct.until(as_of))

        assert len(transactions) == 25
        assert self.acct.balance(as_of) == Money(37)
