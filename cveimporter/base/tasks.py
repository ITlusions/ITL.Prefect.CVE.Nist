# linkedinjobs/base/tasks.py
import requests
from prefect import task
from base.config import settings

@task
def fetch_cves_from_nvd(start_date: str, end_date: str):
    params = {
        "pubStartDate": start_date,
        "pubEndDate": end_date,
    }
    response = requests.get(settings.nvd_api_url, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        cve_data = response.json()
        return cve_data
    else:
        raise Exception(f"Failed to fetch CVEs: {response.status_code}")

@task
def process_cve_data(cve_data):
    # For simplicity, print the first 5 CVEs
    cves = cve_data.get('vulnerabilities', [])
    for cve in cves[:5]:
        cve_id = cve['cve']['id']
        description = cve['cve']['descriptions'][0]['value']
        print(f"CVE ID: {cve_id}, Description: {description}")