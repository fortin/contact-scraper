#!/usr/bin/env python3

import talon
talon.init()

from talon import signature

with open('email1.txt', 'r', encoding='utf-8') as email_msg:
    my_sig = email_msg.read()

text, signature = signature.extract(my_sig, sender='mike@blacklodge.org')

print('Email 1 signature: \n' + str(signature) + '\n')

with open('email2.txt', 'r', encoding='utf-8') as email_msg:
    my_sig = email_msg.read()

text, signature = signature.extract(my_sig, sender='mike@blacklodge.org')

print('Email 2 signature: \n' + str(signature))
