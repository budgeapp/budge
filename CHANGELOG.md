# Changelog

## v0.6.0 (unreleased)

- Set account property on `Transaction` objects generated from `RepeatingTransaction`
  objects.
- Allow `dateutil.rrule.rruleset` in `RepeatingTransaction.schedule` and
  `RepeatingTransfer.schedule`.
- Refactor internal storage of `Collection` instances to use `dict`.
- Exclude `Transaction` objects generated from a `RepeatingTransaction` when iterating
  over an account's transactions, if a manually entered `Transaction` matches the
  generated `Transaction`.

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
