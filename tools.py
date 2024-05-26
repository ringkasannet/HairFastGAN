import requests
import torch
from PIL import Image
import numpy as np
from utils.shape_predictor import align_face
from torchvision.utils import save_image


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

url="https://metro.co.uk/wp-content/uploads/2020/12/Alex-Cooper-3e3f.jpg"
tensor_image=image_to_tensors(url)
aligned=align_face(tensor_image,is_filepath=False, return_tensors=True)
output="/workspace/HairFastGAN/aligned/"
save_image(aligned,f'{output}fromTensor.png')


from utils.shape_predictor import align_face
from torchvision.utils import save_image

source="unaligned"
output="/workspace/HairFastGAN/aligned/"
for filename in os.listdir(source):
    full_filename=os.path.join(source, filename)
    if os.path.isfile(full_filename):
        base, ext = os.path.splitext(filename)
        aligned=align_face(full_filename,is_filepath=True, return_tensors=True)
        save_image(aligned,f'{output}{base}.png')
