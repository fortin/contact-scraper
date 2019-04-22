#!/usr/bin/env python3
#
#  Contact Scraper for Gmail
#
#  Created by Antonio Fortin on 2019-04-01.
#  Copyright (c) 2019 Antonio Fortin. All rights reserved.
#

# import talon
# from pathlib import Path
from talon.signature.bruteforce import extract_signature

# talon.init()

# from talon import signature

my_sig = """Dear Subscriber,
Tom Paladino, a scalar energy researcher, is committed to ensure that the best data protection and compliance data policies are in place. Our privacy policy explains how we collect and use personal data. The purpose of this communication is to offer you and your family complimentary scalar light healing sessions. There is no obligation to participate in these complimentary scalar light healing sessions.
Why we are contacting you? We are contacting you today as part of our compliance with the General Data Protection Regulations (GDPR) which came into force on 25th May 2018.
The data that we possess includes your name and email address. The GDPR classifies information such as your name and email address as personal data.
What do we do with the data? We use the data to contact you from time to time to provide you with complimentary scalar light healing sessions. These complimentary scalar light healing sessions carry no obligation.
The lawful basis we use for this processing is "Legitimate Interest" for "direct marketing". It is recommended that companies using this basis conduct a "Legitimate Interests Assessment" (LIA), which we have done. You subscribed to our offer for a complimentary scalar light session or heard about us and subsequently subscribed to our newsletter.
To register for the complimentary 15 day session please visit:  WWW.FREESCALAR.US
To confirm your acceptance to receive emails as well as the complimentary scalar light sessions, please confirm.
You can unsubscribe at any time.
You have the right to opt out of future communications and the quickest way to do this is to use the unsubscribe link at the bottom of this email.
Thank you.

--
Tom Paladino
1767 Lakewood Ranch Blvd #231
Lakewood Ranch, Florida 34211
805-364-3051 or 800-345-9851
support@scalarlight.com
SelfHealGo.com / ScalarLight.com"""

# If you do not wish to receive further emails from us, click here to unsubscribe.  You can read our Privacy Policy here.  If you have any questions about this email, please contact admin@scalarlight.com."""

# with open('sig_test3.txt', 'r', encoding='utf-8') as email_msg:
#     my_sig = email_msg.read()
# email_msg = open('sig_test2.eml')
# my_sig = Path(email_msg).read_text()

# text, signature = signature.extract(my_sig, sender='john.doe@example.com')

text, signature = extract_signature(my_sig)

print(signature)
