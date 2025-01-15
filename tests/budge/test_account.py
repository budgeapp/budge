from datetime import date

import dateutil.rrule
from dateutil.relativedelta import relativedelta
from pytest import fixture
from stockholm import Money

from budge import Account, RepeatingTransaction, Transaction
from budge.rrule import rruleset


@fixture(scope="session")
def account(
    transaction: Transaction,
    repeating_transaction_rrule: RepeatingTransaction,
    repeating_transaction_rruleset: RepeatingTransaction,
):
    acct = Account(name="test")

    manual_transaction = Transaction(
        repeating_transaction_rrule.description,
        repeating_transaction_rrule.amount,
        list(repeating_transaction_rrule)[0].date,
    )

    acct.repeating_transactions.add(
        repeating_transaction_rrule, repeating_transaction_rruleset
    )
    acct.transactions.add(transaction, manual_transaction)

    return acct


@fixture(scope="session")
def transaction():
    return Transaction("test transaction", Money(1), date(2022, 12, 1))


@fixture(scope="session")
def repeating_transaction_rrule(today: date, rrule: dateutil.rrule.rrule):
    return RepeatingTransaction(
        "test repeating transaction with rrule",
        Money(1),
        schedule=rrule,
    )


@fixture(scope="session")
def repeating_transaction_rruleset(rruleset: rruleset):
    return RepeatingTransaction(
        "test repeating transaction with rruleset", Money(2), schedule=rruleset
    )


def test_account_balance(account: Account, today: date):
    assert account.balance(today) == Money(1)
    assert account.balance(today + relativedelta(years=1)) == Money(37)


def test_account_transactions_range(account: Account, today: date):
    end_date = today + relativedelta(months=3)
    transactions = list(account.transactions_range(today, end_date))

    assert len(transactions) == 6
    assert transactions[0].description == "test repeating transaction with rruleset"
    assert transactions[0].date == date(2022, 12, 17)

    assert transactions[-1].date == date(2023, 3, 1)

    next_date = transactions[0].date
    for transaction in transactions:
        assert transaction.date >= next_date
        next_date = transaction.date


def test_account_running_balance(account: Account, today: date):
    end_date = today + relativedelta(months=3)
    balances = list(account.running_balance(today, end_date))

    assert len(balances) == 6
    assert balances[0].balance == Money(3)
    assert balances[1].balance == Money(4)
    assert balances[-1].balance == Money(10)


def test_account_daily_balance_past(account: Account, today: date):
    start_date = today + relativedelta(months=-1)
    balances = list(account.daily_balance(start_date, today))

    assert len(balances) == 31
    assert balances[0] == (start_date, Money(0))
    assert balances[-1] == (today, Money(1))


def test_account_daily_balance_future(account: Account, today: date):
    end_date = today + relativedelta(months=1)
    balances = list(account.daily_balance(today, end_date))

    assert len(balances) == 32
    assert balances[0] == (today, Money(1))
    assert balances[9] == (date(2022, 12, 15), Money(1))
    assert balances[11] == (date(2022, 12, 17), Money(3))
    assert balances[-1] == (end_date, Money(4))
