from mongoengine import *
from datetime import datetime


class Checkpoint(EmbeddedDocument):
    """
    A MongoEngine EmbeddedDocument containing:
    distance: MongoEngine float field, required, (checkpoint distance in kilometers),
                location: MongoEngine string field, optional, (checkpoint location name),
                open_time: MongoEngine datetime field, required, (checkpoint opening time),
                close_time: MongoEngine datetime field, required, (checkpoint closing time).
    """
    distance = FloatField(required=True)
    location = StringField(required=False)
    open_time = DateTimeField(required=True)
    close_time = DateTimeField(required=True)


class Brevet(Document):
    """
    A MongoEngine document containing:
    length: MongoEngine float field, required
    start_time: MongoEngine datetime field, required
    checkpoints: MongoEngine list field of Checkpoints, required
    """
    length = FloatField(required=True)
    start_time = DateTimeField(required=True)
    checkpoints = ListField(required=True)


def build_checkpoint_list(request_body_checkpoints):
    checkpoints = list()
    for data in request_body_checkpoints:
        checkpoint_document = Checkpoint(
            distance=data['distance'], 
            location=data['location'],
            open_time=datetime.fromisoformat(data['open_time']),
            close_time=datetime.fromisoformat(data['close_time'])
        )
        checkpoints.append(checkpoint_document)
    return checkpoints
