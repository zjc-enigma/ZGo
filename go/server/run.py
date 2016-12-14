import sys
from os import path
from flask import Flask
from flask import redirect
from flask import jsonify
from flask import url_for
from flask import send_from_directory, request, Response
from flask import render_template
from flask_restful import Resource, Api, fields, marshal_with, reqparse

app = Flask(__name__, static_folder="../static", template_folder="../templates")
api = Api(app)



class NextBoard(Resource):

    def post(self):
        print("recv:", request.json)
        return {
            "name": "infinite",
            "level": 9
        }


    def get(self):
        pass


api.add_resource(NextBoard, '/get_next_move')



@app.route('/')
def index():
    return render_template("index.html")



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=9090, threaded=True)
