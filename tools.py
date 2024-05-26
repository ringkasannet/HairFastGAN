import requests
import torch
from PIL import Image
import numpy as np
from utils.shape_predictor import align_face
from torchvision.utils import save_image
import requests
import os
from google.cloud import storage
import re
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="barberfits-visualizer-8410bd16f96c.json"

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

def url_to_aligned_tensor(url):
    tensor_image=image_to_tensors(url)
    aligned=align_face(tensor_image,is_filepath=False, return_tensors=True)
    return aligned
    

def image_to_tensors(url):
  """Reads an image from a URL and converts it to a list of PyTorch tensors.

  Args:
      url (str): The URL of the image.

  Returns:
      list: A list of PyTorch tensors representing the image.
  """

  # Download the image from the URL
  response = requests.get(url, stream=True)
  response.raise_for_status()  # Raise an exception for bad status codes

  # Open the image with PIL
  image = Image.open(response.raw)

  # Convert the image to RGB mode if it's not already
  if image.mode != "RGB":
    image = image.convert("RGB")

  # Convert the image to a PyTorch tensor
  tensor = torch.from_numpy(
      np.array(image).astype(np.float32).transpose((2, 0, 1))
  ) / 255.0

  # Return the tensor as a list (for convenience)
  return [tensor] 

# url="https://metro.co.uk/wp-content/uploads/2020/12/Alex-Cooper-3e3f.jpg"
# tensor_image=image_to_tensors(url)
# aligned=align_face(tensor_image,is_filepath=False, return_tensors=True)
# output="/workspace/HairFastGAN/aligned/"
# save_image(aligned,f'{output}fromTensor.png')


def get_file_name_from_url(url):
    match = re.search(r'/([^/]+)\.(png|jpg)$', url)
    if match:
      return match.group(1)
    else:
        return None

# print(get_file_name_from_url(url))

# from utils.shape_predictor import align_face
# from torchvision.utils import save_image

# source="unaligned"
# output="/workspace/HairFastGAN/aligned/"
# for filename in os.listdir(source):
#     full_filename=os.path.join(source, filename)
#     if os.path.isfile(full_filename):
#         base, ext = os.path.splitext(filename)
#         aligned=align_face(full_filename,is_filepath=True, return_tensors=True)
#         save_image(aligned,f'{output}{base}.png')
