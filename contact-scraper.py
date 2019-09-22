#!/usr/bin/env python3
#
#  Contact Scraper for email
#
#  Copyright (c) 2019 Antonio Fortin. All rights reserved.
#

import re
from email.parser import HeaderParser
import phonenumbers
from names_dataset import NameDataset

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
            numbers.add(phonenumbers.format_number(
                match.number, phonenumbers.PhoneNumberFormat.E164))
            if numbers != set():  # stop after first match (not ideal)
                break
        if numbers == set():
            numbers = None
        numbers = str(numbers).replace("{'", "").replace("'}", "")
    return(numbers)


def email_catcher(filename):
    # extract all email addresses from message (not necessary yet)
    pattern = re.compile(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)")
    emails = set()
    with open(filename) as f:
        for i, line in enumerate(f):
            for match in re.finditer(pattern, line):
                emails.update(match.groups())
    return(emails)


def dict_pop(contact, numbers):
    domain = re.sub(r"[a-zA-Z0-9_.+-]+@([a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)",
                    r"\1",
                    contact[-1])
    try:
        contact = {
            'lastname': contact[1],
            'firstname': contact[0],
            'email': contact[-1],
            'company': domain,
            'address': None,
            'phone': numbers
        }
    except:
        pass
    return(contact)


my_file = 'test_email.eml'

headers = header_parser(my_file)

from_val = headers['From']
contact = re.sub(r'[^@. a-zA-Z]', '', from_val).split()

numbers = num_catcher(my_file)
contact = dict_pop(contact, numbers)

print(contact)

# emails = email_catcher(my_file)
# print(emails)
