import logging
import json
from hcs_core.sglib.client_util import hdc_service_client
from hcs_core.ctxp import timeutil
from hcs_core.util.lru import LRUSet

log = logging.getLogger(__name__)


def _client():
    return hdc_service_client("hoc-diagnostic")


def _hash(o):
    return json.dumps(o).__hash__()


_temp_dedup = LRUSet(10000)


def _check_dup(o):
    h = _hash(o)
    if h in _temp_dedup:
        return True
    _temp_dedup.add(h)


def search(payload: dict, size: int = 100):

    pointer_timestamp = timeutil.iso_date_to_timestamp(payload["from"])
    end_timestamp = timeutil.iso_date_to_timestamp(payload["to"])

    count = 0
    while pointer_timestamp < end_timestamp and count < size:

        payload["from"] = timeutil.timestamp_to_iso_date(pointer_timestamp)
        log.info(f"range: from={payload['from']}, to={payload['to']}")

        page = _client().post("/v1/data/search", json=payload)
        if not page:
            break

        if isinstance(page, str):
            page = json.loads(page)

        if not page:
            break

        # _old = count
        for item in page:

            data = item["data"]
            if _check_dup(data):
                continue

            count += 1
            yield data

            if count >= size:
                break

            pointer_timestamp = max(data["d"]["utcTime"] + 1, pointer_timestamp + 1000)

        # log.info(f"events={count - _old}")
