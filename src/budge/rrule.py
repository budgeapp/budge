from dataclasses import dataclass, field
from datetime import date, datetime, time
from typing import List

import dateutil.rrule

date_format = "%Y%m%dT%H%M%S"


@dataclass(unsafe_hash=True)
class rruleset:
    _rruleset: dateutil.rrule.rruleset = field(
        default_factory=dateutil.rrule.rruleset, hash=True
    )

    def rrule(self, rrule: dateutil.rrule.rrule):
        self._rruleset.rrule(rrule)

    def rdate(self, rdate: date | datetime):
        self._rruleset.rdate(self._combine(rdate))

    def exrule(self, rrule: dateutil.rrule.rrule):
        self._rruleset.exrule(rrule)

    def exdate(self, exdate: date | datetime):
        self._rruleset.exdate(self._combine(exdate))

    def _combine(self, d: date | datetime):
        return d if isinstance(d, datetime) else datetime.combine(d, time(0, 0))

    @property
    def _rrule(self) -> List[dateutil.rrule.rrule]: ...

    @property
    def _rdate(self) -> List[date]: ...

    @property
    def _exrule(self) -> List[dateutil.rrule.rrule]: ...

    @property
    def _exdate(self) -> List[date]: ...

    def __getattr__(self, name):
        return self._rruleset.__getattribute__(name)

    def __iter__(self):
        yield from self._rruleset

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


def rrulestr(s: str, **kwargs):
    rule = dateutil.rrule.rrulestr(s, **kwargs)

    return rruleset(rule) if isinstance(rule, dateutil.rrule.rruleset) else rule
