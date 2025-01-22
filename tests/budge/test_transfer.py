from datetime import date

import dateutil.rrule
from dateutil.relativedelta import relativedelta
from pytest import fixture
from stockholm import Money

from budge import Account, RepeatingTransfer, Transfer


@fixture
def from_account():
    return Account("from account")


@fixture
def to_account():
    return Account("to account")


@fixture
def transfer(today: date, from_account: Account, to_account: Account):
    return Transfer(
        description="test transfer",
        amount=Money(100),
        date=today,
        from_account=from_account,
        to_account=to_account,
    )


@fixture
def repeating_transfer(
    rrule: dateutil.rrule.rrule, from_account: Account, to_account: Account
):
    return RepeatingTransfer(
        "test repeating transfer",
        Money(100),
        from_account=from_account,
        to_account=to_account,
        schedule=rrule,
    )


def test_transfer(
    today: date, transfer: Transfer, from_account: Account, to_account: Account
):
    assert transfer.from_transaction.amount == Money(-100)
    assert transfer.to_transaction.amount == Money(100)

    assert transfer.from_transaction.cleared is False
    assert transfer.to_transaction.cleared is False

    assert from_account.balance(today) == Money(-100)
    assert to_account.balance(today) == Money(100)


def test_repeating_transfer(
    today: date,
    repeating_transfer: RepeatingTransfer,
    from_account: Account,
    to_account: Account,
):
    repeating_transfer.last_cleared = today + relativedelta(months=3)

    assert repeating_transfer.from_transaction.amount == Money(-100)
    assert repeating_transfer.to_transaction.amount == Money(100)

    assert repeating_transfer.from_transaction.cleared is False
    assert repeating_transfer.to_transaction.cleared is False

    as_of = today + relativedelta(months=6)

    assert from_account.balance(as_of) == Money(-600)
    assert to_account.balance(as_of) == Money(600)

    assert from_account.balance(as_of, cleared=True) == Money(-300)
    assert to_account.balance(as_of, cleared=True) == Money(300)
