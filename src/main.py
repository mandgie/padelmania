import numpy as np
import cv2
import time
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

file_name = 'test_film.avi'
key_path = "/Users/magnusfriberg/secrets/padelmania.json"


cap = cv2.VideoCapture(0)
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(file_name,fourcc, 20.0, (frame_width, frame_height))

t0 = time.time()

while(cap.isOpened()):
    t1 = time.time()
    ret, frame = cap.read()
    if ret==True:
        # frame = cv2.flip(frame,0)

        # write the flipped frame
        out.write(frame)

        cv2.imshow('frame',frame)
        num_sec = t1 - t0
        if num_sec > 15:
            break
    else:
        break

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()

# Give time for video to be loaded
time.sleep(30)

# Upload to cloud storage
upload_blob(bucket_name='padelmania-films', source_file_name=file_name, destination_blob_name=file_name, key_path=key_path)
