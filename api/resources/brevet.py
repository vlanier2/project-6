"""
Resource: Brevet
"""
from flask import Response, request
from flask_restful import Resource
from datetime import datetime
import logging

# You need to implement this in database/models/
from database.models import Brevet, Checkpoint

logging.basicConfig(level=logging.DEBUG)

class BrevetApi(Resource):
    def get(self, _id):
        brevet = Brevet.objects.get(id=_id).to_json()
        return Response(brevet, mimetype="application/json", status=200)
    
    def put(self, _id):
        body = request.get_json()

        logging.debug(body)

        checkpoints = list()
        for checkpoint_key in body['checkpoints']:



            data = body['checkpoints'][checkpoint_key]
            checkpoints.append(
                Checkpoint(data['distance'], data['location'],
                           datetime.fromisoformat(data['open_time']),
                           datetime.fromisoformat(data['close_time']))
            )
        brevet = Brevet.objects.get(id=_id) #.update(**body)
        brevet.update(length = body["length"])
        brevet.update(checkpoints = checkpoints)
        brevet.update(start_time = datetime.fromisoformat(body["start_time"]))

        return {'id' : str(_id), 'status' : 'updated'}, 200
    
    def delete(self, _id):
        Brevet.objects.get(id=_id).delete()
        return {'id' : str(_id), 'status' : 'deleted'}, 200

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
