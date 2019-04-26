import re
import string
import csv

def headers2dict(filename):
    with open(filename, 'r') as f:
        headers = f.read()
    headers = headers.replace("[(", "{\n", 1)
    headers = headers.replace(")]", "\n}")
    headers = headers.replace("',", "':")
    headers = re.sub(r"{(.+?}).+", "\\1", headers)
    headers = headers.replace("), (", ", \n")
    for char in headers:
        headers = headers.translate({ord(i):None for i in '[]'})
    return(headers)

headers = headers2dict('test-headers.txt')

wanted = ['From'] # The keys you want
dict((k, headers[k]) for k in wanted if k in headers)
# {from: headers[from] for from in headers.keys() & {'From'}}

print(dict)
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
