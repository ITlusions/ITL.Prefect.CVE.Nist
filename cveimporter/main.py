from base.flows import update_cve_data_flow

if __name__ == "__main__":
    print('Starting Flow')
    
    # Call the flow without storing in Cassandra
    update_cve_data_flow(store_in_db=False)

    # Or, to store in Cassandra, use:
    # update_cve_data_flow(store_in_db=True)