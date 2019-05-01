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
        # stop when binary data starts
        if h == "Content-Type: image" or h == "Content-Type: application":
            break
        else:
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
        if numbers == set():
            numbers = None
        numbers = str(numbers).replace("{'", "").replace("'}", "")
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

def dict_pop(contact, numbers):
    if contact[0].isupper():
        contact = {
                    'lastname' : contact[0].replace("[", "").replace("]", "").replace("'", ""),
                    'firstname': contact[1].replace("[", "").replace("]", "").replace("'", ""),
                    'email'    : contact[-1].replace("[", "").replace("]", "").replace("'", ""),
                    'company'  : None,
                    'address'  : None,
                    'phone'    : numbers
                    }
    elif len(contact) < 4:
        try:
            contact = {
                        'lastname' : contact[1].replace("[", "").replace("]", "").replace("'", ""),
                        'firstname': contact[0].replace("[", "").replace("]", "").replace("'", ""),
                        'email'    : contact[-1].replace("[", "").replace("]", "").replace("'", ""),
                        'company'  : None,
                        'address'  : None,
                        'phone'    : numbers
                        }
        except:
            pass
    else:
        company = str(contact[0:-1]).replace("[", "").replace("]", "").replace("'", "").replace('"', "").replace(",", "")
        contact = {
                    'lastname' : None,
                    'firstname': None,
                    'email'    : contact[-1].replace("[", "").replace("]", "").replace("'", ""),
                    'company'  : company,
                    'address'  : None,
                    'phone'    : numbers
                    }
    return(contact)

my_file = 'test_email.eml'

raw_headers = header_parser(my_file)
headers = header_cleaner(raw_headers)
headers = json.loads(headers)
from_key = ['From'] # The key(s) you want

from_hdr = dict((k, headers[k]) for k in from_key if k in headers)
from_val = str([*from_hdr.values()])

contact = from_val.split()
numbers = number_catcher(my_file)

# emails = email_catcher(my_file)
# print(emails)
contact = dict_pop(contact, numbers)

print(contact)
