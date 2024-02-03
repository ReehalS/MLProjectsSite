from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
# from algorithm import run_algorithm
from main import run_algorithm
from eda import analysis
from flask_restful import Api, Resource

app = Flask(__name__)

CORS(app)
api = Api(app)

@app.route("/", methods=['GET'])
def return_home():
    return jsonify({
        "message": "Hello there",
        "people" : ["General Kenobi", "Anakin Skywalker", "Padme Amidala"]
        })

if __name__ == "__main__":
    app.run(debug=True, port=8080)