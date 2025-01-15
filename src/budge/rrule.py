import datetime
from typing import List

import dateutil
import dateutil.rrule

date_format = "%Y%m%dT%H%M%S"


class rruleset(dateutil.rrule.rruleset):
    _rrule: List[dateutil.rrule.rrule] = []
    _rdate: List[datetime.date] = []
    _exrule: List[dateutil.rrule.rrule] = []
    _exdate: List[datetime.date] = []

    def __str__(self):
        rrule_strs = [str(rule) for rule in self._rrule]
        dtstart_lines = [line for line in rrule_strs if line.startswith("DTSTART")]

        rule = "\n".join({dtstart_lines[0], *rrule_strs})

        if self._rdate:
            rule += f"\nRDATE:{','.join(date.strftime(date_format) for date in self._rdate)}"

        if self._exrule:
            rule += "\n" + "\n".join(str(rule) for rule in self._exrule).replace(
                "RRULE", "EXRULE"
            )

        if self._exdate:
            rule += f"\nEXDATE:{','.join(date.strftime(date_format) for date in self._exdate)}"

        return rule
