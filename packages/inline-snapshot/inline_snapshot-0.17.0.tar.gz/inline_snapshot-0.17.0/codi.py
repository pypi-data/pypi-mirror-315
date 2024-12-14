
import datetime as dt
import uuid

import attrs

from dirty_equals import IsDatetime
from inline_snapshot import Is, snapshot


@attrs.define
class Attrs:
    ts: dt.datetime
    id: uuid.UUID


print(attrs.has(Attrs))


def test():
    id = uuid.uuid4()

    # Simple values work.
    assert snapshot(Attrs(ts=1, id=2)) == Attrs(1, 2)

    # Wrapped value don't work.
    assert snapshot(Attrs(ts=IsDatetime(), id=Is(id))) == Attrs(
        dt.datetime.now(), id
    )
