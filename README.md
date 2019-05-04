# Contact Scraper

### A tool to scrape contact info from email messages. 

Contact Scraper takes raw email messages as input and attempts to return a Python dictionary populated with the sender's contact information.


## To-do

1) Get Mailgun talon to extract signatures reliably, so more complete contact info can be parsed from there;

2) Extract address info using postal-address or usaddress libraries;

3) Fix dict_pop() 