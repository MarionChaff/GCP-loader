from google.oauth2 import service_account
from google.cloud import storage
import os

class GCPFileUploader:

    def __init__ (self, credentials_path, bucket_name):
        self.credentials_path = credentials_path
        self.bucket_name = bucket_name

    def from_local_to_gcp (self, local_directory, gcp_directory):

        try:
            credentials = service_account.Credentials.from_service_account_file(self.credentials_path)
            storage_client = storage.Client(credentials = credentials)
            bucket = storage_client.bucket(self.bucket_name)
            print('GCP account initialized')

        except Exception as e:
            print(f"Error: {e}")

        try:

            files = [file for file in os.scandir(local_directory)]

            # Replace by the line below if you want to load only specific extensions
            #files = [file for file in os.scandir(local_directory) if file.name.endswith('.mid')]

            for k, file in enumerate(files):
                blob_path = os.path.join(gcp_directory, file)
                blob = bucket.blob(blob_path)
                blob.upload_from_filename(file)
                print(f'Upload {k + 1}/{len(files)} completed')

        except Exception as e:
            print(f"Error: {e}")

        return None
