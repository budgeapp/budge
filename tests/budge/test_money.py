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


def test_into_money_with_callable():
    def get_amount(instance: IntoMoneyTest):
        assert instance is obj
        return Money(100)

    obj = IntoMoneyTest(get_amount)
    assert isinstance(obj.amount, Money)
    assert obj.amount == Money(100)


def test_into_money_with_wrong_callable_type():
    def wrong_function(instance: IntoMoneyTest):
        return "can't convert this to Money"

    obj = IntoMoneyTest(wrong_function)
    with raises(ConversionError, match="Input value cannot be used as monetary amount"):
        obj.amount
