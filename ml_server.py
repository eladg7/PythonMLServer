import io
import traceback
import flask
from PIL import Image
from flask import request, jsonify
import pytesseract

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# in order to use the tesseract, you will need to download it from https://github.com/UB-Mannheim/tesseract/wiki
# and set tesseract.exe to PATH
# after that, pip install pytesseract and pip install tesseract

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


@app.route('/', methods=['GET'])
def home():
    # TODO remove this
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction " \
           "novels.</p> "


@app.route('/drugByBox', methods=['POST'])
def drug_by_box():
    # get file buffer
    file = get_image_from_request(request.get_json())
    if file is not None:
        text_in_image = get_string_from_file(file)
    else:
        text_in_image = ""
    return jsonify(text_in_image)


@app.route('/drugByImage', methods=['POST'])
def drug_by_image():
    # get file buffer
    file = get_image_from_request(request.get_json())
    if file is not None:
        # predict data
        # pill_properties = ...
        pass
    else:
        pill_properties = {}
    return jsonify(pill_properties)


def get_string_from_file(file):
    # convert it into image
    image_stream = io.BytesIO(bytes(file))
    image_file = Image.open(image_stream)
    # todo delete later, this is just so we can see the picture
    # image_file.save("a_test.png")
    return pytesseract.image_to_string(image_file)


def get_image_from_request(req_json):
    file = None
    try:
        file = req_json['file']['data']
    except TypeError as err:
        # print stack trace
        traceback.print_tb(err.__traceback__)

    return file


app.run()
