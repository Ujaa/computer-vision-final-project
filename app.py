import json, os
import io
from flask import Flask, render_template, request,flash
from PIL import Image
import numpy as np
import cv2
import torch
import scan as s
from HTP import HTP
app = Flask(__name__)

device = "cuda" if torch.cuda.is_available() else "cpu"
model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt', force_reload=True, skip_validation=True)

app.config['UPLOAD_FOLDER'] = 'static/upload'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/draw')
def draw():
    return render_template('draw.html')

@app.route('/result', methods=['POST'])
def result():
    contents = dict()
    
    if request.method != 'POST':
        return
    
    if request.files.get('image'):
        im_origin_path = os.path.join(app.config['UPLOAD_FOLDER'], 'image_origin.png')
        im_path = os.path.join(app.config['UPLOAD_FOLDER'], 'image.png')
        im_detect_path = os.path.join(app.config['UPLOAD_FOLDER'], 'image_detect.png')
        
        im_file = request.files['image']
        im_file.save(im_origin_path)
        
        cv_im = cv2.imread(im_origin_path,cv2.IMREAD_COLOR)
        cv_im = s.transform_img(cv_im)
        cv2.imwrite(im_path, cv_im)
        
        im = Image.open(im_path)
        predict = model(im, size=640)
        results = json.loads(predict.pandas().xyxy[0].to_json(orient='records'))
        
        left_x,left_y,right_x,right_y=100000,100000,0,0
        
        im_np = np.array(im)
        result_np = np.array(im)
        
        print(results)
        
        for result in results:
            if(result['confidence'] < 0.5):
                break
            
            x_min, y_min, x_max, y_max, name = result['xmin'], result['ymin'], result['xmax'], result['ymax'], result['name']
            x1, y1, x2, y2 = int(x_min), int(y_min), int(x_max), int(y_max)
            cv2.rectangle(im_np, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.putText(im_np, name, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)
            if(left_x>x1):
                left_x = x1
            if(left_y>y1):
                left_y = y1
            if(right_x<x2):
                right_x =x2
            if(right_y<y2):
                right_y = y2
            print(name)
       
        margin = 100

        # 안전 검사를 추가하여 이미지 밖으로 벗어나지 않도록 함
        left_y = max(0, left_y - margin)
        left_x = max(0, left_x - margin)
        right_y = min(im_np.shape[0], right_y + margin)
        right_x = min(im_np.shape[1], right_x + margin)

        cropped_img = result_np[left_y:right_y, left_x:right_x]
        
        Image.fromarray(im_np).save(im_detect_path)
        try:
            Image.fromarray(cropped_img).save(im_path)
        except ValueError as e:
            print(f"Error saving image: {e}")
            flash("이미지를 다시 입력해주세요")
        #Image.fromarray(cropped_img).save(im_path)
        
        htp = HTP(results)
        contents = htp.get_result()
        
    return render_template('result.html', contents = contents)

if __name__=='__main__':
    app.run(debug=True, port=5000)