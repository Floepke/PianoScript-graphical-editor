# import
import json

# load test json-file
file = {}
with open('/home/philipbergwerf/Desktop/test.pianoscript', 'r') as f:
    file = json.load(f)

# save the file
with open('/home/philipbergwerf/Desktop/test.pianoscript','w') as f:
    f.write(json.dumps(file, separators=(',', ':')))