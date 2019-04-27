import re
import string
import csv
import json

def extract_headers(filename):
    with open(filename, 'r') as f:
        headers = f.read()
    headers = headers.replace('"', '').replace("[(", "{", 1).replace(")]", "}").replace("',", "':").replace("'", '"').replace("), (", ",")
    # strip double quotes, convert brackets [()] to braces and make dict-like string
    headers = re.sub(r"{(.+?}).+", "\\1", headers) # get rid of everything after the headers
    return(headers)

# TODO is there a less bruteforce way of doing headers2dict?

headers = str(extract_headers('test-headers.txt'))
headers = json.loads(headers)
wanted = ['From'] # The keys you want
from_value = dict((k, headers[k]) for k in ['From'] if k in headers)
print(from_value)
