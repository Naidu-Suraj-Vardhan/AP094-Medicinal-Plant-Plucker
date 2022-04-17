from flask import Flask, request, session, g, redirect
from flask import url_for, abort, render_template, flash, jsonify
import os
import uuid
import cv2
import subprocess
import base64
# Create two constant. They direct to the app root folder and logo upload folder
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static', 'uploads')

# Configure Flask app and the logo upload folder
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"


@app.route('/upload', methods=['POST'])
def upload_file():
    # In controller save the file with desired name
    latestfile = request.files['image']
    filename = str(uuid.uuid4()) + '.jpg'
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'],filename)
    latestfile.save(full_filename)
    # In controller call the predict_image function
    result = predict_image(full_filename)
    # In controller return the result
    return jsonify({"output":result})



def predict_image(image_path):
    result = subprocess.run(['python3', 'detect.py', '--source', image_path, '--weights', 'best.pt'], stdout=subprocess.PIPE)
    final = result.stdout.decode('utf-8').strip()
    print(final)
    if(final == '1'):
        return 1
    else:
        return 0


@app.route('/checkFiles', methods=['GET'])
def checkFiles():
    l_ = os.listdir('runs/detect/exp/')
    
    return jsonify({
    'list' : l_
    })



@app.route('/downloadFiles', methods=['POST'])
def downloadFiles():
    l_ = request.json['image']
    
    image = cv2.imread("runs/detect/exp/"+l_)
    _,encoded = cv2.imencode('.jpeg',image)
    baseEncoded = base64.b64encode(encoded)

    return baseEncoded,200


if __name__ == '__main__':
    app.run(host='0.0.0.0',port="5000",debug=True)
    
