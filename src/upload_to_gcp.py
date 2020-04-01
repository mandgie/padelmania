from google.cloud import storage
from google.oauth2 import service_account


def upload_blob(bucket_name, source_file_name, destination_blob_name, key_path):
    """Uploads a file to the bucket."""
    # bucket_name = "your-bucket-name"
    # source_file_name = "local/path/to/file"
    # destination_blob_name = "storage-object-name"

    credentials = service_account.Credentials.from_service_account_file(
    key_path,
    scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )

    storage_client = storage.Client(
        credentials=credentials,
        project=credentials.project_id,)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )

file_name = 'output.avi'

key_path = "/Users/magnusfriberg/secrets/padelmania.json"

upload_blob(bucket_name='padelmania-films', source_file_name=file_name, destination_blob_name=file_name, key_path=key_path)
