import io

import flask
from PIL import Image
from flask import request
import pytesseract

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# in order to use the tesseract, you will need to download it from https://github.com/UB-Mannheim/tesseract/wiki
# and set tesseract.exe to PATH
# after that, pip install pytesseract and pip install tesseract

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction " \
           "novels.</p> "


@app.route('/drugByImage', methods=['POST'])
def drug_by_image():
    # get file buffer
    file = request.get_json()['file']['data']
    # convert it into image
    image_stream = io.BytesIO(bytes(file))
    image_file = Image.open(image_stream)
    # todo delete later, this is just so we can see the picture
    image_file.save("a_test.png")
    print(pytesseract.image_to_string(image_file))
    return {}


app.run()