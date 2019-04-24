#!/usr/bin/env python3
#
#  Contact Scraper for Gmail
#
#  Created by Antonio Fortin on 2019-04-01.
#  Copyright (c) 2019 Antonio Fortin. All rights reserved.
#

import phonenumbers

numbers_file = open('test_email.eml', 'r')
my_numbers = numbers_file.read()

numbers = set()

for match in phonenumbers.PhoneNumberMatcher(my_numbers, "US"):
    try:
        numbers.add(phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.E164))
    except(TypeError):
        pass

print(numbers)
