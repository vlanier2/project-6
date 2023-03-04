"""
Resource: Brevets
"""
from flask import Response, request
from flask_restful import Resource
import logging
from datetime import datetime

# You need to implement this in database/models/
from database.models import Brevet, Checkpoint

logging.basicConfig(level=logging.DEBUG)

class BrevetsApi(Resource):
    def get(self):
        brevets = Brevet.objects().order_by('-distance').to_json()
        return Response(brevets, mimetype="application/json", status=200)

    def post(self):

        logging.debug("POST")

        body = request.get_json()

        logging.debug(body)
        logging.debug(body['checkpoints'])

        checkpoints = list()
        for data in body['checkpoints']:
            
            checkpoints.append(
                Checkpoint(distance=data['distance'], location=data['location'],
                           open_time=datetime.fromisoformat(data['open_time']),
                           close_time=datetime.fromisoformat(data['close_time']))
            )

        logging.debug("SAVE")

        for obj in body:
            logging.debug(obj)
            logging.debug(body[obj])

        brevet = Brevet()
        brevet.length = body['length']
        brevet.start_time = datetime.fromisoformat(body['start_time'])
        brevet.checkpoints = checkpoints
        brevet.save()
        id = brevet.id
        return {'id' : str(id)}, 200

# MongoEngine queries:
# Brevet.objects() : similar to find_all. Returns a MongoEngine query
# Brevet(...).save() : creates new brevet
# Brevet.objects.get(id=...) : similar to find_one

# Two options when returning responses:
#
# return Response(json_object, mimetype="application/json", status=200)
# return python_dict, 200
#
# Why would you need both?
# Flask-RESTful's default behavior:
# Return python dictionary and status code,
# it will serialize the dictionary as a JSON.
#
# MongoEngine's objects() has a .to_json() but not a .to_dict(),
# So when you're returning a brevet / brevets, you need to convert
# it from a MongoEngine query object to a JSON and send back the JSON
# directly instead of letting Flask-RESTful attempt to convert it to a
# JSON for you.
