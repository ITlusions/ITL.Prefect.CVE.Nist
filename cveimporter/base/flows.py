from prefect import flow
from datetime import datetime
from base.tasks import process_cve_data, fetch_cve_data, get_last_update_time
from base.config import settings
import time

@flow
def update_cve_data_flow(store_in_db: bool = False):
    last_update_time = get_last_update_time()  # Retrieve last update timestamp
    current_time = datetime.now().isoformat()
    
    start_index = 0
    results_per_page = 50
    total_results = 10000  # Example total results
    
    # Construct the API URL with modification dates
    api_url = f"{settings.nvd_api_url}?lastModStartDate={last_update_time}&lastModEndDate={current_time}"
    
    # Determine the rate limit sleep time based on API key presence
    if settings.nvd_api_key:
        rate_limit_sleep_time = 0.6  # Sleep time for 50 requests in 30 seconds
    else:
        rate_limit_sleep_time = 6.0  # Sleep time for 5 requests in 30 seconds

    # Loop to fetch and process paginated CVE data
    while start_index < total_results:
        cve_data = fetch_cve_data(api_url, start_index, results_per_page)
        process_cve_data(cve_data, store_in_db)
        
        start_index += results_per_page
        
        # Sleep based on the determined rate limit to avoid hitting the limit
        time.sleep(rate_limit_sleep_time)  # Adjust based on the API's rate limit guidelines
