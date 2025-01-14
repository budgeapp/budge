from decimal import Decimal

from stockholm import Money
from stockholm.money import MoneyModel

type IntoMoneyType = MoneyModel[Money] | Decimal | int | float | str


class IntoMoney:
    def __set_name__(self, owner, name: str):
        self._name = "_" + name

    def __get__(self, instance, owner=None) -> Money:
        return getattr(instance, self._name)

    def __set__(self, instance, value: IntoMoneyType):
        setattr(instance, self._name, Money(value))
