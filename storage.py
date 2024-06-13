from google.cloud import storage
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import tools
from torchvision.utils import save_image


os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="barberfits-visualizer-8410bd16f96c.json"

cred = credentials.Certificate('/workspace/HairFastGAN/barberfits-visualizer-8410bd16f96c.json')

app = firebase_admin.initialize_app(cred)

db = firestore.client()


# Create a callback on_snapshot function to capture changes
def on_snapshot(doc_snapshot, changes, read_time):
    file_names_reference_folder=[]
    for filename in os.listdir("references"):
        full_filename=os.path.join("references", filename)
        if os.path.isfile(full_filename):
            base, ext = os.path.splitext(filename)
            file_names_reference_folder.append(base)
    print("files in folder:",file_names_reference_folder)

    file_names_firestore=[]
    for doc in doc_snapshot:
        url=doc.to_dict().get('url')
        if (url):
            file_name=tools.get_file_name_from_url(url)
            if file_name not in file_names_reference_folder:
                save_aligned_image_from_url(url)
            file_names_firestore.append(file_name)
    print("files in firestore:",file_names_firestore)


    for file_name in file_names_reference_folder:
        if file_name not in file_names_firestore:
            print("deleting", file_name)
            os.remove(os.path.join("/workspace/HairFastGAN/references/", file_name + ".png"))  # Assuming JPG 


doc_ref = db.collection("references")
doc_watch = doc_ref.on_snapshot(on_snapshot)

def save_aligned_image_from_url(url):
    file_name=tools.get_file_name_from_url(url)
    print('adding image, getting aligned image from url:',url,file_name)
    aligned=tools.url_to_aligned_tensor(url)
    save_image(aligned,f'/workspace/HairFastGAN/references/{file_name}.png')

    
            

def upload_blob_from_memory(bucket_name, contents, destination_blob_name):
    """Uploads a file to the bucket."""

    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"

    # The contents to upload to the file
    # contents = "these are my contents"

    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(contents)

    print(
        f"{destination_blob_name} uploaded to {bucket_name}."
    )


def upload_file(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Optional: set a generation-match precondition to avoid potential race conditions
    # and data corruptions. The request to upload is aborted if the object's
    # generation number does not match your precondition. For a destination
    # object that does not yet exist, set the if_generation_match precondition to 0.
    # If the destination object already exists in your bucket, set instead a
    # generation-match precondition using its generation number.
    generation_match_precondition = 0

    blob.upload_from_filename(source_file_name, if_generation_match=generation_match_precondition)

    print(
        f"File {source_file_name} uploaded to {destination_blob_name}."
    )


def delete_file(folder_path, file_name):
  """Deletes a file from a given folder.

  Args:
    folder_path: The path to the folder containing the file.
    file_name: The name of the file to delete.
  """

  file_path = os.path.join(folder_path, file_name)

  # Check if the file exists
  if os.path.exists(file_path):
    os.remove(file_path)
    print(f"File '{file_name}' deleted successfully from '{folder_path}'.")
  else:
    print(f"File '{file_name}' not found in '{folder_path}'.")