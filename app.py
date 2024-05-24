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
        
        result_image = hair_fast.swap(pil_images[0],pil_images[1],pil_images[2],align=True)[0]
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
        if isinstance(result_image, torch.Tensor):
            image_byte=tensor_to_byte(result_image)
            now = datetime.now() # current date and time
            date_time = now.strftime("%H%M%S")
            save_image(result_image,f'/home/HairFastGAN/output/{date_time}.png')
            # return send_file(BytesIO(image_byte), mimetype='image/jpeg')
        return "<p> succeded </p>"
    except Exception as e:
        print("found error when swapping")
        print(e)
        return jsonify({'error': str(e)}), 500


# run command: gunicorn app:app -b :5000 -w 2

