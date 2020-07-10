from flask import Flask, render_template, url_for, request, redirect
import os
from werkzeug.utils import secure_filename
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract


UPLOAD_FOLDER = './static/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/',methods = ['GET', 'POST'])
def index():
    img_path=None
    text=''
    if request.method == 'POST':
        file = request.files['image']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            img_path="./static/uploads/{}".format(filename)
            pytesseract.pytesseract.tesseract_cmd = r'./tesseract/tesseract'
            text=pytesseract.image_to_string(Image.open(img_path))
    return render_template('index.html',img_path=img_path,text=text)

if __name__=="__main__":
    app.run(debug=True)