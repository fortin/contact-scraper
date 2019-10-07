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
import csv
import os
import glob
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

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
    return emails

def header_parser(filename):
    """
    Parse email headers
    """
    with open(filename, 'r') as msg:
        my_email = msg.read()
        parser = HeaderParser()
        h = parser.parsestr(my_email)
        headers = dict(h.items())
    return headers

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
    return body

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
    # numbers = re.sub('^(.+)$', r'\"\1\"', str(numbers))
    return numbers

def xfrom_from(headers):
    """
    Parse headers and return tuple with available contact info.
    """
    from_val = []
    from_regex = re.compile('<\/.+?>')
    # if no 'From' or 'X-From', check for 'Sender'
    if ('From' not in headers) and ('X-From' not in headers):
        if ('Sender' in headers):
            from_val = headers['Sender']
        else:
            print("Input is not a valid email. Try again")
            sys.exit()
    # if From but no X-From, from_val is From, and conversely
    if ('From' in headers) and ('X-From' not in headers):
        from_val = headers['From']
        from_val = from_val.replace('\"', '').replace("\'", "")
    if ('From' not in headers) and ('X-From' in headers):
        from_val = headers['X-From']
        from_val = from_val.replace('\"', '').replace("\'", "")
    # if both, concatenate them
    if ('From' in headers) and ('X-From' in headers):
        from_hd = headers['From']
        from_hd = from_hd.replace('\"', '').replace("\'", "")
        xfrom_hd = headers['X-From']
        xfrom_hd = xfrom_hd.replace('\"', '').replace("\'", "")
        from_val = xfrom_hd + ' ' + from_hd
    from_val = [ x for x in from_val.split() if not from_regex.search(x) ]
    if re.match(r"^.+?,\', .+?", str(from_val)):
        from_val = re.sub("(\[)(.+?,)\', ((.+?)+?) (.+?)( .+?)?", r"\1\3 \2' ", str(from_val))
        from_val = from_val.replace(',', '')
    return from_val

def str_cleaner(x):
    x = re.sub(r'[^@. a-zA-Z]', '', str(x))
    return x

def dict_pplt(contact, numbers, middle_name, filename):
    """
    Populate dictionary with contact info from headers.

    Arguments:
    contact - cleaned-up From header comprising sender's name and email address
    numbers - phone numbers scraped from body

    Outputs:
    Python dictionary with contact fields as keys and scraped info as values
    """
    last_name = [ x for x in contact if m.search_last_name(x) ]
    first_name = [ x for x in contact if m.search_first_name(x) ]
    email_regex = re.compile(r"(^[a-zA-Z0-9_.+-]+@([a-zA-Z0-9-]+\.)?([a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$))")
    # Andy from Tandy cases
    a_from_b = re.compile(r"\[(\'.+), \'(@|[Ff]rom)\', (\'.+), \'(.+?)\'\]")
    if re.match(a_from_b, str(contact)):
        # first_name last_name @/from company
        name = a_from_b.match(str(contact)).group(1)
        if re.search(r", ", name):
            name = name.split()
            first_name = name[0]
            last_name = name[1]
        else:
        # cases where only one unambiguous first name is there
            first_name = a_from_b.match(str(contact)).group(1)
            last_name = None
        domain = a_from_b.match(str(contact)).group(3)
        domain = str_cleaner(domain)
    # cases where both names are valid last_names
    elif len(last_name) > 1:
        # cases where both names are valid first_names
        if len(first_name) > 1:
            # assign variables according to 'first_name last_name' order in header
            last_name = last_name[1]
            first_name = first_name[0]
        # if first_name is second element in last_name, then first element of last_name is last name (i.e., From field is in last_name first_name order)
        elif re.match(r"\[\'.+?\', \'" + str(first_name), str(last_name)):
            last_name = last_name[0]
        else:
            # if only last_name is ambiguous, get it from the second list element
            last_name = last_name[1]
    # if only first_name is ambiguous, get it from first list element
    elif len(first_name) > 1:
        first_name = first_name[0]
    # if there is one good last name and no first names, leave first name empty
    elif (len(last_name) == 1) and (len(first_name) == 0):
        last_name = last_name[0]
        first_name = None
    # converse of above
    elif (len(last_name) == 0) and (len(first_name) == 1):
        first_name = first_name[0]
    # if first and last name are identical, assume that it's just a first name
    elif last_name == first_name:
        last_name = None
    else:
        pass
    if not first_name:
        first_name = None
    elif not last_name:
        last_name = None
    elif last_name == first_name:
        last_name = None
    # strip non-alphanumeric characters and convert lists to strings
    last_name = str_cleaner(last_name)
    first_name = str_cleaner(first_name)
    try:
        email = [ x for x in contact if bool(re.search(email_regex, x)) ][-1]
        email = str_cleaner(email)
    except:
        email = None
    if 'domain' not in locals():
        domain = re.sub(email_regex, r"\3", email)
    try:
        contact = {
            'title': None,
            'lastname': last_name,
            'firstname': first_name,
            'middlename': middle_name,
            'job_title': None,
            'email': email,
            'company': domain,
            'address': None,
            'phone': numbers,
            'filename': filename
            }
    except:
        pass
    return contact

def csv_writer(sig_path):
    """
    Processes directory of emails and appends contact dictionary to csv file.
    """
    from_regex = re.compile('<\/.+?>')
    for my_file in glob.glob(os.path.join(sig_path, '*.txt')):
        headers = header_parser(my_file)
        from_val = xfrom_from(headers)
        contact = str_cleaner(from_val).split()
        if re.match(r"^[a-zA-Z]$", contact[1]):
            middle_name = contact[1]
            del contact[1]
        elif re.match(r"^[a-zA-Z]$", contact[2]):
            middle_name = contact[2]
            del contact[2]
        else:
            middle_name = None
        numbers = num_catcher(my_file)
        contact_dict = dict_pplt(contact, numbers, middle_name, my_file)
        with open('contacts.csv', 'a') as f:
            f.write("\n")
            for key in contact_dict.keys():
                f.write("%s,"%(contact_dict[key]))
    return

def test_email(my_file):
    headers = header_parser(my_file)
    from_val = xfrom_from(headers)
    contact = str_cleaner(from_val).split()
    print(contact)
    if re.match(r"^[a-zA-Z]$", contact[1]):
        middle_name = contact[1]
        del contact[1]
    elif re.match(r"^[a-zA-Z]$", contact[2]):
        middle_name = contact[2]
        del contact[2]
    else:
        middle_name = None
    numbers = num_catcher(my_file)
    contact_dict = dict_pplt(contact, numbers, middle_name, my_file)
    return contact_dict


m = NameDataset()
# cv = CountVectorizer()

sig_path = "data/sig"
nosig_path = "data/nosig"

job_titles = pd.read_csv("data/job_title_dictionary 2.txt")
# print(job_titles)

job_titles['Job Title'] = job_titles['Job Title'].apply(lambda x: x.casefold())
# print(job_titles)
csv_writer(sig_path)

def is_title(x):
    x = " ".join(x.casefold().strip().split())
    return x in job_titles['Job Title'].values

def is_title_sen(x):
    # loop through bigrams looking for job title
    bigram_vectorizer = CountVectorizer(ngram_range=(1, 3),
                                    token_pattern=r'\b\w+\b', min_df=1)
    analyze = bigram_vectorizer.build_analyzer()
    # print(sum(list(map(is_title, analyze(x)))))
    # print(analyze(x))# >= 1)
    return sum(list(map(is_title, analyze(x)))) >= 1

my_file3 = '/Users/antonio/Documents/Dropbox/Code/Python/Contact-Scraper/data/sig/arnold-j-67.txt'
# contact_dict = test_email(my_file3)
# print(contact_dict)
# my_file1 = '/Users/antonio/Documents/Dropbox/Code/Python/Contact-Scraper/data/sig/crandell-s-35.txt'
# my_file2 = '/Users/antonio/Documents/Dropbox/Code/Python/Contact-Scraper/data/sig/allen-p-30.txt'
# my_file = 'test_email.eml'
# contact_dict = test_email(my_file)
# print(contact_dict)
# contact_dict = test_email(my_file1)
# print(contact_dict)
# contact_dict = test_email(my_file2)
# print(contact_dict)

# print(m.search_last_name('Robertson'))
# m.search_first_name(x)

# print(is_title('scary Monster'))
# print(is_title('  TeAchEr   '))
# print(is_title('Data     SCientist'))

# print(is_title_sen(body_extractor(my_file)))
#
# print(is_title_sen('Ich    werde ein 3d scheisse'))
# print(is_title_sen('I am a      Data     scientist     '))
# print(is_title_sen('Calligrapher'))

# body = body_extractor(my_file)
# print(body)


# emails = email_catcher(my_file)
# print(emails)
