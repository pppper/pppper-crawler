import json

def jsonprint(data):
  print(json.dumps(data, ensure_ascii=False, indent=4))