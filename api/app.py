"""
Brevets RESTful API
"""
import logging
import os
from flask import Flask
from flask_restful import Api
from mongoengine import connect
from resources import BrevetApi, BrevetsApi

app = Flask(__name__)
api = Api(app)
connect(host=f"mongodb://{os.environ['MONGODB_HOSTNAME']}/brevets")

api.add_resource(BrevetApi, "/api/brevet/<_id>")
api.add_resource(BrevetsApi, "/api/brevets")

app.debug = os.environ["DEBUG"]
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    app.logger.debug(f"Opening for global access on port {os.environ['PORT']}")
    app.run(port=os.environ["PORT"], host="0.0.0.0")