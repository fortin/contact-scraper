#!/usr/bin/env python3
#
#  Contact Scraper for Gmail
#
#  Created by Antonio Fortin on 2019-04-01.
#  Copyright (c) 2019 Antonio Fortin. All rights reserved.
#

import re
import email
import email.parser
import string
import csv
import json
import phonenumbers

def extract_headers(filename):
    with open(filename, 'r') as f:
        headers = f.read()
    headers = headers.replace('"', '').replace("[(", "{", 1).replace(")]", "}").replace("',", "':").replace("'", '"').replace("), (", ",")
    # strip double quotes, convert brackets [()] to braces and make string dict-like for json.loads
    headers = re.sub(r"{(.+?}).+", "\\1", headers)
    # get rid of everything after the headers
    return(headers)

# TODO is there a less bruteforce way of doing extract_headers?

headers = str(extract_headers('test-headers.txt'))
headers = json.loads(headers)
wanted_keys = ['From', 'Organization'] # The keys you want
from_value = dict((k, headers[k]) for k in wanted_keys if k in headers)
print(from_value)

pattern = re.compile(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)")
msg = open('test_email.eml')
my_email = msg.read()

emails = set()
numbers = set()

# parse email headers
parser = email.parser.HeaderParser()
headers = parser.parsestr(str(my_email))
names = []

for h in headers.items():
    names.append(h)

print(names) # TODO process headers from string rather than external file.

# extract all email addresses from message
for i, line in enumerate(open('test_email.eml')):
    for match in re.finditer(pattern, line):
        emails.update(match.groups())

# extract all US phone numbers from message
for match in phonenumbers.PhoneNumberMatcher(my_email, "US"):
    try:
        numbers.add(phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.E164))
    except(TypeError):
        pass

print(emails, numbers)
