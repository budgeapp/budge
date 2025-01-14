from dataclasses import dataclass

from pytest import raises
from stockholm import ConversionError, Money

from budge.money import IntoMoney


@dataclass
class IntoMoneyTest:
    amount: IntoMoney = IntoMoney()


def test_into_money_from_int():
    obj = IntoMoneyTest(100)
    assert isinstance(obj.amount, Money)
    assert obj.amount == Money(100)


def test_into_money_from_str():
    obj = IntoMoneyTest("100")
    assert isinstance(obj.amount, Money)
    assert obj.amount == Money(100)


def test_into_money_from_empty_string():
    with raises(ConversionError, match="Missing input values for monetary amount"):
        IntoMoneyTest("")
