"""
Resource: Brevets
"""
from flask import Response, request
from flask_restful import Resource
import logging
from datetime import datetime

from database.models import Brevet, Checkpoint, build_checkpoint_list

logging.basicConfig(level=logging.DEBUG)

class BrevetsApi(Resource):
    def get(self):
        brevets = Brevet.objects().order_by('-distance').to_json()
        return Response(brevets, mimetype="application/json", status=200)

    def post(self):
        body = request.get_json()
        checkpoints = build_checkpoint_list(body['checkpoints'])
        brevet = Brevet()
        brevet.length = body['length']
        brevet.start_time = datetime.fromisoformat(body['start_time'])
        brevet.checkpoints = checkpoints
        brevet.save()
        id = brevet.id
        return {'id' : str(id)}, 200