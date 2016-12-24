import sys
from os import path
from flask import Flask
from flask import redirect
from flask import jsonify
from flask import url_for
from flask import send_from_directory, request, Response
from flask import render_template
from flask_restful import Resource, Api, fields, marshal_with, reqparse
import random
sys.path.append('../../lib')
from board import Board

app = Flask(__name__, static_folder="../static", template_folder="../templates")
api = Api(app)

board = Board()






class NextBoard(Resource):

    def _pos_to_coordinate(self, pos):
        x = int(pos % 19)
        y = int(pos / 19)
        print ("coordinate:", (x, y))
        return (x, y)


    def post(self):
        print("recv:", request.json)
        pos = request.json['position']
        coordinate = self._pos_to_coordinate(pos)

        board.move(coordinate)
        return {
            "pos": random.randint(0, 360),
        }


    def get(self):
        pass


api.add_resource(NextBoard, '/get_next_move')



@app.route('/')
def index():
    return render_template("index.html")



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=9090, threaded=True)
