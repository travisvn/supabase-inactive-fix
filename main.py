# main.py

import json
import os
import logging
from helpers.utils import generate_secure_random_string
from services.supabase_service import SupabaseClient

# User-defined variables to toggle additional features
log_failed_databases = True  # Set to True to log failed databases
detailed_status_report = True  # Set to True to generate a detailed status report

# Configure logging with timestamp
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def main():
    # Load configurations from config.json
    try:
        with open('config.json', 'r') as config_file:
            configs = json.load(config_file)
    except FileNotFoundError:
        logging.error("Configuration file 'config.json' not found.")
        return
    except json.JSONDecodeError as e:
        logging.error(f"Error parsing 'config.json': {e}")
        return

    all_successful = True  # Flag to track overall success

    # Initialize lists for additional features
    failed_databases = [] if log_failed_databases else None
    status_report = [] if detailed_status_report else None

    # Iterate over each configuration
    for config in configs:
        name = config.get('name', 'Unnamed Database')
        url = config.get('supabase_url')
        key = config.get('supabase_key')
        table_name = config.get('table_name', 'KeepAlive')

        # If using environment variables for keys
        key_env_var = config.get('supabase_key_env')
        if key_env_var:
            key = os.getenv(key_env_var)

        if not url or not key:
            logging.error(f"Supabase URL or Key missing for '{name}'. Skipping.")
            all_successful = False
            if log_failed_databases:
                failed_databases.append(name)
            continue

        logging.info(f"Processing database: {name}")

        # Initialize Supabase client for this configuration
        supabase_client = SupabaseClient(url, key, table_name)

        # Generate a random string
        random_name = generate_secure_random_string(10)

        # Insert the random name into the table
        success_insert = supabase_client.insert_random_name(random_name)
        if not success_insert:
            all_successful = False
            if log_failed_databases:
                failed_databases.append(name)
            # Proceed to next database since insertion failed
            continue

        # Get the count of entries in the table
        count = supabase_client.get_table_count()
        if count is None:
            logging.error(f"Failed to get count for table '{table_name}' in database '{name}'.")
            all_successful = False
            if log_failed_databases:
                failed_databases.append(name)
            continue  # Skip to next configuration

        logging.info(f"Current number of entries in '{table_name}': {count}")

        # Initialize success_delete to None
        success_delete = None

        # If there are more than 10 entries, delete a random one
        if count > 10:
            logging.info(f"Table '{table_name}' has more than 10 entries. Deleting a random entry.")
            success_delete = supabase_client.delete_random_entry()
            if not success_delete:
                all_successful = False
                if log_failed_databases and name not in failed_databases:
                    failed_databases.append(name)
        else:
            logging.info(f"Table '{table_name}' has 10 or fewer entries. No deletion needed.")

        # Collect status information
        if detailed_status_report:
            status = {
                'name': name,
                'success_insert': success_insert,
                'success_delete': success_delete,
                'count': count
            }
            status_report.append(status)

    # After processing all configurations
    if all_successful:
        logging.info("All database actions were successful.")
    else:
        logging.warning("Some database actions failed.")

        if log_failed_databases and failed_databases:
            logging.warning("Failed databases:")
            for db_name in failed_databases:
                logging.warning(f"- {db_name}")

    if detailed_status_report and status_report:
        logging.info("\nDetailed Status Report:")
        for status in status_report:
            logging.info(f"Database: {status['name']}")
            logging.info(f"  Insert Success: {status['success_insert']}")
            logging.info(f"  Entry Count: {status['count']}")
            if status['success_delete'] is not None:
                logging.info(f"  Delete Success: {status['success_delete']}")
            else:
                logging.info("  Delete Success: N/A")


if __name__ == "__main__":
    main()
