from dataclasses import InitVar, dataclass, field

from .account import Account
from .transaction import Transaction


@dataclass(kw_only=True)
class Transfer(Transaction):
    """Record of a transfer between two accounts."""

    from_account: InitVar[Account]
    to_account: InitVar[Account]
    from_transaction: Transaction = field(init=False)
    to_transaction: Transaction = field(init=False)

    def __post_init__(self, from_account: Account, to_account: Account):
        """
        Create the from and to transactions, add them to the respective accounts,
        and set their parent to this transfer.
        """
        self.from_transaction = Transaction(-self.amount, self.description, self.date)
        self.to_transaction = Transaction(self.amount, self.description, self.date)

        self.from_transaction.parent = self.to_transaction.parent = self

        from_account.transactions.append(self.from_transaction)
        to_account.transactions.append(self.to_transaction)
