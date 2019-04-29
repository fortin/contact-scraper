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
    # with open(filename, 'r') as f:
    #     headers = f.read()
    headers = str(raw_headers)
    # strip double quotes, convert brackets [()] to braces and make string dict-like for json.loads
    headers = re.sub(r"{(.+?}).+", "\\1", headers)
    # get rid of everything after the headers
    for char in headers:
        headers = headers.translate({ord(i):None for i in '[]'})
    return(headers)

# TODO is there a less bruteforce way of doing the above?

raw_headers = header_parser('test_email.eml')
print(raw_headers)
print(type(raw_headers))
# headers = str(extract_headers(headers))

# names = []
# for h in headers.items():
#     names.append(h)

# print(names) # TODO process headers from string rather than external file.

headers = str(extract_headers(raw_headers))
# print(headers)
# print(type(headers))
# headers = json.loads(headers)
# wanted_keys = ['From'] # The key(s) you want
# from_field = dict((k, headers[k]) for k in wanted_keys if k in headers)

# print(from_field)


# pattern = re.compile(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)")
# numbers = set()

# extractdas all email addresses from message
# for i, line in enumerate(open('test_email.eml')):
#     for match in re.finditer(pattern, line):
#         emails.update(match.groups())

# extract all US phone numbers from message
# for match in phonenumbers.PhoneNumberMatcher(my_email, "US"):
#     try:
#         numbers.add(phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.E164))
#     except(TypeError):
#         pass
#
# print(emails, numbers)
