#!/usr/bin/env python3
#
#  Contact Scraper for Gmail
#
#  Created by Antonio Fortin on 2019-04-01.
#  Copyright (c) 2019 Antonio Fortin. All rights reserved.
#

import phonenumbers
import re
import email
import email.parser
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

pattern = re.compile(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)")
msg = open('test_email.eml')
my_email = msg.read()

emails = set()
numbers = set()

parser = email.parser.HeaderParser()
headers = parser.parsestr(str(my_email))
names = []

for h in headers.items():
    # m = re.search(r"From", h)
    # if m:
    names.append(h)

print(names)

for i, line in enumerate(open('test_email.eml')):
    for match in re.finditer(pattern, line):
        emails.update(match.groups())

for match in phonenumbers.PhoneNumberMatcher(my_email, "US"):
    try:
        numbers.add(phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.E164))
    except(TypeError):
        pass

print(emails, numbers)
