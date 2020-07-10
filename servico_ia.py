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
        print("baixando ", item['assets']['B8']['href'])
        r = requests.get(item['assets']['B8']['href'])
        if r.status_code == 200:
            f = open(item['_id'] + ".tif", "wb")
            print("baixando")
            f.write(r.content)
            f.close()
            reprojectA(item['_id'])
            cropImg(body[0], item['_id'])
    
    
    imgs_ids=[]
    for item in body[1:]:
        raster = rasterio.open("cropped"+ item["_id"] + ".tif").read(1)
        w = raster.width
        h = raster.height
        plt.imshow(test)
        plt.show()
        predicted = predict(raster)
        sh_preds = np.reshape(predicted, (h,w))
        spec = plt.imshow(sh_preds)
        plt.savefig(item['_id'] + '.png', bbox_inches='tight', pad_inches=0)
        img_id = upload(item['_id'] + '.png')
        imgs_ids.append(img_id)
    print(imgs_ids)
    res = {}
    res['links'] = imgs_ids
    return res, 200 


def upload(file):
    client_id = 'afae1e846ae1a56'
    client_secret = '2776c2df4ec2a2ce91b75857113d277921e61854'

    client = ImgurClient(client_id, client_secret)
    image = client.upload_from_path(file)
    return image['link']

def predict(x):
    model = load_model('modelo.h5')
    
    preds = model.predict(x)

    sh_preds = np.reshape(preds, (h,w))

    plt.imshow(img_out)
    plt.show()

    spec = plt.imshow(img_out)
    plt.savefig('image.png', bbox_inches='tight', pad_inches=0)
    img_id = upload('image.png')

    return img_id

if __name__ == "__main__":
    app.run(port=8922, debug=True)