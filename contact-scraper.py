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

def header_parser(filename):
    # parse email headers
    with open(filename, 'r') as msg:
        my_email = msg.read()
        parser = email.parser.HeaderParser()
        raw_headers = parser.parsestr(my_email)
    return(raw_headers)

def extract_headers(raw_headers):
    str_headers = []
    for h in raw_headers.items():
        str_headers.append(h)
    headers = str(str_headers)
    headers = headers.replace('"', '').replace("[(", "{", 1).replace(")]", "}").replace("',", "':").replace("'", '"').replace("), (", ",")
    # strip double quotes, convert brackets [()] to braces and make string dict-like for json.loads
    headers = re.sub(r"{(.+?}).+", "\\1", headers)
    # get rid of everything after the headers
    for char in headers:
        headers = headers.translate({ord(i):None for i in '[]'})
    return(headers)

# TODO is there a less bruteforce way of doing the cleanup above?

def number_catcher(filename):
    # extract all US phone numbers from message
    with open(filename, 'r') as msg:
        my_email = msg.read()
        numbers = set()
        for match in phonenumbers.PhoneNumberMatcher(my_email, "US"):
            try:
                numbers.add(phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.E164))
            except(TypeError):
                pass
    return(numbers)

my_file = 'test_email.eml'

raw_headers = header_parser(my_file)
headers = str(extract_headers(raw_headers))
headers = json.loads(headers)
wanted_keys = ['From'] # The key(s) you want
from_field = dict((k, headers[k]) for k in wanted_keys if k in headers)

print(from_field)
numbers = number_catcher(my_file)
print(numbers)

pattern = re.compile(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)")

emails = set()

# extract all email addresses from message
for i, line in enumerate(open('test_email.eml')):
    for match in re.finditer(pattern, line):
        emails.update(match.groups())


print(emails, numbers)
