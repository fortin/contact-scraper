#!/usr/bin/env python3
#
#  Contact Scraper for email
#
#  Copyright (c) 2019 Antonio Fortin. All rights reserved.
#

import sys
import re
import email
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

def body_extractor(filename):
    """
    Extract body of email message from file.
    """
    msg = email.message_from_file(open(filename, 'r'))
    body = ''

    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get('Content-Disposition'))

        # skip any text/plain (txt) attachments
            if ctype == 'text/plain' or ctype == 'text/html' and 'attachment' not in cdispo:
                body = part.get_payload(decode=True) # decode
                break
    # not multipart - i.e. plain text, no attachments
    else:
        body = b.get_payload(decode=True)
    # strip HTML and remove \r, \t, \n
    body = re.sub('<[^<]+?>', '', str(body)).replace('\\r', '\r').replace('\\n', '\n').replace('\\t', '')
    # is there a more general, additive way to do this?
    return(body)

def num_catcher(filename):
    """
    Extract all US phone numbers from message and return last one
    """
    with open(filename, 'r') as msg:
        my_email = msg.read()
        numbers = set()
        for match in phonenumbers.PhoneNumberMatcher(my_email, "US"):
            numbers.add(phonenumbers.format_number(
                match.number, phonenumbers.PhoneNumberFormat.E164))
            # if numbers != set():  # stop after first match (not ideal)
            #     break
        if len(numbers) == 0:
            numbers = None
            return(numbers)
        # else:
        #     numbers = numbers[0]#str(numbers).replace("{'", "").replace("'}", "")
    numbers = list(numbers)
    numbers = numbers[-1]
    return(numbers)


def email_catcher(filename):
    """
    Extract all email addresses from message
    Not used and probably not necessary
    """
    pattern = re.compile(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)")
    emails = set()
    with open(filename) as f:
        for i, line in enumerate(f):
            for match in re.finditer(pattern, line):
                emails.update(match.groups())
    return(emails)


def dict_pplt(contact, numbers):
    email_regex = re.compile(r"(^[a-zA-Z0-9_.+-]+@([a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$))")
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
    elif (len(last_name) == 1) & (len(first_name) == 0):
        last_name = last_name[0]
    elif (len(last_name) == 0) & (len(first_name) == 1):
        first_name = first_name[0]
    else:
        pass
    # strip non-alphanumeric characters and convert lists to strings
    last_name = re.sub(r'[^@. a-zA-Z]', '', str(last_name))
    first_name = re.sub(r'[^@. a-zA-Z]', '', str(first_name))
    try:
        email = [ x for x in contact if bool(re.search(email_regex, x)) ][-1]
    except:
        email = None
    email = re.sub(r'[^@. a-zA-Z]', '', str(email))
    domain = re.sub(email_regex, r"\2", email)
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
my_file = 'test_email.eml'

headers = header_parser(my_file)

from_val = headers['From']
contact = re.sub(r'[^@. a-zA-Z]', '', from_val).split()

numbers = num_catcher(my_file)
# print(numbers)
contact_dict = dict_pplt(contact, numbers)

print(contact_dict)

body = body_extractor(my_file)
print(body)

# name = (contact[0] + ' ' + contact[1])
# print(name)

# emails = email_catcher(my_file)
# print(emails)
