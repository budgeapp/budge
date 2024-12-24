from datetime import date, timedelta
from typing import Generator


def daterange(start_date: date, end_date: date) -> Generator[date]:
    """Iterate over a range of dates, inclusive of the start and end dates."""
    yield from (
        start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)
    )
