from pytest import fixture

import budge.rrule


@fixture
def rrulestr():
    return (
        "DTSTART:20221206T000000\n"
        "RRULE:FREQ=MONTHLY;BYMONTHDAY=15\n"
        "RDATE:20221217T000000\n"
        "EXRULE:FREQ=MONTHLY;BYMONTHDAY=20\n"
        "EXDATE:20221215T000000"
    )


def test_rruleset_str(rruleset: budge.rrule.rruleset, rrulestr):
    assert str(rruleset) == rrulestr


def test_rrulestr(rruleset, rrulestr):
    from_rrulestr = budge.rrule.rrulestr(rrulestr)

    assert isinstance(from_rrulestr, budge.rrule.rruleset)
    assert str(from_rrulestr) == str(rruleset)
