import json
from models.USState import State

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, State):
            print("ENCODING: ")
            print(obj)
            return obj.value
        if hasattr(obj, 'to_dict'):
            return obj.to_dict()
        return super().default(obj)