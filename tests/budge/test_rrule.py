import budge.rrule


def test_rruleset_str(rruleset: budge.rrule.rruleset):
    assert str(rruleset) == (
        "DTSTART:20221206T000000\n"
        "RRULE:FREQ=MONTHLY;BYMONTHDAY=15\n"
        "RDATE:20221217T000000\n"
        "EXRULE:FREQ=MONTHLY;BYMONTHDAY=20\n"
        "EXDATE:20221215T000000"
    )
