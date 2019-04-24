#!/usr/bin/env python3
#
#  Contact Scraper for Gmail
#
#  Created by Antonio Fortin on 2019-04-01.
#  Copyright (c) 2019 Antonio Fortin. All rights reserved.
#

import usaddress
import re

pattern = re.compile(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)")

emails = set()
addresses = set()

for i, line in enumerate(open('test_email.eml')):
    for match in re.finditer(pattern, line):
        emails.update(match.groups())

for match in usaddress.parse(enumerate(open('test_email.eml'))):
    addresses.update(match.groups())

print(emails, addresses)
