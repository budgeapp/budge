from datetime import date

from dateutil.relativedelta import relativedelta

from budge.date import daterange


def test_daterange():
    start_date = date(2022, 12, 28)
    end_date = start_date + relativedelta(weeks=1)

    dates = list(daterange(start_date, end_date))

    assert dates == [
        date(2022, 12, 28),
        date(2022, 12, 29),
        date(2022, 12, 30),
        date(2022, 12, 31),
        date(2023, 1, 1),
        date(2023, 1, 2),
        date(2023, 1, 3),
        date(2023, 1, 4),
    ]
