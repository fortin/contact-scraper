#!/usr/bin/env python3
#
#  Contact Scraper for email
#
#  Copyright (c) 2019 Antonio Fortin. All rights reserved.
#

import re
import email.message
from email.parser import HeaderParser
import phonenumbers
from names_dataset import NameDataset

def payload_parser(filename):
    # parse email headers
    with open(filename, 'r') as msg:
        # if msg.is_multipart():
        #     for payload in msg.get_payload():
        #         # if payload.is_multipart(): ...
        #         print(payload.get_payload())
        # else:
        #     body = msg.get_payload()
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
        if len(numbers) == 0:
            numbers = None
            return(numbers)
        # else:
        #     numbers = numbers[0]#str(numbers).replace("{'", "").replace("'}", "")
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
    """
    Populate dictionary with contact info from headers.

    Arguments:
    contact - cleaned-up From header comprising sender's name and email address
    numbers - phone numbers scraped from body

    Outputs:
    Python dictionary with contact fields as keys and scraped info as values
    """

    last_name = [ x for x in contact if m.search_last_name(x) ]
    first_name = [ x for x in contact if m.search_first_name(x) ]
    # catch cases where both names are valid last_names
    if len(last_name) > 1:
        # catch cases where both names are valid first_names
        if len(first_name) > 1:
            # assign variables according to 'first_name last_name' order in header
            last_name = last_name[1]
            first_name = first_name[0]
        else:
            # if only last_name is ambiguous, get it from the second list element
            last_name = last_name[1]
    # if only first_name is ambiguous, get it from first list element
    elif len(first_name) > 1:
        first_name = first_name[0]
    # strip non-alphanumeric characters and convert lists to strings
    last_name = re.sub(r'[^@. a-zA-Z]', '', str(last_name))
    first_name = re.sub(r'[^@. a-zA-Z]', '', str(first_name))
    email = [ x for x in contact if "@" in x ]
    email = re.sub(r'[^@. a-zA-Z]', '', str(email))
    domain = re.sub(r"[a-zA-Z0-9_.+-]+@([a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)",
                    r"\1",
                    email)
    # TODO is there a way to have a for loop that applies the regex to each variable as a string, and overwrites the variable with the output?
    try:
        contact = {
            'lastname': last_name,
            'firstname': first_name,
            'email': email,
            'company': domain,
            'address': None,
            'phone': numbers
        }
    except:
        pass
    return(contact)

m = NameDataset()
my_file = 'BankWireReceived.eml'

headers = payload_parser(my_file)

from_val = headers['From']
contact = re.sub(r'[^@. a-zA-Z]', '', from_val).split()

numbers = num_catcher(my_file)
print(numbers)
contact = dict_pop(contact, numbers)

# print(first_name, last_name)
print(contact)

# emails = email_catcher(my_file)
# print(emails)
