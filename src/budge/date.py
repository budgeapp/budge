from datetime import date, timedelta


def daterange(start_date: date, end_date: date):
    """Iterate over a range of dates, inclusive of the start and end dates."""
    return (
        start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)
    )
