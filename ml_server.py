import io
import traceback

import flask
import pytesseract
from PIL import Image
from flask import request, jsonify

import consts
from MLHandler import MLHandler

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# in order to use the tesseract, you will need to download it from https://github.com/UB-Mannheim/tesseract/wiki
# and set tesseract.exe to PATH
# after that, pip install pytesseract and pip install tesseract
pytesseract.pytesseract.tesseract_cmd = consts.tesseract_cmd


@app.route(consts.drug_by_box_route, methods=[consts.post_request])
def drug_by_box():
    # get file buffer
    file = get_image_file_from_request(request.get_json())
    if file is not None:
        image_file = get_image_from_file(file)
        text_in_image = pytesseract.image_to_string(image_file)
    else:
        text_in_image = ""
    return jsonify(text_in_image)


@app.route(consts.drug_by_image_route, methods=[consts.post_request])
def drug_by_image():
    # get file buffer
    file = get_image_file_from_request(request.get_json())
    pill_properties = {}
    if file is not None:
        # predict properties
        image_file = get_image_from_file(file)
        pill_properties = MLHandler.get_pill_properties(image_file)
    return jsonify(pill_properties)


def get_image_from_file(file):
    image_stream = io.BytesIO(bytes(file))
    return Image.open(image_stream)


def get_image_file_from_request(req_json):
    file = None
    try:
        file = req_json[consts.file_in_json][consts.data_in_json]
    except TypeError as err:
        # print stack trace
        traceback.print_tb(err.__traceback__)

    return file


app.run()
