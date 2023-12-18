import json, os
import io
from flask import Flask, render_template, request
from PIL import Image
import numpy as np
#import cv2
import torch

app = Flask(__name__)

model = torch.hub.load('ultralytics/yolov5', 'custom', path='./best.pt', force_reload=True, skip_validation=True)

device = "cuda" if torch.cuda.is_available() else "cpu"
model = torch.load("model.pt", map_location=device)


app.config['UPLOAD_FOLDER'] = 'static/upload'
app.config['RESULT_FOLDER'] = 'static/result'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/draw')
def draw():
    return render_template('draw.html')

@app.route('/result', methods=['POST'])
def result():
    if request.method != 'POST':
        return
    
    if request.files.get('image'):
        # Method 1
        # with request.files["image"] as f:
        #     im = Image.open(io.BytesIO(f.read()))

        # Method 2
        im_file = request.files['image']
        im_bytes = im_file.read()
        im = Image.open(io.BytesIO(im_bytes))

        results = model(im, size=640) 
        print(results.pandas().xyxy[0].to_json(orient='records')) 
        
        return render_template('result.html')
    
    return

if __name__=='__main__':
    app.run(debug=True)