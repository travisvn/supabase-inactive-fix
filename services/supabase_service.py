# services/supabase_service.py

from supabase import create_client, Client


class SupabaseClient:
    def __init__(self, url, key, table_name):
        if not url or not key:
            raise ValueError("Supabase URL and Key must be provided.")

        self.client: Client = create_client(url, key)
        self.table_name = table_name

    def insert_random_name(self, random_name):
        data = {'name': random_name}
        try:
            response = self.client.table(self.table_name).insert(data).execute()
            print(f"Inserted data into '{self.table_name}': {response.data}")
            return True
        except Exception as e:
            print(f"Error inserting data into '{self.table_name}': {e}")
            return False

    def get_table_count(self):
        try:
            response = self.client.table(self.table_name).select('*', count='exact').execute()
            if response.count is not None:
                return response.count
            else:
                print(f"Could not retrieve count from '{self.table_name}'.")
                return None
        except Exception as e:
            print(f"Error counting data in '{self.table_name}': {e}")
            return None

    def delete_random_entry(self):
        try:
            # Fetch all IDs from the table
            response = self.client.table(self.table_name).select('id').execute()
            if response.data:
                ids = [item['id'] for item in response.data]
                if not ids:
                    print(f"No entries to delete in '{self.table_name}'.")
                    return True  # No deletion needed, but not an error

                # Randomly select one ID to delete
                import random
                random_id = random.choice(ids)

                # Delete the entry with the selected ID
                self.client.table(self.table_name).delete().eq('id', random_id).execute()
                print(f"Deleted entry with id {random_id} from '{self.table_name}'.")
                return True
            else:
                print(f"No data retrieved from '{self.table_name}'.")
                return False
        except Exception as e:
            print(f"Error deleting data from '{self.table_name}': {e}")
            return False
