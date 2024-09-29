from prefect import flow
from datetime import datetime
from base.tasks import process_cve_data, fetch_cve_data, get_last_update_time
import time

@flow
def update_cve_data_flow(store_in_db: bool = False):
    last_update_time = get_last_update_time()  # Retrieve last update timestamp
    current_time = datetime.now().isoformat()
    
    start_index = 0
    results_per_page = 100
    total_results = 10000  # Example total results
    
    # Construct the API URL with modification dates
    api_url = f"https://services.nvd.nist.gov/rest/json/cves/1.0?modStartDate={last_update_time}&modEndDate={current_time}"
    
    # Loop to fetch and process paginated CVE data
    while start_index < total_results:
        cve_data = fetch_cve_data(api_url, start_index, results_per_page).result()
        process_cve_data(cve_data, store_in_db)
        start_index += results_per_page
        
        # Sleep between requests to avoid rate limiting
        time.sleep(6)
