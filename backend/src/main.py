from flask import Flask
from flask_cors import CORS
from db import DB_new


DBN = DB_new()
app = Flask(__name__)
CORS(app, resources={
    r"/get_placemark/*": {"origins": "*"},
    r"/get_info/*": {"origins": "*"},
    }) # настройка CORS POLICY


@app.route("/get_placemark", methods=['POST'])
def hello_world():
    data = DBN.get_all_placemarks()
    return {"placemarks" : data[0], "colors" : data[1], "baloon": data[2]}


@app.route("/get_info", methods=['POST'])
def info():
    return {"data": DBN.find_place()}


if __name__ == "__main__":
    app.run()