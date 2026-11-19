import requests
from prefect import task

from base.config import settings

_session = requests.Session()
if settings.nvd_api_key:
    _session.headers["apiKey"] = settings.nvd_api_key


@task(retries=3, retry_delay_seconds=[30, 60, 120])
def fetch_cve_data(params: dict) -> dict:
    response = _session.get(settings.nvd_api_url, params=params, timeout=60)
    response.raise_for_status()
    return response.json()


@task
def process_cve_data(cve_data: dict) -> int:
    vulnerabilities = cve_data.get("vulnerabilities", [])
    for item in vulnerabilities:
        cve = item["cve"]
        description = next(
            (d["value"] for d in cve.get("descriptions", []) if d.get("lang") == "en"),
            "",
        )
        print(f"CVE ID: {cve['id']}, Description: {description}")
    return len(vulnerabilities)