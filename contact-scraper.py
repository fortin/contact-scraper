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
import json
import phonenumbers
# from io import IOBase

def header_parser(filename):
    # parse email headers
    with open(filename, 'r') as msg:
        my_email = msg.read()
        parser = email.parser.HeaderParser()
        raw_headers = parser.parsestr(my_email)
    return(raw_headers)

def header_cleaner(raw_headers):
    str_headers = []
    for h in raw_headers.items():
        str_headers.append(h)
    headers = str(str_headers)
    # strip double quotes, convert brackets [()] to braces and make string dict-like for json.loads
    headers = headers.replace('"', '').replace("[(", "{", 1).replace(")]", "}").replace("',", "':").replace("'", '"').replace("), (", ",")
    # get rid of everything after the headers
    headers = re.sub(r"{(.+?}).+", "\\1", headers)
    # for char in headers:
    #     headers = headers.translate({ord(i):None for i in '[]'})
    return(headers)

# TODO is there a less bruteforce way of doing the cleanup above?

def number_catcher(filename):
    # extract all US phone numbers from message
    with open(filename, 'r') as msg:
        my_email = msg.read()
        numbers = set()
        for match in phonenumbers.PhoneNumberMatcher(my_email, "US"):
            numbers.add(phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.E164))
    return(numbers)

def email_catcher(filename):
    # extract all email addresses from message
    pattern = re.compile(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)")
    emails = set()
    with open(filename) as f:
        for i, line in enumerate(f):
            for match in re.finditer(pattern, line):
                emails.update(match.groups())
# TODO check if filename is a file or string type and react accordingly.
    return(emails)

my_file = 'test_email.eml'

raw_headers = header_parser(my_file)
headers = header_cleaner(raw_headers)
headers = json.loads(headers)
wanted_keys = ['From'] # The key(s) you want

from_hdr = dict((k, headers[k]) for k in wanted_keys if k in headers)
from_val = str([*from_hdr.values()])

contact = from_val.split()

contact = {
            'lastname' : contact[1].replace("[", "").replace("]", ""),
            'firstname': contact[0].replace("[", "").replace("]", "").replace("'", ""),
            'email'    : contact[-1].replace("[", "").replace("]", ""),
            'company'  : None
            }

print(contact)

numbers = number_catcher(my_file)
print(numbers)

emails = email_catcher(my_file)
print(emails)
