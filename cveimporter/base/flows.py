from prefect import flow
from datetime import datetime
from base.tasks import fetch_cves_from_nvd, process_cve_data

@flow
def nvd_cve_flow():
    # Example: Get CVEs published in the last 7 days
    today = datetime.now().date()
    start_date = f"{today}T00:00:00:000 UTC-00:00"
    end_date = f"{today}T23:59:59:000 UTC-00:00"
    
    # Fetch CVE data from NVD API
    cve_data = fetch_cves_from_nvd(start_date, end_date)
    
    # Process the fetched CVE data
    process_cve_data(cve_data)
