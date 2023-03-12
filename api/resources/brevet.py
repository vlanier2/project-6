"""
Resource: Brevet
"""
from flask import Response, request
from flask_restful import Resource
import logging
from datetime import datetime

from database.models import Brevet, Checkpoint, build_checkpoint_list

logging.basicConfig(level=logging.DEBUG)

class BrevetApi(Resource):
    def get(self, _id):
        brevet = Brevet.objects.get(id=_id).to_json()
        return Response(brevet, mimetype="application/json", status=200)
    
    def put(self, _id):

        body = request.get_json()
        brevet = Brevet.objects.get(id=_id)

        update_query = {}

        if "length" in body:
            update_query["length"] = body["length"]

        if "checkpoints" in body:
            update_query["checkpoints"] = build_checkpoint_list(body["checkpoints"])

        if "start_time" in body:
            update_query["start_time"] = datetime.fromisoformat(body["start_time"])

        brevet.update(**update_query)

        return {'id' : str(_id), 'status' : 'updated'}, 200
    
    def delete(self, _id):
        Brevet.objects.get(id=_id).delete()
        return {'id' : str(_id), 'status' : 'deleted'}, 200