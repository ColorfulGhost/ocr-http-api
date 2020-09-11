import hashlib
import os
from wsgiref.simple_server import make_server

import easyocr
from flask import Flask
from flask_restful import Api, Resource, reqparse
from werkzeug.datastructures import FileStorage


class OCRRestfulApi(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("image", type=FileStorage, help="imgFile is wrong.", location='files')

    def post(self):
        args = self.parser.parse_args()
        img_file = args.get("image")
        img_file.save(img_file.filename)
        reader = easyocr.Reader(['ch_sim', 'en'], gpu=False)  # need to run only once to load model into memory

        md5_l = hashlib.md5()
        with open(img_file.filename, mode="rb") as f:
            by = f.read()
        md5_l.update(by)

        result = {}
        file_md5 = md5_l.hexdigest()
        resultArr = reader.readtext(img_file.filename, detail=0)
        result[file_md5] = resultArr

        os.remove(img_file.filename)
        return result, 201


if __name__ == '__main__':
    app = Flask(__name__)
    api = Api(app)

    api.add_resource(OCRRestfulApi, "/doOCR")
    server = make_server(('0.0.0.0', 88), app)
    server.serve_forever()

    # app.run(
    #     host='0.0.0.0',
    #     port=88,
    #     debug=True)
