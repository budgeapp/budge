from decimal import Decimal
from typing import Any, Union

from stockholm import Money, MoneyType
from stockholm.money import MoneyModel

IntoMoneyType = Union[MoneyType, MoneyModel[Any], Decimal, int, float, str, object]


class IntoMoney:
    def __set_name__(self, owner: Any, name: str):
        self._name = "_" + name

    def __get__(self, instance, owner=None) -> Money:
        return getattr(instance, self._name)

    def __set__(self, instance, value: IntoMoneyType):
        setattr(instance, self._name, Money(value))
