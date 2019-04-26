import re
import string
import csv

def headers2dict(filename):
    with open(filename, 'r') as f:
        headers = f.read()
    headers = headers.replace("[(", "{", 1)
    headers = headers.replace(")]", "}")
    headers = headers.replace("',", "':")
    headers = re.sub(r"{(.+?}).+", "\\1", headers)
    headers = headers.replace("'", '"')
    headers = headers.replace("), (", ",")
    for char in headers:
        headers = headers.translate({ord(i):None for i in '[]'})
    return(headers)

headers = str(headers2dict('test-headers.txt'))
print(headers)
# headers = json.loads(headers)
print(type(headers))
# wanted = ['From'] # The keys you want
# dict((k, headers[k]) for k in wanted if k in headers)
# {from: headers[from] for from in headers.keys() & {'From'}}

# print(dict)
# print(headers)
# print(type(wanted))
# print(dictionary)
#
# names = ()
#
# for key, value in dictionary:
#     m = re.search(r'From', key)
#     if m:
#         names.append(value)
#
# print(names)
