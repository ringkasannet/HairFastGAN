print("downloading model and initiating server")
import time
start_time = time.time()

from flask import Flask, send_file, request, jsonify
from PIL import Image
from io import BytesIO
import requests
import os
from hair_swap import HairFast, get_parser
from torchvision.utils import save_image
import torch
from torchvision.transforms import ToPILImage

app = Flask(__name__)
app = Flask(__name__)

hair_fast = HairFast(get_parser().parse_args([]))
end_time=time.time()
elapsed_time=end_time-start_time
print(f"Time taken to download model: {elapsed_time} seconds")

# if __name__ == '__main__':
#     app.run_server(host='127.0.0.1', port='8050', debug=True)


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

@app.route("/",methods=['POST'])
def hello_world():
    return "<p>Hello, World!</p>"

from queue import Queue
request_queue = Queue()

@app.route("/check")
def chech_route():
    print("receiving checking request")
    request_queue.put("halo")
    while not request_queue.empty():
        print(f"queue size: {request_queue.qsize()}")
        request_queue.get()
        print("sleeping for 10 seconds")
        time.sleep(10)
        return "<p> check complete <p>"

from datetime import datetime

        
import os
from google.cloud import storage
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

@app.route('/convert', methods=['POST'])
def convert_images():
    print("receiving convert request....")
    torch.cuda.empty_cache()
    checkpoint1 = time.time()
    data = request.get_json()
    face_url = data.get('face')
    shape_url = data.get('shape')
    color_url = data.get('color')
    print(face_url,shape_url,color_url)
    if not all([face_url, shape_url, color_url]):
        return jsonify({"error": "Missing image URLs"}), 400

    urls = [face_url, shape_url, color_url]
    try:
        print("images found and valid, converting...")
        pil_images = download_and_convert_to_pils(urls)

        checkpoint2 = time.time()
        print(f"finished downloading and converting to pils, took {checkpoint2-checkpoint1}")
        
        result_images = hair_fast.swap(pil_images[0],pil_images[1],pil_images[2],align=True)
        checkpoint3 = time.time()
        print(f"finished swapping, took {checkpoint3-checkpoint2}")

        # for i in range(len(result_image)):
        #     print('saving images')
        #     if isinstance(result_image[i], torch.Tensor):
        #         save_image(result_image[i], f'/home/HairFastGAN/output/result{i}.png')
        # # else:
        #     # save_image(result_image, '/home/HairFastGAN/output/HairFast_result.png')
        #     # result_image.save('/home/HairFastGan/output/HairFast_result.png')
        # checkpoint4 = time.time()
        # for index,image in enumerate(result_images):
        #     if isinstance(image, torch.Tensor):
        #         # save_image(image,f'/workspace/HairFastGAN/out/{index}.png')
        #         image_byte=tensor_to_byte(result_images
                
        image_byte=tensor_to_byte(result_images[0])
        upload_blob_from_memory("barberfits-photo-bucket",image_byte,"output.png")
        url="https://storage.googleapis.com/barberfits-photo-bucket/output.png"
        return url
        return "success"
    except Exception as e:
        print("found error when swapping")
        print(e)
        return jsonify({'error': str(e)}), 500

from tools import url_to_aligned_tensor
@app.route('/processReferences', methods=['POST'])
def process_references():
    print("receiving convert request....")
    checkpoint1 = time.time()
    data = request.get_json()
    face_url = data.get('face')
    if not all([face_url]):
        return jsonify({"error": "Missing image URLs"}), 400
    aligned_face_tensor=url_to_aligned_tensor(face_url)
    
    reference_folder="aligned"
    image_urls=[]
    for filename in os.listdir(reference_folder):
        full_filename=os.path.join(reference_folder, filename)
        if os.path.isfile(full_filename):
            base, ext = os.path.splitext(filename)
            try:
                print("images found and valid, converting...")
                result_images = hair_fast.swap(aligned_face_tensor[0],full_filename,full_filename,align=False)
                image_byte=tensor_to_byte(result_images)
                upload_blob_from_memory("barberfits-photo-bucket",image_byte,"filename")
                image_urls.append(f"https://storage.googleapis.com/barberfits-photo-bucket/{filename}")
            except Exception as e:
                print("found error when swapping")
                print(e)
                return jsonify({'error': str(e)}), 500

    checkpoint3 = time.time()
    print(f"finished swapping, took {checkpoint3-checkpoint2}")            
    return image_urls


@app.route('/convertAligned', methods=['POST'])
def convert_images_aligned():
    print("receiving convert request....")
    torch.cuda.empty_cache()
    checkpoint1 = time.time()
    try:
        
        result_image = hair_fast.swap("/workspace/HairFastGAN/input/0.png","/workspace/HairFastGAN/input/1.png","/workspace/HairFastGAN/input/2.png")
        checkpoint2 = time.time()
        print(f"finished swapping, took {checkpoint2-checkpoint1}")

        # for i in range(len(result_image)):
        #     print('saving images')
        #     if isinstance(result_image[i], torch.Tensor):
        #         save_image(result_image[i], f'/home/HairFastGAN/output/result{i}.png')
        # # else:
        #     # save_image(result_image, '/home/HairFastGAN/output/HairFast_result.png')
        #     # result_image.save('/home/HairFastGan/output/HairFast_result.png')
        # checkpoint4 = time.time()
        if isinstance(result_image, torch.Tensor):
            image_byte=tensor_to_byte(result_image)
            # now = datetime.now() # current date and time
            # date_time = now.strftime("%H%M%S")
            checkpoint3 = time.time()

            print(f"finished converting to byte, took {checkpoint3-checkpoint2}, total time: {checkpoint3-checkpoint1}")

            # save_image(result_image,f'/workspace/HairFastGAN/output/{date_time}.png')
            return send_file(BytesIO(image_byte), mimetype='image/jpeg')
    except Exception as e:
        print("found error when swapping")
        print(e)
        return jsonify({'error': str(e)}), 500
# run command: gunicorn app:app -b :5000 -w 1

