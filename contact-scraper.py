#!/usr/bin/env python3
#
#  Contact Scraper for Gmail
#
#  Created by Antonio Fortin on 2019-04-01.
#  Copyright (c) 2019 Antonio Fortin. All rights reserved.
#

import phonenumbers
import re
import email
import email.parser

pattern = re.compile(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)")
msg = open('test_email.eml')
my_email = msg.read()

emails = set()
numbers = set()

parser = email.parser.HeaderParser()
headers = parser.parsestr(str(my_email))

for h in headers.items():
    print(h)

for i, line in enumerate(open('test_email.eml')):
    for match in re.finditer(pattern, line):
        emails.update(match.groups())

for match in phonenumbers.PhoneNumberMatcher(my_email, "US"):
    try:
        numbers.add(phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.E164))
    except(TypeError):
        pass

print(emails, numbers)
