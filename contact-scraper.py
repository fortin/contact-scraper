#!/usr/bin/env python3
#
#  Contact Scraper for Gmail
#
#  Created by Antonio Fortin on 2019-04-01.
#  Copyright (c) 2019 Antonio Fortin. All rights reserved.
#

import phonenumbers
import re

pattern = re.compile(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)")
email = open('test_email.eml')
my_email = email.read()

emails = set()
numbers = set()

for i, line in enumerate(open('test_email.eml')):
    for match in re.finditer(pattern, line):
        emails.update(match.groups())

for match in phonenumbers.PhoneNumberMatcher(my_email, "US"):
    try:
        numbers.add(phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.E164))
    except(TypeError):
        pass

print(emails, numbers)
