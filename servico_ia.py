from flask import Flask, request, jsonify
from imgurpython import ImgurClient
from crop import cropImg, reprojectA
import json
#from tensorflow import keras
#from tensorflow.keras.models import load_model
import numpy as np
#import pandas as pd
import rasterio
from flask_cors import CORS
import requests
import matplotlib.pyplot as plt
app = Flask(__name__)
CORS(app)

@app.route('/ia', methods=['POST'])
def ia():
    print('chegou aqui')
    body = request.get_json()
    print(body[0])
    for item in body[1:]:
        print(item['assets']['B8']['href'])
        r = requests.get(item['assets']['B8']['href'])
        if r.status_code == 200:
            f = open(item['_id'] + ".tif", "wb")
            f.write(r.content)
            f.close()
            reprojectA(item['_id'])
            cropImg(body[0])
    
    
   # lat = body['lat']
   # lon = body['lon']
    #geo = body['geo']
    

    #print(rasterio.open("B02.tiff").profile)
    imgs_ids=[]
    for item in body[1:]:
        test = rasterio.open("cropped" + ".tif").read(1)
        plt.imshow(test)
        plt.show()
        spec = plt.imshow(test)
        plt.savefig(item['_id'] + '.png', bbox_inches='tight', pad_inches=0)
        img_id = upload(item['_id'] + '.png')
        imgs_ids.append(img_id)
    print(imgs_ids)
    return imgs_ids, 200 


def upload(file):
    client_id = 'afae1e846ae1a56'
    client_secret = '2776c2df4ec2a2ce91b75857113d277921e61854'

    client = ImgurClient(client_id, client_secret)
    image = client.upload_from_path(file)
    return image['link']

def predict(x):
    model = load_model('modelo.h5')
    print(model.summary())
    preds = model.predict(x)

    img_out = []
    for i in range(0,300):
        img_out.append([])
        for j in range(0,300):
            img_out[i].append(preds[0][1]*300)
    plt.imshow(img_out)
    plt.show()

    spec = plt.imshow(img_out)
    plt.savefig('image.png', bbox_inches='tight', pad_inches=0)
    img_id = upload('image.png')

    return img_id

def eps(n):
  return n > 0.018
  # return n > 0.045

if __name__ == "__main__":
    app.run(port=8922, debug=True)