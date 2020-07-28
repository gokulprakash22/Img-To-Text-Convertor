from flask import Flask, render_template, url_for, request
from werkzeug.utils import secure_filename
import os
import requests
import json

UPLOAD_FOLDER = './static/uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def ocr_space_file(filename):
    payload = {'isOverlayRequired': False,
               'apikey': os.environ.get('OCR_SPACE_API_KEY'),
               'language': 'eng',
               'isTable': True
               }
    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: f},
                          data=payload,
                          )
    return r.content.decode()

@app.route('/',methods = ['GET', 'POST'])
def index():
    img_path=None
    text=None
    error_msg=None
    if request.method == 'POST':
        file = request.files['image']
        if file.filename == '':
            error_msg="Please Upload Any Image"
        elif file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            img_path="./static/uploads/{}".format(filename)
            test_file = ocr_space_file(filename=img_path)
            result = json.loads(test_file)
            parsed_results = result.get("ParsedResults")[0].get("ParsedText")
            lines = parsed_results.split('\r\n')
            text=[]
            for i in range(len(lines)):
                words=lines[i].split('\t')
                text.append(words)
            error_msg=None
        else:
            error_msg="Please Upload PNG/JPG/JPEG Image"
    return render_template('index.html',img_path=img_path,text=text,error_msg=error_msg)

if __name__=="__main__":
    app.run(debug=True)