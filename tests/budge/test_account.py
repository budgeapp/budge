from datetime import date

import dateutil.rrule
from dateutil.relativedelta import relativedelta
from pytest import fixture
from stockholm import Money

from budge import Account, RepeatingTransaction, Transaction
from budge.rrule import rruleset


@fixture
def account(
    transaction: Transaction,
    cleared_transaction: Transaction,
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
    acct.transactions.add(transaction, cleared_transaction, manual_transaction)

    return acct


@fixture
def transaction():
    return Transaction("test transaction", Money(1), date(2022, 12, 1))


@fixture
def cleared_transaction():
    return Transaction(
        "test cleared transaction", Money(10), date(2022, 12, 1), cleared=True
    )


@fixture
def repeating_transaction_rrule(today: date, rrule: dateutil.rrule.rrule):
    return RepeatingTransaction(
        "test repeating transaction with rrule",
        Money(100),
        schedule=rrule,
        _last_cleared=today + relativedelta(months=1),
    )


@fixture
def repeating_transaction_rruleset(today: date, rruleset: rruleset):
    return RepeatingTransaction(
        "test repeating transaction with rruleset",
        Money(1000),
        schedule=rruleset,
        _last_cleared=today + relativedelta(months=1),
    )


def test_account_balance(account: Account, today: date):
    assert account.balance(today) == Money(11)
    assert account.balance(today + relativedelta(years=1)) == Money(13211)


def test_account_balance_cleared_true(account: Account, today: date):
    assert account.balance(today, cleared=True) == Money(10)
    assert account.balance(today + relativedelta(years=1), cleared=True) == Money(1010)


def test_account_balance_cleared_false(account: Account, today: date):
    assert account.balance(today, cleared=False) == Money(1)
    assert account.balance(today + relativedelta(years=1), cleared=False) == Money(
        12201
    )


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


def test_account_transactions_range_cleared_true(account: Account, today: date):
    end_date = today + relativedelta(months=3)
    transactions = list(account.transactions_range(today, end_date, cleared=True))

    assert len(transactions) == 1
    assert transactions[0].description == "test repeating transaction with rruleset"
    assert transactions[0].date == date(2022, 12, 17)


def test_account_transactions_range_cleared_false(account: Account, today: date):
    end_date = today + relativedelta(months=3)
    transactions = list(account.transactions_range(today, end_date, cleared=False))

    assert len(transactions) == 5
    assert transactions[0].description == "test repeating transaction with rrule"
    assert transactions[0].date == date(2023, 1, 1)


def test_account_running_balance(account: Account, today: date):
    end_date = today + relativedelta(months=3)
    balances = list(account.running_balance(today, end_date))

    assert len(balances) == 6
    assert balances[0].balance == Money(1011)
    assert balances[1].balance == Money(1111)
    assert balances[-1].balance == Money(3311)


def test_account_running_balance_cleared_true(account: Account, today: date):
    end_date = today + relativedelta(months=3)
    balances = list(account.running_balance(today, end_date, cleared=True))

    assert len(balances) == 1
    assert balances[0].balance == Money(1010)


def test_account_running_balance_cleared_false(account: Account, today: date):
    end_date = today + relativedelta(months=3)
    balances = list(account.running_balance(today, end_date, cleared=False))

    assert len(balances) == 5
    assert balances[0].balance == Money(101)
    assert balances[1].balance == Money(1101)
    assert balances[-1].balance == Money(2301)


def test_account_daily_balance_past(account: Account, today: date):
    start_date = today + relativedelta(months=-1)
    balances = list(account.daily_balance(start_date, today))

    assert len(balances) == 31
    assert balances[0] == (start_date, Money(0))
    assert balances[-1] == (today, Money(11))


def test_account_daily_balance_future(account: Account, today: date):
    end_date = today + relativedelta(months=1)
    balances = list(account.daily_balance(today, end_date))

    assert len(balances) == 32
    assert balances[0] == (today, Money(11))
    assert balances[9] == (date(2022, 12, 15), Money(11))
    assert balances[11] == (date(2022, 12, 17), Money(1011))
    assert balances[-1] == (end_date, Money(1111))


def test_account_daily_balance_cleared_true(account: Account, today: date):
    end_date = today + relativedelta(months=1)
    balances = list(account.daily_balance(today, end_date, cleared=True))

    assert len(balances) == 32
    assert balances[0] == (today, Money(10))
    assert balances[9] == (date(2022, 12, 15), Money(10))
    assert balances[11] == (date(2022, 12, 17), Money(1010))
    assert balances[-1] == (end_date, Money(1010))


def test_account_daily_balance_cleared_false(account: Account, today: date):
    end_date = today + relativedelta(months=1)
    balances = list(account.daily_balance(today, end_date, cleared=False))

    assert len(balances) == 32
    assert balances[0] == (today, Money(1))
    assert balances[9] == (date(2022, 12, 15), Money(1))
    assert balances[11] == (date(2022, 12, 17), Money(1))
    assert balances[-1] == (end_date, Money(101))
