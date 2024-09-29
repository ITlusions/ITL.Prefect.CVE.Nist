import requests
from prefect import task
from base.config import settings

# Fetch CVE data from NVD API
@task
def fetch_cve_data(api_url, start_index, results_per_page):
    headers = {}
    
    # Check if the API key is provided and add it to the headers
    if settings.nvd_api_key:  
        headers['apiKey'] = settings.nvd_api_key  

    # Make the API request with headers
    response = requests.get(f"{api_url}&startIndex={start_index}&resultsPerPage={results_per_page}", headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch CVEs: {response.status_code}")

# Process CVE data, optionally store in Cassandra
@task
def process_cve_data(cve_data, store_in_db: bool = False):
    cves = cve_data.get('vulnerabilities', [])
    
    # Loop through CVE data for processing
    for cve in cves:
        cve_id = cve['cve']['id']
        description = cve['cve']['descriptions'][0]['value']
        print(f"CVE ID: {cve_id}, Description: {description}")
        
        # Optional storage in Cassandra
        if store_in_db:
            cluster = Cluster(['127.0.0.1']) 
            session = cluster.connect('cve_keyspace')
            
            insert_query = """
            INSERT INTO cve_data (cve_id, description)
            VALUES (%s, %s)
            """
            session.execute(insert_query, (cve_id, description))
            session.shutdown()

# Function to get the last update timestamp (you can store this in a file or DB)
def get_last_update_time():
    # Placeholder: Retrieve the last update time (e.g., from a file or database)
    return "2024-09-22T00:00:00"