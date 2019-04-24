#!/usr/bin/env python3
#
#  Contact Scraper for Gmail
#
#  Created by Antonio Fortin on 2019-04-01.
#  Copyright (c) 2019 Antonio Fortin. All rights reserved.
#

import usaddress
import re

addresses = set()

for match in usaddress.parse(enumerate(open('test_email.eml'))):
    addresses.update(match.groups())

# for i, line in enumerate(open('test_email.eml')):
#     for match in re.finditer(pattern, line):
#         addresses.update(match.groups())

print(addresses)
