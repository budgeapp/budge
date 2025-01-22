# Changelog

## v1.2.0 (2025-01-21)

- Add `Transaction.cleared` boolean field.
- Add `RepeatingTransaction.last_cleared` date field. All `Transactions` yielded
  will have their `cleared` field set to true if the date is before the value of
  `last_cleared`. The same rule applies to `RepeatingTransfer`.
- Add `cleared: bool | None` parameters to `Account` methods, where a non-`None`
  value filters account transactions by the given value for `cleared`.

## v1.1.1 (2025-01-13)

- Removed the ability to set a transaction's amount to a callback until I've
  redesigned how that functionality should work.

## v1.1.0 (2025-01-11)

- Added `Account.running_balance` that iterates through each transaction in an
  account for the given date range, and includes the current running balance of
  the account.

## v1.0.0 (2024-12-27)

- Accept any value that can be passed to the constructor of `stockholm.Money`
  wherever a `Money` object was required as an argument.
- Accept a function that accepts the object instance as an argument and returns
  a `Money`-convertible value as an `amount` parameter.
- Swapped positions of the `amount` and `description` fields on `Transaction`.

## v0.6.0 (2024-12-25)

- Set account property on `Transaction` objects generated from
  `RepeatingTransaction` objects.
- Allow `dateutil.rrule.rruleset` in `RepeatingTransaction.schedule` and
  `RepeatingTransfer.schedule`.
- Refactor internal storage of `Collection` instances to use `dict`.
- Exclude `Transaction` objects generated from a `RepeatingTransaction` when
  iterating over an account's transactions, if a manually entered `Transaction`
  matches the generated `Transaction`.

## v0.5.0 (2024-12-23)

- Refactored `Account.transactions` and `Account.repeating_transactions` to a
  `Collection` class that assigns parent references on child items.
- Refactored generators to prefer `yield from` over returning a generator.

## v0.4.0 (2024-12-11)

- Added `Account.daily_balance` to iterate through account balance by date.
- Renamed `RecurringTransaction` and `RecurringTransfer` to
  `RepeatingTransaction` and `RepeatingTransfer`.

## v0.3.0 (2024-12-08)

- Added `RecurringTransfer` model.

## v0.2.0 (2024-12-08)

- Added `Transfer` model for transfers between accounts.
- Renamed `RecurringTransaction.rrule` to `RecurringTransaction.schedule`.

## v0.1.0 (2024-12-06)

- Initial release.
