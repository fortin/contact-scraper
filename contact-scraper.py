#!/usr/bin/env python3
#
#  Contact Scraper for email
#
#  Created by Antonio Fortin on 2019-04-01.
#  Copyright (c) 2019 Antonio Fortin. All rights reserved.
#

import re
from email.parser import HeaderParser
import phonenumbers

def header_parser(filename):
    # parse email headers
    with open(filename, 'r') as msg:
        my_email = msg.read()
        parser = HeaderParser()
        h = parser.parsestr(my_email)
        headers = dict(h.items())
    return(headers)

def num_catcher(filename):
    # extract all US phone numbers from message
    with open(filename, 'r') as msg:
        my_email = msg.read()
        numbers = set()
        for match in phonenumbers.PhoneNumberMatcher(my_email, "US"):
            numbers.add(phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.E164))
            if numbers != set(): # stop after first match
                break
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

headers = header_parser(my_file)

from_key = ['From'] # The key(s) you want

from_hdr = dict((k, headers[k]) for k in from_key if k in headers)
from_val = str([*from_hdr.values()])

contact = from_val.split()

numbers = num_catcher(my_file)
contact = dict_pop(contact, numbers)

print(contact)

# emails = email_catcher(my_file)
# print(emails)
