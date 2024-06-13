import requests
import torch
from PIL import Image
import numpy as np
from utils.shape_predictor import align_face
from torchvision.utils import save_image
import requests
import os
import re
from io import BytesIO
from torchvision.transforms import ToPILImage




def url_to_aligned_tensor(url):
    tensor_image=url_to_tensor(url)
    aligned=align_face(tensor_image,is_filepath=False, return_tensors=True)
    return aligned
    

def url_to_tensor(url):
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

 
def get_file_name_from_url(url):
    match = re.search(r'/([^/]+)\.(png|jpg)$', url)
    if match:
      return match.group(1)
    else:
        return None


def download_and_convert_to_pil(url):
    response = requests.get(url, allow_redirects=True, headers={"User-Agent": "Mozilla/5.0"})
    img = Image.open(BytesIO(response.content))
    return img

def tensor_to_byte(tensor):
    """Converts a PyTorch tensor to a PIL Image."""
    to_pil = ToPILImage()
    pil_image= to_pil(tensor)
    buffer = BytesIO()
    pil_image.save(buffer, format="JPEG")
    return buffer.getvalue()
    
def download_and_convert_to_pils(urls):
    pil_images = []
    for url in urls:
        response = requests.get(url, allow_redirects=True, headers={"User-Agent": "Mozilla/5.0"})
        img = Image.open(BytesIO(response.content))
        pil_images.append(img)
        print(f"Downloaded an image of size {img.size}")
    return pil_images

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
