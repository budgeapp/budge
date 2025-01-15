from datetime import date

import dateutil.rrule
from dateutil.rrule import MONTHLY
from pytest import fixture

import budge.rrule


@fixture(scope="session")
def today():
    return date(2022, 12, 6)


@fixture(scope="session")
def rrule(today: date):
    return dateutil.rrule.rrule(MONTHLY, bymonthday=1, dtstart=today)


@fixture(scope="session")
def rruleset(today: date):
    ruleset = budge.rrule.rruleset()

    ruleset.rrule(dateutil.rrule.rrule(freq=MONTHLY, bymonthday=15, dtstart=today))
    ruleset.rdate(date(2022, 12, 17))
    ruleset.exdate(date(2022, 12, 15))
    ruleset.exrule(dateutil.rrule.rrule(freq=MONTHLY, bymonthday=20))

    return ruleset
