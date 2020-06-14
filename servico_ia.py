from flask import Flask, request
from imgurpython import ImgurClient
from tensorflow import keras
from keras.models import load_model
import numpy as np
import pandas as pd
import rasterio
import requests
import matplotlib.pyplot as plt
app = Flask(__name__)

@app.route('/ia')
def ia():
    body = request.get_json()
   # lat = body['lat']
   # lon = body['lon']
    #geo = body['geo']
    bandas = dict.fromkeys(['B02', 'B03', 'B04', 'B08'])
    df = pd.DataFrame()
    for b in bandas.keys():
        bandas[b] = requests.get('http://services.sentinel-hub.com/ogc/wms/8cbb4249-c380-4033-9616-5ae31e75b8b9?REQUEST=GetMap&LAYERS={}&MAXCC=20&WIDTH=300&HEIGHT=300&FORMAT=image/tiff&TIME=2020-01-01&GEOMETRY=POLYGON((-23.49827102335408%20-48.17391096004957,%20-23.522711137062757%20-48.1737192145292,%20-23.522183700485243%20-48.12175617862559,%20-23.495809177809207%20-48.120222214466594,%20-23.49827102335408%20-48.17391096004957))&CRS=EPSG:4326&BGCOLOR=000000'.format(b))
        
        if bandas[b].status_code == 200:
            f = open(b + ".tiff", "wb")
            f.write(bandas[b].content)
            f.close()
    

    #print(rasterio.open("B02.tiff").profile)
    
    in_b02 = rasterio.open("B02.tiff").read(1).flatten() / 20001
    in_b03 = rasterio.open("B03.tiff").read(1).flatten() / 19969
    in_b04 = rasterio.open("B04.tiff").read(1).flatten() / 22426
    in_b08 = rasterio.open("B08.tiff").read(1).flatten() / 33128
    in_ndvi = np.subtract(in_b08, in_b04)/ np.add(in_b08, in_b04)
    in_ndvi = np.nan_to_num(in_ndvi)

    x = [] 

    for i in range(0,300):
        x.append([in_b02[i], in_b03[i], in_b04[i], in_b08[i], in_ndvi[i]])

    x = np.array(x)
    img_id = predict(x)

    return img_id, 200 


def upload(file):
    client_id = 'afae1e846ae1a56'
    client_secret = '2776c2df4ec2a2ce91b75857113d277921e61854'

    client = ImgurClient(client_id, client_secret)
    image = client.upload_from_path(file)
    return image['link']

def predict(x):
    model = load_model('modelo.h5')
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
    app.run(port=8922,  threaded=False, debug=True)