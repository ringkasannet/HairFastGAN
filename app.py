print("downloading model and initiating server")
import time
start_time = time.time()

from flask import Flask, send_file, request, jsonify, stream_with_context
from PIL import Image
from io import BytesIO
import requests
import os
from hair_swap import HairFast, get_parser
from torchvision.utils import save_image
import torch
import tools
import storage
import json

app = Flask(__name__)

hair_fast = HairFast(get_parser().parse_args([]))
end_time=time.time()
elapsed_time=end_time-start_time
print(f"Time taken to download model: {elapsed_time} seconds")

@app.route("/health",methods=['GET'])
def health_check():
    print("checking for health")
    response = {"healthy": True}
    yield "1"
    return jsonify(response), 200, {'Content-Type': 'application/json'}

@app.route("/",methods=['GET'])
def home():
    print("we are called in home")
    return "in home"        

@app.route("/check-references",methods=['GET'])
def check_references():
    print("we are called in home")
    return "in home"        


@app.route('/convert', methods=['POST'])
def convert_images():
    print("receiving convert request....")
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
        
        image_byte=tools.tensor_to_byte(result_images[0])
        storage.upload_blob_from_memory("barberfits-photo-bucket",image_byte,"output.png")
        url="https://storage.googleapis.com/barberfits-photo-bucket/output.png"
        return url
        return "success"
    except Exception as e:
        print("found error when swapping")
        print(e)
        return jsonify({'error': str(e)}), 500

@app.route('/reference', methods=['POST'])
def add_reference():
    reference_url=request.get_json().get('ref')
    file_name=tools.get_file_name_from_url(reference_url)
    print("adding reference:",file_name)
    ref_tensor=tools.url_to_aligned_tensor(reference_url)
    save_image(ref_tensor, f'/workspace/HairFastGAN/references/{file_name}.png')
    return jsonify({"success":True})

@app.route('/reference/<item_id>', methods=['DELETE'])
def delete_reference(item_id):
    folder_name="/workspace/HairFastGAN/references"
    file_name=f"{item_id}.png"
    storage.delete_file(folder_name,file_name)
    return {"success":True}


@app.route('/process-references', methods=['POST'])
def process_references():

    def process_references_generator():
        checkpoint1 = time.time()
        face_url = request.get_json().get('face')
        id=request.get_json().get('id')
        if not face_url:
            return jsonify({"error": "Missing image URLs"}), 400
    
        aligned_face_tensor=tools.url_to_aligned_tensor(face_url)
        face_url_file_name=tools.get_file_name_from_url(face_url)
        print("receiving convert request....",face_url_file_name)

        reference_folder="references"
        image_urls=[]
        i=0
        for filename in os.listdir(reference_folder):
            full_filename=os.path.join(reference_folder, filename)
            if os.path.isfile(full_filename):
                base, ext = os.path.splitext(filename)
                try:
                    print("images found and valid, converting...")
                    result_images = hair_fast.swap(aligned_face_tensor[0],full_filename,full_filename,align=False)
                    image_byte=tools.tensor_to_byte(result_images)
                    storage.upload_blob_from_memory("barberfits-photo-bucket",image_byte,f"result/{id}/{base}.png")
                    i=i+1
                    # yield jsonify({"id":base,"url":f"https://storage.googleapis.com/barberfits-photo-bucket/result/{id}/{base}.png"})
                    yield json.dumps({"id": base, "url": f"https://storage.googleapis.com/barberfits-photo-bucket/result/{id}/{base}.png"}).encode('utf-8')
                except Exception as e:
                    print("found error when swapping")
                    print(e)
                    return jsonify({'error': str(e)}), 500

        checkpoint2 = time.time()
        print(f"finished swapping, took {checkpoint2-checkpoint1}")            
    # return image_urls
    return stream_with_context(process_references_generator())

@app.route('/references/<id>',methods=['POST'])
def changeReferences():
    return {id:id,url:request.args.url}
    
@app.route('/convert-aligned', methods=['POST'])
def convert_images_aligned():
    print("receiving convert request....")
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
            image_byte=tools.tensor_to_byte(result_image)
            checkpoint3 = time.time()

            print(f"finished converting to byte, took {checkpoint3-checkpoint2}, total time: {checkpoint3-checkpoint1}")

            # save_image(result_image,f'/workspace/HairFastGAN/output/{date_time}.png')
            return send_file(BytesIO(image_byte), mimetype='image/jpeg')
    except Exception as e:
        print("found error when swapping")
        print(e)
        return jsonify({'error': str(e)}), 500
# run command: gunicorn app:app -b :5000 -w 1

