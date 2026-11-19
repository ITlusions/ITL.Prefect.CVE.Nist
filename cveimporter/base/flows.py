import time
from datetime import datetime, timedelta, timezone

from prefect import flow
from prefect.variables import Variable

from base.config import settings
from base.tasks import fetch_cve_data, process_cve_data

WATERMARK_VARIABLE = "nist_cve_last_update"
DEFAULT_START = datetime(2024, 9, 22, tzinfo=timezone.utc)
WINDOW = timedelta(days=90)  # NVD rejects modification windows longer than 120 days
PAGE_SIZE = 2000  # NVD maximum resultsPerPage


def _nvd_date(moment: datetime) -> str:
    return moment.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000+00:00")


@flow(name="update-cve-data-flow")
def update_cve_data_flow() -> int:
    now = datetime.now(timezone.utc)
    last_update = datetime.fromisoformat(
        Variable.get(WATERMARK_VARIABLE, default=DEFAULT_START.isoformat())
    )
    delay = 0.6 if settings.nvd_api_key else 6.0
    total = 0
    window_start = last_update

    while window_start < now:
        window_end = min(window_start + WINDOW, now)
        start_index = 0
        while True:
            page = fetch_cve_data({
                "lastModStartDate": _nvd_date(window_start),
                "lastModEndDate": _nvd_date(window_end),
                "startIndex": start_index,
                "resultsPerPage": PAGE_SIZE,
            })
            total += process_cve_data(page)
            start_index += PAGE_SIZE
            if start_index >= page.get("totalResults", 0):
                break
            time.sleep(delay)
        Variable.set(WATERMARK_VARIABLE, window_end.isoformat(), overwrite=True)
        window_start = window_end
        if window_start < now:
            time.sleep(delay)

    return total