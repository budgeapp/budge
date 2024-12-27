from collections.abc import Callable
from decimal import Decimal
from typing import Any

from stockholm import Money
from stockholm.money import MoneyModel

type IntoMoneyType = MoneyModel[Money] | Decimal | int | float | str

type IntoMoneyCallback = Callable[[Any], IntoMoneyType]


class IntoMoney:
    def __set_name__(self, owner: Any, name: str):
        self._name = "_" + name

    def __get__(self, instance: Any, owner=None) -> Money:
        attr: Money | IntoMoneyCallback = getattr(instance, self._name)

        if isinstance(attr, Money):
            return attr

        return Money(attr(instance))

    def __set__(self, instance, value: IntoMoneyType | IntoMoneyCallback):
        if not callable(value):
            value = Money(value)

        setattr(instance, self._name, value)
