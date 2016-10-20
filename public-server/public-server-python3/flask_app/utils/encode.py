from json import JSONEncoder
from flask.json import JSONEncoder as Flask_JSONEncoder
from datetime import datetime

class MyJSONEncoder(JSONEncoder):

    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                obj = obj.isoformat()
                return obj
        except TypeError:
            print("TypeError for isinstance")
            pass
        return JSONEncoder.default(self, obj)

class MyFlaskJSONEncoder(Flask_JSONEncoder):

    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                obj = obj.isoformat()
                return obj
        except TypeError:
            print("TypeError for isinstance")
            pass
        return Flask_JSONEncoder.default(self, obj)