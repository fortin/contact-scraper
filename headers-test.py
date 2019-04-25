import re
import string
import csv

with open('test-headers.txt', 'r') as f:
    headers = f.read()

for char in headers:
    headers = headers.translate({ord(i):None for i in '[]'})

dictionary = pickle.load(headers)

print(type(headers))
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
