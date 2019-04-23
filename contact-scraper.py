#!/usr/bin/env python3

from talon.signature.bruteforce import extract_signature

with open('email1.txt', 'r', encoding='utf-8') as email_msg:
    my_sig = email_msg.read()

text, signature = extract_signature(my_sig)

print('Signature found: \n' + str(signature) + '\n')

with open('email2.txt', 'r', encoding='utf-8') as email_msg:
    my_sig = email_msg.read()

text, signature = extract_signature(my_sig)

print('Signature found: \n' + str(signature))
