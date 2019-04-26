import re
import string
import csv
import json

def headers2dict(filename):
    with open(filename, 'r') as f:
        headers = f.read()
    headers = headers.replace('"', '') # strip double quotes
    headers = headers.replace("[(", "{", 1) # [( -> {
    headers = headers.replace(")]", "}") # )] -> }
    headers = headers.replace("',", "':") # ', -> ':
    headers = re.sub(r"{(.+?}).+", "\\1", headers) # get rid of everything after the headers
    headers = headers.replace("'", '"') # single to double quotes for dict
    headers = headers.replace("), (", ",") # ), ( -> ,
    for char in headers:
        headers = headers.translate({ord(i):None for i in '[]'})
    return(headers)

# TODO is there a less bruteforce way of doing headers2dict?

headers = str(headers2dict('test-headers.txt'))
headers = json.loads(headers)
wanted = ['From', 'To'] # The keys you want
from_value = dict((k, headers[k]) for k in wanted if k in headers)
print(from_value)
