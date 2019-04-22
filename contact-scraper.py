#!/usr/bin/env python3
#
#  Contact Scraper for Gmail
#
#  Created by Antonio Fortin on 2019-04-01.
#  Copyright (c) 2019 Antonio Fortin. All rights reserved.
#

import re
from talon.signature.bruteforce import extract_signature
import postal_address
import phonenumbers

pattern = re.compile(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)")

emails = set()
numbers = set()

email_file = open('test_email.eml')
my_text = email_file.readlines()
numbers_file = open('phonenumbers.txt')
my_numbers = numbers_file.read()

for i, line in enumerate(my_text):
    for match in re.finditer(pattern, line):
        emails.update(match.groups())
    # try:
    #     for match in phonenumbers.PhoneNumberMatcher(my_text, "US"):
    #         phonenumbers.update(match.groups())
    # except(TypeError):
    #     print('Type Error')

for i, line in enumerate(my_numbers):
    try:
        for match in phonenumbers.PhoneNumberMatcher(my_numbers, "US"):
            numbers.update(match.groups())
            # print(match)
    except(TypeError):
        print('Type Error')

print(emails, numbers)
