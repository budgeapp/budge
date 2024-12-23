# Changelog

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
